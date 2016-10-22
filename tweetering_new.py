""" Streaming twitter API example """

from __future__ import print_function
import sys
import tweepy
import json
import csv
import re
import numpy as np
from ConfigParser import ConfigParser
from nltk.corpus import stopwords

 
class TwitterListener(tweepy.StreamListener):
    """ Twitter stream listener. """
    def __init__(self, api=None):
    	super(TwitterListener, self).__init__()
    	self.num_tweets = 0
	self.list_of_tweets = []

    def on_status(self, status):
    	record = status.text
    	#print(record) #See Tweepy documentation to learn how to access other fields
    	self.num_tweets += 1
    	if self.num_tweets < 10000:
        	self.list_of_tweets.append(record)
        	return True
    	else:
        	return False

    def on_error(self, msg):
        print('Error: %s', msg)

    def on_timeout(self):
        print('timeout : wait for next poll')
        sleep(10)

def get_config():
    """ Get the configuration """
    conf = ConfigParser()
    conf.read('../cfg/sample.cfg')
    return conf

def get_stream():
    config = get_config()
    auth = tweepy.OAuthHandler(config.get('twitter', 'consumer_key'),
                               config.get('twitter', 'consumer_secret'))

    auth.set_access_token(config.get('twitter', 'access_token'),
                          config.get('twitter', 'access_token_secret'))

    listener = TwitterListener()
    stream = tweepy.Stream(auth=auth, listener=listener)
    return stream

def clean_tweets(tweet_list):
    clean_tweet_list = []
    for tweet in tweet_list:
	tweet = re.sub('^RT','',tweet)
	tweet = re.sub('@[a-zA-Z0-9]*:','',tweet)
	tweet = re.sub('\\[a-zA-Z]','',tweet).replace('\u','').replace('\\','').replace('@','').replace('-',' ')
	tweet = re.sub('http.*','',tweet)
	tweet = re.sub('\.+','',tweet)
	tweet = re.sub('[^a-zA-Z0-9-_*.]', ' ', tweet)
	tweet = re.sub('[0-9]','',tweet)
	tweet = ' '.join(tweet.split())
	clean_tweet_list.append(tweet)
    return clean_tweet_list

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: %s <word>" % (sys.argv[0]))
    else:
        word = sys.argv[1]
        stream = get_stream()
        print("Listening to '%s' and '%s' ..." %('#' + word, word))	
    	stream.filter(track=['#' + word, word])
	cleaned_tweets = clean_tweets(stream.listener.list_of_tweets)
	filename = word + '_tweets.txt'
	file = open(filename, 'w+')
	file.write(str(cleaned_tweets))
	file.close()
