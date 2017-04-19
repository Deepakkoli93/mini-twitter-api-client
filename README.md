A mini twitter api client
==

This is a python implementation of a twitter api client which can fetch tweets based on :
1. a hashtag present in the tweet, and
2. the number of times the tweet has been retweeted

Usage
==
Clone the repo using
	
	git clone https://github.com/Deepakkoli93/mini-twitter-api-client.git
	
Install the dependencies

	pip install -r requirements.txt

If the above does not work then install the requests module using
	
	pip install requests

Edit the _configuration.ini_ file to place your twitter app's _consumer key_ and _consumer secret_.  I have provided a sample key and secret so you can leave the _configuration.ini_ as it is.

Go to the repo's root directory and open a python shell. To fetch tweets, run the following commands
	
	from TwitterApiClient.api_client import api_client
	api_client = api_client()
	api_client.display_tweets("#custserv", 1)

This will fetch and disaply the tweets which have #custserv hashtag present in them and have been retweeted at least once.

_display_tweets_ can accept two optional parameters. As shown in the above example, the minimum number of retweets required is 1 but that parameter can be skipped, it defaults to 1

It can take another parameter which is a file name (defaults to "tweets.txt"). The client will only print the text part of the tweets on the terminal and a complete dump of the tweets with all their fields will be written to "tweets.txt" (or a filename if provided). 
The following example fetches tweets which have #custserv hashtag in them and have atleast 100 retweets. The complete details of these tweets will then be written into _popular_tweets.txt_ 
	
	api_client.display_tweets("#ipl", 100, "popular_tweets.txt")

 _sample.py_ contains a sample call

The module contains the following basic function:
* _fetch_bearer_token - fetches the authentication bearer token required to authenticate other api calls and saves it
* _fetch_tweets - uses the bearer token to make a call to twitter's search api to fetch the tweets containg the required hashtag. It then filters those tweets according to the minimum number of tweets required and returns them
* display_tweets - This is the function that the user calls. It uses _fetch_tweets to get the required tweets. Then it  displays them on the terminal and writes them to a file.



