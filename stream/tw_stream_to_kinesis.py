#!env python
# -*- coding: utf-8 -*-

import os, sys, time
import boto.kinesis
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

def get_auth():
    consumer_key =        "your_consumer_key"
    consumer_secret =     "your_consumer_secret"
    access_token =        "your_access_token"
    access_token_secret = "your_access_token_secret"
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

class KclListener(StreamListener):

    def __init__(self):
        self.connection = boto.kinesis.connect_to_region('us-east-1')
        super(KclListener,self).__init__()

    def on_status(self, status):
        put_data = self.connection.put_record("aws-kclpy-adcal", status.text, str(status.id))
        # print status.id
        return True

    def on_error(self, status):
        print status

def main():
    stream = Stream(get_auth(), KclListener())
    while True :
        try:
            stream.filter(track=['aws','azure','gcp','softlayer'])
        except Exception as e:
            print 'Error!! {e}.\n'.format(e=e)
            time.sleep(60)
            stream = Stream(get_auth(),KclListener())

if __name__ == '__main__':
    main()
