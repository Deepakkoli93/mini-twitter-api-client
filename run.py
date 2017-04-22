#!/usr/bin/python

import os
from flask import Flask, render_template, request
from TwitterApiClient.api_client import api_client


app = Flask(__name__)

"""
This is the landing page. Only a form is displayed here with pre-filled input values.
"""
@app.route("/")
def index():
	hashtag = "#custserv"
	min_retweets = 1
	return render_template("display_tweets.html", hashtag = hashtag, min_retweets = min_retweets)


"""
This route matches when a post request is sent after form submission.
The post request contains the required hashtag and the minimum number
of retweets.
"""
@app.route("/", methods=["POST"])
def display_tweets():
	twitter_client = api_client()
	hashtag = request.form["hashtag"]
	min_retweets = int(request.form["min_retweets"])
	tweets = twitter_client._fetch_tweets(hashtag, min_retweets)
	message = ""
	tweets_text = []
	if len(tweets) <= 0:
		message = "No tweets found matching the criteria"
		return render_template("display_tweets.html", message=message, tweets=tweets_text)
	tweets_text = [(tweet["text"].encode("utf-8"), tweet["id_str"], tweet["user"]["screen_name"]) 
	for tweet in tweets]
	return render_template("display_tweets.html", message=message, tweets=tweets_text, 
		hashtag=hashtag, min_retweets=min_retweets)
 
"""
This is the driver method. It starts the flask application and starts serving requests.
"""
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	# port = 1234
	app.run(host="0.0.0.0", port=port)