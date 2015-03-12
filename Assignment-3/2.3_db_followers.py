__author__ = 'cjllop'

import pymongo
import sys
import tweepy
import time
from lloplib import setuptweepy

def pull_followers(api, db_top30, db_followers, pull_num):
    for top_tweet in db_top30.find():
        try:
            top_name = top_tweet[u'screen_name']
            starting_follower_count = top_tweet[u'followers_count']
            print "Getting followers for user '" + top_name + "', who had " + str(starting_follower_count) +" when we first scraped the tweets."
            i = 1
            for user in tweepy.Cursor(api.followers, screen_name=top_name).items():
                 try:
                     db_followers.insert({'screen_name':top_name, 'follower_name':user.screen_name, 'pull_num':pull_num})
                     if i % 5000 == 0:
                         print "Processing follower #" + str(i) + " for user " + top_name
                     i += 1
                 except Exception:
                     pass
        except Exception:
            pass

if __name__ == '__main__':
    # Set up MongoDB connection
    try:
        connection = pymongo.MongoClient()
        db = connection['Assignment']
        db_top30 = db['top_30_retweets'] #used to store data on the original poster of top 30 tweets
        db_followers = db['db_followers'] #store follower data
        db_unfollowers = db['db_unfollowers'] #store records of those who unfollow to answer the assignment
    except Exception:
        print "Exception while connecting to MongoDB"
        sys.exit(0)

    #empty db_followers/unfollowers since we want them to be created in this code
    if db_followers.count() != 0:
        db_followers.drop()
    if db_unfollowers.count() != 0:
        db_unfollowers.drop()

    # Setup Tweepy API
    try:
        api = setuptweepy.prepare_api()
    except Exception:
        print "Trouble connecting to Twitter. Ending program."
        sys.exit(0)

    #The Problem: We want to find the difference in followers at two points in time.
    # Each user has a large number of followers, and we do not want to store them all in memory at once.
    # To solve this, we store MongoDB records with three items:
        #user_name:XYZ follower_name: ZYX pull_num: 1
        #where the user_name and follower_name are self explanatory. Pull_num = 1 at time 0, and 2 at time 1-week
    # We can then use the aggregate function to identify followers who are only in the dataset at pull_num = 1
    # and not pull_num = 2
    print "Run first pull of follower data."
    pull_followers(api, db_top30, db_followers, 1)
    print "Wait one week."
    # time.sleep(604800)
    print "Run second pull of follower data."
    # pull_followers(api, db_top30, db_followers, 2)

    # run aggregate analysis
    follower_analysis_1 = db_followers.aggregate( [
       {"$group": {"_id": {"screen_name":"$screen_name","follower_name":"$follower_name"},
            "total": { "$sum": 1 },
            "last": { "$max":"$pull_num"}}},
       {"$sort": { "total": 1 } }
    ] )

    # print results from aggregate analysis
    print
    print "These users are no longer following:"
    for check in follower_analysis_1[u'result']:
        try:
            # If the condition below is met, the screen_name/follower_name pair only appeared once, the first time
                # we pulled followers. This means they are in the desired set of output
            if check[u'total'] == 1 and check[u'last'] == 1:
                name_data = check[u'_id']
                db_unfollowers.insert({u'screen_name':name_data[u'screen_name'],u'follower_name':name_data[u'follower_name']})
                print name_data[u'follower_name'] + " is no longer following " + name_data[u'screen_name'] + "."
        except Exception:
            pass
