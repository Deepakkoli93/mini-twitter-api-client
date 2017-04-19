#!/usr/bin/python

import base64
import requests
import logging
import os
import ConfigParser

logger = logging.getLogger(__name__)
logging.basicConfig()

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configuration.ini")
config = ConfigParser.ConfigParser()
config.read(config_path)
CONSUMER_KEY = config.get("twitter api client", "CONSUMER_KEY")
BASE_URI = config.get("twitter api client", "BASE_URI")
CONSUMER_SECRET = config.get("twitter api client", "CONSUMER_SECRET")


class Twitter_api(object):

	def __init__(self):
		"""
		This will store the bearer token required to authenticate other api calls
		"""
		self.bearer_token = ""

	"""
	Fetches the bearer token required to authenticate other api calls and stores
	it in self.bearer_token
	@param: no parameters
	@return: void
	@raise: Exception if the call does not return 200 response code
	"""
	def _fetch_bearer_token(self):
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
	"""
	def fetch_tweets(self, hashtag):
		self._fetch_bearer_token()
		resource_path = "/1.1/search/tweets.json"
		url = "https://" + BASE_URI + resource_path
		headers = {"Authorization": self.bearer_token}
		payload = {"q" : hashtag}
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
				if tweet["retweet_count"] > 0:
					print(tweet["text"])
					filtered_tweets.append(tweet)
			return filtered_tweets
		else:
			raise Exception("Status code for fetch tweets call {}".format(response.status_code))


if __name__ == "__main__":
	api_client = Twitter_api()
	api_client.fetch_tweets("#custerv")
