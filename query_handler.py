class QueryHandler():

	def __init__(self, twitter_ids_filename):
		self.twitter_ids_filename = twitter_ids_filename

	def get_twitter_ids(self):
		twitter_ids = []

		F = open(self.twitter_ids_filename, "r")

		for line in F:
			twitter_ids.append(line.strip())

		return twitter_ids