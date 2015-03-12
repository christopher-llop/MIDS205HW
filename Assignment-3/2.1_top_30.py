import pymongo
import sys

if __name__ == '__main__':
    # Set up MongoDB connection
    try:
        connection = pymongo.MongoClient()
        db = connection['Assignment']
        db_streamT = db['db_streamT']
        db_tweets = db['db_tweets']
        db_top30 = db['top_30_retweets'] #used to store data on the original poster of top 30 tweets
    except:
        print "Exception while connecting to MongoDB"
        sys.exit(0)

    #empty db_top30 since we want it to be created in this code
    if db_top30.count() != 0:
        db_top30.drop()

    #Note: the assignment specifically asks for retweets, meaning the data selected
    #must start with the "RT" tag (as opposed to one user tweeting the same
    #advertisement over and over, never being retweeted).
    #I will have the aggregate function store the top 100 results in memory, because
    #after examining the data I believe this is more than sufficient as a starting
    #point to then filter down to retweets only. I am trying to avoid storing all
    #of the retweets in memory by filtering to only RT posts first.
    top_30_RT_raw = db_tweets.aggregate( [
       {
         "$group": {
            "_id": "$text",
            "total": { "$sum": 1 }
         }
       },
       { "$sort": { "total": -1 } },
       { "$limit": 100}
    ] )

    #limit to the top 30 retweets. Let the random ordering break ties, since the
    #assignment requires 30 tweets and any tie-breaking algorithm would be equally
    #arbitrary.
    i = 1
    top_30_RT_list = []
    for tweet in top_30_RT_raw[u'result']:
        try:
            if tweet[u'_id'].startswith("RT @") and len(top_30_RT_list) < 30:
                top_30_RT_list.append(tweet)
                print "Tweet " + str(i) + " is a retweet. Add tweet: " + tweet[u'_id']
            elif len(top_30_RT_list) < 30:
                print "Tweet " + str(i) + " is NOT a retweet. Skip tweet: " + tweet[u'_id']
            i += 1
        except:
            pass


    #Get the data of interest from the db_streamT (this is exciting)
    #Note - Arash clarified that we want the data for the ORIGINAL tweeter, so we need to dig into the
    #"retweeted_status" key.
    for tweet in top_30_RT_list:
        try:
            #print str(i) + ": " + str(tweet)
            tweet_text = tweet[u'_id']
            full_tweet = db_streamT.find_one({'text':tweet_text})
            tweet_username = ((full_tweet[u'retweeted_status'])[u'user'])[u'screen_name']
            tweet_location = ((full_tweet[u'retweeted_status'])[u'user'])[u'location']
            #followers_count not requested in the assignment, but I am interested in printing this to screen in code
            #2.3 while processing the number of followers to provide a slightly better user experience.
            tweet_followers_count = ((full_tweet[u'retweeted_status'])[u'user'])[u'followers_count']

            db_top30.insert({u'text':tweet_text, u'screen_name':tweet_username, u'location':tweet_location,
                             u'observed_retweet':tweet[u'total'], u'followers_count':tweet_followers_count})
        except:
            print "Error while searching for original tweeter data. This is a required part of the assignment. Program terminating."
            sys.exit(0)

    print "DISPLAY RESULTS"
    for top_retweet in db_top30.find():
        print top_retweet
