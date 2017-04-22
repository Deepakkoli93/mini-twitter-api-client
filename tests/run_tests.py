"""
This modules tests the methods defined in TwitterApiClient
"""
from sys import path
from os.path import dirname
import unittest
# from TwitterApiClient.api_client import api_client


"""
Class to define unit test cases
"""
class TestApiClient(unittest.TestCase):

	"""
	Test if bearer token is fetched properly
	"""
	def test_bearer_token(self):
		self._api_client = api_client()
		self._api_client._fetch_bearer_token()
		assert(self._api_client.bearer_token).startswith("Bearer")


	"""
	Test if every tweet has #custserv and atleast 1 minimum retweet count
	"""
	def test_featch_tweets(self):
		self._api_client = api_client()
		self.tweets = self._api_client._fetch_tweets("#custserv", 1)
		for tweet in self.tweets:
			self.assertGreaterEqual(tweet["retweet_count"], 1)

if __name__ == '__main__':
	path.append(dirname(path[0]))
	from TwitterApiClient.api_client import api_client
	unittest.main()


