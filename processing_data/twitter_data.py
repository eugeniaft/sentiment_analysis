import requests
from bs4 import BeautifulSoup
from requests_oauthlib import OAuth1
import re

def auth_credentials(app_key,
                     app_secret,
                     oauth_token,
                     oauth_token_secret):

    # Creating an OAuth Client connection
    auth = OAuth1 (app_key,
                   app_secret,
                   oauth_token,
                   oauth_token_secret)

    return auth


def tweet_query(q, n_tweets, lang, result_type, auth):

    # url from twitter API
    url_rest = "https://api.twitter.com/1.1/search/tweets.json"
    params = {'q': q, 'count': n_tweets, 'lang': lang,  'result_type': result_type}
    results = requests.get(url_rest, params=params, auth=auth)

    return results.json()


def get_tweet_data(tweet):

    tweet_data = {}

    tweet_data['tweet'] = BeautifulSoup(tweet['text'], "html.parser").get_text()
    tweet_data['tweet_language'] = tweet['metadata']['iso_language_code']
    tweet_data['source'] = re.search('rel="nofollow">(.*)</a>', tweet['source']).group(1)
    tweet_data['geo'] = tweet['geo']
    tweet_data['retweet_count'] = tweet['retweet_count']
    tweet_data['favorite_count'] = tweet['favorite_count']
    tweet_data['favorited'] = tweet['favorited']
    tweet_data['retweeted'] = tweet['retweeted']

    tweet_user = tweet['user']
    tweet_data['user_id'] = tweet_user['id']
    tweet_data['username'] = tweet_user['name']
    tweet_data['user_screename'] = tweet_user['screen_name']
    tweet_data['user_location'] = tweet_user['location']
    tweet_data['followers_count'] = tweet_user['followers_count']
    tweet_data['friends_count'] = tweet_user['friends_count']
    tweet_data['listed_count'] = tweet_user['listed_count']
    tweet_data['created_at'] = tweet_user['created_at']
    tweet_data['statuses_count'] = tweet_user['statuses_count']
    tweet_data['language'] = tweet_user['lang']

    return tweet_data
