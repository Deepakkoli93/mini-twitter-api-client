#!/usr/bin/python

import base64
import requests
import logging
import os
import ConfigParser

logger = logging.getLogger(__name__)
logging.basicConfig()

config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "configuration.ini")
config = ConfigParser.ConfigParser()
config.read(config_path)
CONSUMER_KEY = config.get("twitter api client", "CONSUMER_KEY")
BASE_URI = config.get("twitter api client", "BASE_URI")
CONSUMER_SECRET = config.get("twitter api client", "CONSUMER_SECRET")


"""
This class defines the twitter api client and contains method to fetch tweets from 
twitter's REST api
"""
class api_client(object):

	def __init__(self):
		"""
		This will store the bearer token required to authenticate other api calls
		"""
		self.bearer_token = ""

	"""
	Fetches the bearer token required to authenticate other api calls and stores
	it in self.bearer_token
	@param: no parameters
	@return: None
	@raise: Exception if the call does not return 200 response code
	"""
	def _fetch_bearer_token(self):
		logger.debug("Fetching the bearer token...")
		resource_path = "/oauth2/token"
		headers = {"Authorization": "Basic " + base64.b64encode(bytes(CONSUMER_KEY+":"+CONSUMER_SECRET))}
		headers["Content-Type"] = "application/x-www-form-urlencoded"
		url = "https://" + BASE_URI + resource_path
		response = requests.post(url, headers = headers, data = {"grant_type": "client_credentials"})
		logger.debug("Response status code of the auth request : " + str(response.status_code))
		if response.status_code == 200:
			logger.debug("Bearer access token: " + response.json()["access_token"])
			self.bearer_token = "Bearer " + response.json()["access_token"]
		else:
			logger.error("Not able to get authentication token")
			raise Exception("Status code for auth call {}".format(response.status_code))

	"""
	Fetches and prints the tweets which contain the given hashtag and have been retweeted
	atleast once
	@param hashtag : the hashtag that should be present in the tweet
	@return: returns a list of tweets
	@raise: Exception if the response of fetch tweets call is not 200
	"""
	def _fetch_tweets(self, hashtag, min_retweets):
		self._fetch_bearer_token()
		resource_path = "/1.1/search/tweets.json"
		url = "https://" + BASE_URI + resource_path
		headers = {"Authorization": self.bearer_token}
		payload = {"q" : hashtag, "count" : 100}
		response = requests.get(url, headers = headers, params=payload)
		logger.debug("Response status of the fetch tweets request : " + str(response.status_code))
		if response.status_code == 200:
			tweets = response.json()["statuses"]
			if len(tweets) <= 0:
				return []
			filtered_tweets = []
			for tweet in tweets:
				if not tweet.has_key("retweet_count"):
					continue
				if tweet["retweet_count"] >= min_retweets:
					filtered_tweets.append(tweet)
			return filtered_tweets
		else:
			raise Exception("Status code for fetch tweets call {}".format(response.status_code))

	"""
	Fetches and prints the relevant tweets's text and prints the detailed tweet data in a file
	@param1 hashtag: the hashtag that should be present in the tweet
	@param2 min_retweets: the tweets must have minimum these many retweets. Defaults to atleast 1 retweet
	@param3 filename: name of the file where tweets will be written. Defaults to tweets.txt
	@return: None
	"""
	def display_tweets(self, hashtag, min_retweets=1, filename="tweets.txt"):
		tweets = self._fetch_tweets(hashtag, min_retweets)
		if len(tweets) <= 0:
			print("No tweets found matching the criteria")
		else:
			print("Fetching tweets with hashtag {} and minimum {} retweets...\n".format(hashtag, min_retweets))
			f = open(filename, 'w')
			for i, tweet in enumerate(tweets):
				print("Tweet {} : {}\n".format(i+1, tweet["text"].encode("utf-8")))
				f.write(str(tweet)+"\n\n")
			f.close()
			print("The tweets above with all their fields have been dumped into {}".format(filename))


if __name__ == "__main__":
	api_client = api_client()
	api_client.display_tweets("#custerv", 1)
