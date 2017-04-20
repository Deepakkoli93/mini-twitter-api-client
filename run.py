import os
from flask import Flask, render_template, request
from TwitterApiClient.api_client import api_client


app = Flask(__name__)
 
@app.route("/")
def index():
	return render_template("display_tweets.html")


@app.route("/", methods=["POST"])
def display_tweets():
	# from TwitterApiClient.api_client import api_client
	twitter_client = api_client()
	tweets = twitter_client._fetch_tweets(request.form["hashtag"], int(request.form["min_retweets"]))
	message = ""
	tweets_text = []
	if len(tweets) <= 0:
		message = "No tweets found matching the criteria"
		return render_template("display_tweets.html", message=message, tweets=tweets_text)
	tweets_text = [tweet["text"].encode("utf-8") for tweet in tweets]
	return render_template("display_tweets.html", message=message, tweets=tweets_text)
 
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	# port = 1234
	app.run(host="0.0.0.0", port=port)