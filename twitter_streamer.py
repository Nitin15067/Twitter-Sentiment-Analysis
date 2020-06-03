from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream, API, Cursor
import json
import credentials
from textblob import TextBlob
import re

class TwitterAuthenticator():

	def __init__(self):
		pass

	def authenticate_twitter_app(self):
		auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
		auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)
		return auth

class TwitterStreamer():

	def __init__(self, twitter_ids):
		self.twitter_authenticator = TwitterAuthenticator()
		self.twitter_ids = twitter_ids

	def stream_tweets(self):
		listener = TwitterListener(self.twitter_ids)
		auth = self.twitter_authenticator.authenticate_twitter_app()		
		stream = Stream(auth, listener)

		stream.filter(follow=self.twitter_ids)

class TwitterListener(StreamListener):

	def __init__(self, twitter_ids):
		self.twitter_ids = twitter_ids

	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def analyze_sentiment(self, tweet):
		analysis = TextBlob(self.clean_tweet(tweet))
		return analysis.sentiment.polarity
		# if analysis.sentiment.polarity > 0:
		# 	return 1
		# elif analysis.sentiment.polarity == 0:
		# 	return 0
		# else:
		# 	return -1

	def on_data(self, data):
		try:
			tweet = json.loads(data)

			if tweet['user']['id_str'] in self.twitter_ids:
				tweet_data = {
					'tweet_id': None,
					'text': None,
					'created_at': None,
					'tags': None,
					'twitter_handle': None
				}

				tweet_text = None
				try:
					tweet_text = tweet['extended_tweet']['full_text']
				except:
					tweet_text = tweet['text']

				sentiment_analysis = self.analyze_sentiment(tweet_text) 
				
				tweet_data['tweet_id'] = str(tweet['id'])
				tweet_data['text'] = tweet_text
				tweet_data['created_at'] = str(tweet['created_at'])
				tweet_data['twitter_handle'] = tweet['user']['id_str']
				tweet_data['sentiment'] = sentiment_analysis

				print(tweet_data)

		except Exception as e:
			 print("Error on receiving tweet data: " + str(e))
		
		return True

	def on_error(self, status):
		if status ==420:
			return False