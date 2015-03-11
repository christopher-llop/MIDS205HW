import boto
import json
import pymongo
import sys

# Class to handle exceptions
class MyException(Exception):
    pass

# helper function to empty the db_tweets while troubleshooting code
def empty_db(db_store):
    db_store.drop()
    print "Emptied MongoDB, now ready for new data."


#get all tweet text from s3, and store in mongoDB
def load_tweets_from_S3(db_store):
    print("Loading data from S3...")
    try:
        s3 = boto.connect_s3()
        files = []
        for i in range(1,8):
            files.append("Tweet Day 2015-03-0" + str(i) + ".txt")
    except Exception:
        raise MyException("Trouble connecting to boto")

    try:
        for file in files:
            try:
                print("Loading file " + file + " from S3.")
                key = s3.get_bucket('com.christopherllop.w205assignment2').get_key(file)
                full_doc = key.get_contents_as_string()
                print("Storing tweets in MongoDB.")
                for tweet in full_doc.split('\n'):
                    #store in db_tweets
                    if tweet != '':
                        tweet_json = json.loads(tweet)
                        text_json = {u'text':tweet_json[u'text']}
                        db_store.insert(text_json)
                print("File " + file + " loaded.")
            except Exception:
                pass

    except Exception:
        pass
        raise MyException("Exception while pulling data from S3 and saving to Mongo")
    except KeyboardInterrupt:
        raise MyException("KeyboardInterrupt detected")


if __name__ == '__main__':
    # Set up MongoDB connection
    try:
        connection = pymongo.MongoClient()
        db = connection['Assignment']
        db_streamT = db['db_streamT']
        db_tweets = db['db_tweets']
    except:
        print "Exception while connecting to MongoDB"
        sys.exit(0)

    #line below used for debugging
    #empty_db(db_tweets)

    try:
        load_tweets_from_S3(db_tweets)
    except MyException as e:
        print e.message