__author__ = 'cjllop'

import pymongo
import sys
import re

# Lexical diversity is calculated by finding the number of unique tokens in the text divided by the
# total number of tokens in the text. Because of this, we must clean the text to only have what
# we want to consider "tokens".

# Assumption: For each tweet, I will filter out "RT" (if a retweet), @user_names (links to other users),
# and URLS. I will NOT filter out hashtags, as these typically represent the subject of which the
# tweeter is discussing, and thus seems as though it would be a valid part of the language diversity for
# the user.

# In other parts of this assignment, I do not filter out unicode. That is, I allow tweets with unicode
# characters to be included in the results for "top 30". For the lexical diversity calculation, I will
# strip out unicode using regex to simplify the assignment. This should not impact English words, but will
# strip out letters that are accented or involve other symbol-based languages. For many romance languages,
# this will not matter because the unique "word" will still be counted, even if it is spelled incorrectly
# once accented characters are removed (though in some cases removing the accent may cause one word to turn
# into another valid word).

# Another consideration is that of "stop words". Stop words are frequent, low-value words such as "the"
# or "an". They would add in heavily to the denominator of the lexical diversity equation, but only
# be represented once each in the numerator. For this analysis, I have decided NOT to remove stop words.
# Our final output will be a plot of lexical diversity by user. Because we are comparing users with each other,
# as opposed to with external results, it is less important to worry about the absolute magnitude of my
# lexical diversity calculation, and more important to ensure it is consistently applied across users in my
# tweet database. While including stop words will reduce the overall magnitude of my lexical diversity measure,
# it will still be comparable across users.

# I have decided not to address stemming in this code due to time constraints. While one could argue that
# lexical diversity only depends on the stems used, one could also argue that it is diverse to use multiple
# conjugations of the same stem. As the assignment instructions did not address this point, I am making the
# design decision to not deal with stemming at this time.

# Finally, I will also ignore any "words" that are only made up of numbers (or numbers and a decimal).

# Note: Our "Lexical Diversity" measure will be biased, because we only gathered a sample of tweets with the
# phases "Microsoft" and "Mojang", thus we have limited ourselves to certain types of tweets.

def clean_tweet(tweet):
# The regex function "clean_tweet" applies regex cleaning with the limitations discussed above (and some not
# discussed for brevity
    # remove RT for retweets (note, I found that sometimes these are nested RTs, so I remove any instance of "\bRT\b")
    strip_1 = re.sub(r'\bRT\b', '', tweet[u'text'])
    # print strip_1
    # remove hyperlinks
    strip_2 = re.sub(r'\bhttp://[^\s]*\b', '', strip_1)
    # print strip_2
    # other usernames
    strip_3 = re.sub(r'[\s]@[a-zA-Z_0-9]*\b', '', strip_2)
    # print strip_3
    # remove nonword characters - see notes above
    strip_4 = re.sub(r'[^ \w]', '', strip_3)
    # print strip_4
    # remove words that are purely numbers
    strip_5 = re.sub(r'\b[0-9]*\b', '', strip_4)
    # print strip_5
    return strip_5

def index_screenname(db_streamT):
    db_streamT.create_index('user.screen_name')

if __name__ == '__main__':
    # Set up MongoDB connection
    try:
        connection = pymongo.MongoClient()
        db = connection['Assignment']
        db_streamT = db['db_streamT']
        db_lex = db['tweet_lexicon']
    except:
        print "Exception while connecting to MongoDB"
        sys.exit(0)

    # Empty db_lex since we want to populate it in this code
    if db_lex.count() != 0:
        db_lex.drop()

    # To solve the problem of not storing too much data in memory, we sort the MongoDB by screen_name and
    # return results in that order. We can then process each user, one at a time, and then store their
    # lexical diversity back to a MongoDB. In a way, we let Mongo be our mapper, and then we reduce the results.
    # Note - the line below only needs to be run once to index the MongoDB for sorting.
    # index_screenname(db_streamT)

    prev_user = None
    user_lexicon = []
    i = 1

    #Process tweet text in sorted order by username
    print "db_streamT has " + str(db_streamT.count()) + " records to process."
    for tweet in db_streamT.find().sort('user.screen_name', 1):
        if i % 1000 == 0:
            print "Processing record " + str(i)
        if tweet[u'user'][u'screen_name'] != prev_user:
            #print "Distinct:"  + str(len(set(user_lexicon)))
            #print "Total: " + str(len(user_lexicon))
            if prev_user != None:
                try:
                    # Calculate diversity and store in Mongo. We round to only 2 decimal place so we can easily
                    # plot a histogram later.
                    diversity = round(float(len(set(user_lexicon))) / float(len(user_lexicon)), 2)
                    db_lex.insert({'screen_name':prev_user, 'lex_dev':diversity})
                except Exception:
                    pass
            prev_user = tweet[u'user'][u'screen_name']
            user_lexicon = []
            # print
            # print prev_user

        clean_text = clean_tweet(tweet)
        user_lexicon = user_lexicon + nltk.tokenize.word_tokenize(clean_text)
        #print user_lexicon
        i += 1


    # Make a histogram of lexical diversity
    diversity_data = db_lex.aggregate( [
        {"$group": {"_id": "$lex_dev",
            "count": { "$sum":1}}},
        {"$sort": { "_id": -1 } },
    ] )

    to_plot = []
    columns = 100
    # store in tuple for processing
    for line in diversity_data[u'result']:
        to_plot.append((str(line[u'_id']), line[u'count']))
        print line

    print to_plot
    n_occurrences = len(to_plot)
    preLabels, values = zip(*to_plot)
    i = 0
    labels = []
    for l in preLabels:
        labels.append(preLabels[i] + " (" + str(values[i]) + ")")
        i = i + 1
    label_width = max(map(len, labels))
    data_width = columns - label_width - 1
    plot_format = '{:%d}|{:%d}' % (label_width, data_width)
    max_value = float(max(values))

    print('Saving histogram')
    for i in range(len(labels)):
        try:
            v = int(values[i]/max_value*data_width)
            str = (plot_format.format(labels[i], '*'*v))
            with open('lexical_diversity_hist.txt', 'a') as outfile:
               outfile.write(str +'\n')
        except Exception:
            pass
    print('Save complete')

    # Note - this analysis showed that a large number of users have a lexical diversity of 1. After this, we
    # see a hump in the lower 90s and 80s. Note that many users likely only had a few tweets for the hashtags
    # studied during the period of interest, leading to this pattern (and the many 1s).