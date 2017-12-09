from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json


class TweetsListener(StreamListener):

    def __init__(self, csocket):
        self.client_socket = csocket

    def on_data(self, data):
        try:
            print(data.split('\n'))
            self.client_socket.send(data.encode())
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
    def on_error(self, status):
        print(status)
        return True


def read_credentials():
    with open("credentials.json", 'r') as input:
        data = json.load(input)
        return data["access_token"], data["access_token_secret"],\
            data["consumer_key"], data["consumer_secret"]


def sendData(c_socket):
    access_token, access_secret, consumer_key, consumer_secret = read_credentials()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=['news'])


if __name__ == "__main__":
    s = socket.socket()         # Create a socket object
    host = "127.0.0.1"     # Get local machine name
    port = 5555                 # Reserve a port for your service.
    s.bind((host, port))        # Bind to the port

    print("Listening on port: %s" % str(port))

    s.listen(5)                 # Now wait for client connection.
    c, addr = s.accept()        # Establish connection with client.
    print(c)
    print("Received request from: " + str(addr))

    sendData(c)

