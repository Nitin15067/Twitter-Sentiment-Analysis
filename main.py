import settings
import query_handler, twitter_streamer

if __name__== "__main__":

	queryHandler = query_handler.QueryHandler(settings.TWITTER_IDS_FILENAME)
	twitter_ids = queryHandler.get_twitter_ids()
	print(twitter_ids)

	twitterStreamer = twitter_streamer.TwitterStreamer(twitter_ids)
	twitterStreamer.stream_tweets()