from collections import Counter
import boto
import json
import pymongo

# Class to handle exceptions
class MyException(Exception):
    pass

def clean_words(text):
    words = []
    for w in text.lower().split():
        w2 = w.strip('!,.?-=$%^&*()_+:\'/\\\"')
        if not(w2.startswith("http://") or w2.startswith("https://") or w2.startswith("@") or w2.startswith("\\u")
                or w2.count('/') > 1 or w2.count('\\u') > 0 or w2 == '' or len(w2) > 30):
            words.append(w2)
    return words

# Get all tweet "text" from MongoDB
def get_words_mongo():
    print("Loading data from MongoDB...")
    try:
        # Establish connection to database
        connection = pymongo.MongoClient()
        db = connection['Assignment']
        micro_tweets = db['db_streamT']
    except Exception:
        raise MyException("Exception while connecting to MongoDB")

    try:
        print "Pulling " + str(micro_tweets.count()) +" records from MongoDB database"
        text = ''
        i = 0
        words = []
        for tweet_data in micro_tweets.find():
            i += 1
            text = text + tweet_data['text'] + ' '
            if i % 3000 == 0:
                print "Pulling record " + str(i) + " of " + str(micro_tweets.count()) + ". Processing words."
                words = words + clean_words(text)
                text = ''
        words = words + clean_words(text)
        text = ''
    except Exception:
        raise MyException("Exception while processing data")
    except KeyboardInterrupt:
        raise MyException("KeyboardInterrupt during data load")

    if words != []:
        print "Data read from MongoDB. Words cleaned for Histogram."
        return words

def get_words_s3():
    print("Loading data from S3...")
    try:
        s3 = boto.connect_s3()
        files = []
        for i in range(1,8):
            files.append("Tweet Day 2015-03-0" + str(i) + ".txt")
    except Exception:
        raise MyException("Trouble connecting to boto")

    try:
        words = []
        for file in files:
            print('Loading file ' + file + ' from S3')
            key = s3.get_bucket('com.christopherllop.w205assignment2').get_key(file)
            full_doc = key.get_contents_as_string()
            text = ''
            for tweet in full_doc.split('\n'):
                if tweet != '':
                    tweet_json = json.loads(tweet)
                    text = text + tweet_json[u'text'] + ' '


            print('Processing ' + file)
            words = words + clean_words(text)
    except Exception:
        raise MyException("Exception while pulling data from S3 and parsing data")
    except KeyboardInterrupt:
        raise MyException("KeyboardInterrupt during data load")

    if words != []:
        print "Data read from S3. Words cleaned for Histogram."
        return words

#def build_histogram(words):




if __name__ == '__main__':
    words = []
    # First try to pull data from local MongoDB
    if words == []:
        try:
            words = words + get_words_mongo()
        except MyException as e:
            print e.message

    # If that data is unavailable, pull from S3
    if words == []:
        try:
            words = words + get_words_s3()
        except MyException as e:
            print e.message

    # Only run histogram code if data was found
    if words != []:
        print('Building histogram')
        counter = Counter(words)

        columns = 100
        n_occurrences = len(counter)
        to_plot = counter.most_common(n_occurrences)
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
                with open('histogram.txt', 'a') as outfile:
                   outfile.write(str +'\n')
            except Exception:
                pass
        print('Save complete')
