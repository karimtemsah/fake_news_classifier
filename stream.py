import time
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import pickle
import pandas as pd

model = pickle.load(open('models/naiiveBayes.pkl', 'rb'))
count_vectorizer = pickle.load(open('models/count_vector.pkl', 'rb'))
def filter_tweets(tweet):
    json_tweet = json.loads(tweet)
    if 'lang' in json_tweet.keys():  # When the lang key was not present it caused issues
        if json_tweet['lang'] == 'en':
            return True  # filter() requires a Boolean value
    return False


def map_tweets(tweet):
    json_tweet = json.loads(tweet)
    if 'text' in json_tweet.keys():
        current_tweet = json_tweet['text']
        #print(model.predict(count_vectorizer.transform(current_tweet)))
        return current_tweet, model.predict(count_vectorizer.transform(pd.Series(current_tweet)))
    return None


sc = SparkContext("local[3]", "Simple App")
ssc = StreamingContext(sc, 10)
lines = ssc.socketTextStream("127.0.0.1", 5555)
#lines.foreachRDD(lambda rdd: rdd.filter(filter_tweets).coalesce(1).saveAsTextFile("./tweets/%f" % time.time()))
lines.foreachRDD(lambda rdd: rdd.filter(filter_tweets).map(map_tweets).coalesce(1).saveAsTextFile("./tweets/%f" % time.time()))
ssc.start()
ssc.awaitTermination()