#!/usr/bin/python

import base64
import requests
import logging

logger = logging.getLogger(__name__)
BASE_URI = "api.twitter.com"
CONSUMER_KEY = "NqTvP1Q6xGveBuNLPyjA2uBcU"
CONSUMER_SECRET = "8BK8mMOFumxWQV2wWdBEQ9ZDWpVpFK7mIIvkTvmQspOo16tkFD"

class Twitter_api(object):
	def __init__(self):
		self.bearer_token = ""

	def _fetch_bearer_token(self):
		resource_path = "/oauth2/token"
		headers = {"Authorization": "Basic " + base64.b64encode(bytes(CONSUMER_KEY+":"+CONSUMER_SECRET))}
		headers["Content-Type"] = "application/x-www-form-urlencoded"
		url = "https://" + BASE_URI + resource_path
		response = requests.post(url, headers = headers, data = {"grant_type": "client_credentials"})
		# print(response)
		# print(response.text)
		# print(dir(response))
		logger.debug("Respons status code of the auth request :" + response.status_code)
		if response.status_code == 200:
			logger.debug("Bearer access token: " + response.json()["access_token"])
			self.bearer_token = "Bearer " + response.json()["access_token"]
		else:
			logger.error("Not able to get authentication token")

	def fetch_tweets(self):
		self._fetch_bearer_token()
		resource_path = "/1.1/search/tweets.json"
		url = "https://" + BASE_URI + resource_path
		headers = {"Authorization": self.bearer_token}
		payload = {"q" : "#custerv"}
		response = requests.get(url, headers = headers, params=payload)
		r = response.json()["statuses"]

if __name__ == "__main__":
	logging.basicConfig()
	api_client = Twitter_api()
	api_client.fetch_tweets()
