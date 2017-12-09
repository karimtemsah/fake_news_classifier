import time
import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

def filter_tweets(tweet):
    json_tweet = json.loads(tweet)
    if 'lang' in json_tweet.keys():  # When the lang key was not present it caused issues
        if json_tweet['lang'] == 'en':
            return True  # filter() requires a Boolean value
    return False


def map_tweets(tweet):
    json_tweet = json.loads(tweet)
    if 'text' in json_tweet.keys():
        return json_tweet['text']
    return None


sc = SparkContext("local[2]", "Simple App")
ssc = StreamingContext(sc, 10)
lines = ssc.socketTextStream("127.0.0.1", 5555)
#lines.foreachRDD(lambda rdd: rdd.filter(filter_tweets).coalesce(1).saveAsTextFile("./tweets/%f" % time.time()))
lines.foreachRDD(lambda rdd: rdd.map(map_tweets).coalesce(1).saveAsTextFile("./tweets/%f" % time.time()))
ssc.start()
ssc.awaitTermination()