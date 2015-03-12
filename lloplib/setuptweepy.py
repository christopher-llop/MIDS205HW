__author__ = 'cjllop'

import tweepy
from tweepy.auth import OAuthHandler


def prepare_api():
    consumer_key = "gugILTi6ETCi960kjuya4fuNu"
    consumer_secret = "ZRdj9rV7EtUCr5Xidl6wBNPKnnUK85gYG505oU0SAkWDypmHA0"

    access_token = "92593109-h8KCVfbdWUViEMXZGembTgOqgWt4cNOxNqNVfuOW5"
    access_token_secret = "vAs7KqAA30fop4Wdtw4pDADA26wjoYePH0lcyFaTshcve"

    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
    except Exception:
        raise Exception("Exception: Problem with creating authentication tokens")

    try:
        api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    except Exception:
        raise Exception("Exception: Problem calling tweepy.API")

    return api