import json
import tweepy
from twitter import OAuth, Twitter
from langdetect import detect
from textblob import TextBlob



class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        self.file = open("tweets.txt", "w")

    def on_status(self, status):
        tweet = status._json
        self.file.write(json.dumps(tweet) + '\n' )
        self.num_tweets += 1
        if self.num_tweets < 100:
            return True
        else:
            return False
        self.file.close()

    def on_error(self, status):
        print(status)


def read_credentials():
    with open("credentials.json", 'rb') as input:
        data = json.load(input)
        return data["access_token"], data["access_token_secret"],\
            data["consumer_key"], data["consumer_secret"]


def twitter_connect():
    acc_token, acc_secret, cons_key, cons_secret = read_credentials()
    auth = tweepy.OAuthHandler(cons_key, cons_secret)
    auth.set_access_token(acc_token, acc_secret)
    return tweepy.Stream(auth, MyStreamListener())


def trending_hashtags():
    acc_token, acc_secret, cons_key, cons_secret = read_credentials()
    twitter = Twitter(auth=OAuth(acc_token, acc_secret, cons_key, cons_secret))
    result = twitter.trends.place(_id=1)[0]["trends"]
    trends = map(lambda item: item["name"], result)
    return list(trends)


def filter_only_english_trends(trends):
    result = []
    for item in trends:
        if TextBlob(item).detect_language() == 'en':
            result.append(item)
    return result

#stream = twitter_connect()
#stream.filter(track=['clinton', 'trump', 'sanders', 'cruz'])
print(filter_only_english_trends(trending_hashtags()))