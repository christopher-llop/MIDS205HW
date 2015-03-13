
import boto
import pymongo
import sys
import os
import json

def save_to_S3(db, db_name):
    print("Saving data to S3...")

    #Store to S3 - boto handles authentication through a config file in my user folder
    try:
        s3 = boto.connect_s3()
        bucket = s3.get_bucket('com.christopherllop.w205assignment3')
    except:
        raise Exception("Unable to connect to S3 bucket via boto")

    # Create list of file names automatically (note, this could be setup to allow the user
    # to define a date range both for the query and this portion of the code. The method
    # implemented remains flexible so this would only be a small change)
    try:
        i = 1
        print db_name + " has " + str(db.count()) + " records to process."
        with open(db_name + '_backup.txt', 'w') as outfile:
            for record in db.find():
                if i % 1000 == 0:
                    print "Writing record " + str(i)
                    outfile.write(str(record) + '\n')
                i += 1
        key = bucket.new_key(db_name + '_backup.txt')
        key.set_contents_from_filename('/Users/cjllop/Code/MIDS/Storage/MIDS205HW/Assignment-3/' + db_name + '_backup.txt')
        key.set_acl('public-read')
        os.remove('/Users/cjllop/Code/MIDS/Storage/MIDS205HW/Assignment-3/' + db_name + '_backup.txt')
        print "Saved " + db_name + "_backup.txt to S3."
    except:
        raise Exception("Unable to save to S3")


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


    test = json.load

    #save to S3
    #save_to_S3(db_streamT, "db_streamT")
    #save_to_S3(db_tweets, "db_tweets")

    load_from_S3(db_tweets, "db_tweets")