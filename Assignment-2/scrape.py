import sys
import tweepy
import datetime
import urllib
import signal
import json
import time
import boto

#twitter login
consumer_key = "gugILTi6ETCi960kjuya4fuNu";
consumer_secret = "ZRdj9rV7EtUCr5Xidl6wBNPKnnUK85gYG505oU0SAkWDypmHA0";

access_token = "92593109-h8KCVfbdWUViEMXZGembTgOqgWt4cNOxNqNVfuOW5";
access_token_secret = "vAs7KqAA30fop4Wdtw4pDADA26wjoYePH0lcyFaTshcve";

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler=auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

#q = urllib.quote_plus(sys.argv[1]) # URL encoded query
q = urllib.quote_plus("#microsoft OR #mojang") # URL encoded query
q = q + " since:2015-01-31 until:2015-02-07"

#Pull and Save Tweets
for tweet in tweepy.Cursor(api.search, q=q).items():
   ts = time.strptime(tweet._json['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
   file_path = "Tweet Day " + time.strftime('%Y-%m-%d', ts) + ".txt"

   with open(file_path, 'a') as outfile:
       json.dump(tweet._json['text'], outfile)
       outfile.write('\n')


#Store to S3 - boto handle authentication through a config file in my user folder
s3 = boto.connect_s3()
bucket = s3.get_bucket('com.christopherllop.w205assignment2')
files = ["Tweet Day 2015-01-31.txt","Tweet Day 2015-02-01.txt","Tweet Day 2015-02-02.txt","Tweet Day 2015-02-03.txt",
         "Tweet Day 2015-02-04.txt","Tweet Day 2015-02-05.txt","Tweet Day 2015-02-06.txt"]

for file in files:
    key = bucket.new_key(file)
    key.set_contents_from_filename('/Users/cjllop/Code/MIDS/Storage/MIDS205HW/Assignment-2/' + file)
    key.set_acl('public-read')