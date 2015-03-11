import sys
import tweepy
import urllib
import json
import time
import boto
import pymongo

# Class to handle exceptions
class MyException(Exception):
    pass

# Twitter API Connections
def prepare_api():
    consumer_key = "gugILTi6ETCi960kjuya4fuNu";
    consumer_secret = "ZRdj9rV7EtUCr5Xidl6wBNPKnnUK85gYG505oU0SAkWDypmHA0";

    access_token = "92593109-h8KCVfbdWUViEMXZGembTgOqgWt4cNOxNqNVfuOW5";
    access_token_secret = "vAs7KqAA30fop4Wdtw4pDADA26wjoYePH0lcyFaTshcve";

    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
    except Exception:
        raise MyException("Exception: Problem with creating authentication tokens")

    try:
        api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    except Exception:
        raise MyException("Exception: Problem calling tweepy.API")

    return api

# Pull and Save Tweets
def twitter_scrape(q, db):
    try:
        tweet_cursor = tweepy.Cursor(api.search, q=q).items()
    except Exception:
        raise MyException("Exception: Problem calling tweepy Cursor")

    #Note - tweepy handles rate limiting for us
    for tweet in tweet_cursor:
        try:
            # Get Date to Partition Raw Data
            ts = time.strptime(tweet._json['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
            file_path = "Tweet Day " + time.strftime('%Y-%m-%d', ts) + "alt.txt"

            # Store data in MongoDB
            db.insert(tweet._json)

            # Save raw data to partitioned files based on date
            with open(file_path, 'a') as outfile:
                json.dump(tweet._json, outfile)
                outfile.write('\n')
        except Exception:
            pass
        except KeyboardInterrupt:
            raise MyException("KeyboardInterrupt during Scraping Process")

#Save to S3 using Boto
def save_to_S3():
    #Store to S3 - boto handles authentication through a config file in my user folder

    try:
        s3 = boto.connect_s3()
        bucket = s3.get_bucket('com.christopherllop.w205assignment2')
    except:
        raise MyException("Unable to connect to S3 bucket via boto")

    # Create list of file names automatically (note, this could be setup to allow the user
    # to define a date range both for the query and this portion of the code. The method
    # implemented remains flexible so this would only be a small change)
    try:
        files = []
        for i in range(1,8):
            files.append("Tweet Day 2015-03-0" + str(i) + ".txt")

        for file in files:
            print("Saving " + file + " to S3.")
            key = bucket.new_key(file)
            key.set_contents_from_filename('/Users/cjllop/Code/MIDS/Storage/MIDS205HW/Assignment-2/' + file)
            key.set_acl('public-read')
    except:
        raise MyException("Unable to save files to S3")

if __name__ == '__main__':
    # Set up MongoDB to store raw JSON
    try:
        # Establish connection to database
        connection = pymongo.MongoClient()
        db = connection['Assignment']
        micro_tweets = db['db_streamT']

        # Make sure the MongoDB database is empty. This code would need to be changed if we
        # decide later to append additional data.
        if micro_tweets.count() != 0:
            micro_tweets.drop()
            print "Emptied MongoDB, Now Ready for Data!"
        else:
            print "Empty MongoDB Ready for Data!"
    except:
        print "Exception while setting up MongoDB"
        sys.exit(0)

    # Set up the Tweepy API Connection
    try:
        api = prepare_api()
    except MyException as e:
        print e.message
        sys.exit(0)

    # Prepare the query. The commented out line is here as a placeholder in case we eventually want
    # the user to provide input via terminal. This program is set up with a hard-coded date range,
    # but with thought to how to require minimal changes for a user to define the date range instead.
    #q = urllib.quote_plus(sys.argv[1]) # URL encoded query
    q = urllib.quote_plus("#microsoft OR #mojang") # URL encoded query
    q = q + " since:2015-03-01 until:2015-03-08"

    # Run the Twitter Scrape using the query "q", saving data into the database "micro_tweets"
    try:
        twitter_scrape(q, micro_tweets)
    except MyException as e:
        print e.message
        sys.exit(0)

    # Robustness check - makes sure the mongoDB has data now. If not, notify the user and exit
    # the program
    if micro_tweets.count() == 0:
        print("No tweets pulled for the date range specified. Please change dates or terms, or run code again.")
        sys.exit(0)

    # Save results to S3
    try:
        save_to_S3()
    except MyException as e:
        print e.message
        sys.exit(0)


