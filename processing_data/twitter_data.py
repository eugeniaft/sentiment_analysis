import requests
from requests_oauthlib import OAuth1
import os
import json


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


def tweet_query(q, n_tweets, until, lang, result_type, auth):
    '''
    possible values for result_type: mixed, recent, popular
    '''

    # url from twitter API
    url_rest = "https://api.twitter.com/1.1/search/tweets.json"
    params = {'q': q, 'count': n_tweets, 'until':until, 'lang': lang,  'result_type': result_type}
    results = requests.get(url_rest, params=params, auth=auth)

    return results.json()


def save_tweet_data(path, filename, tweets):
    with open(os.path.join(path, filename), 'w+') as f:
        json.dump(tweets, f)


def parse_tweet(tweet):

    tvals = ['created_at',
             'id_str',
             'text',
             'source',
             'in_reply_to_status_id',
             'in_reply_to_status_id_str',
             'in_reply_to_user_id',
             'in_reply_to_user_id_str',
             'in_reply_to_screen_name',
             'geo',
             'coordinates',
             'place',
             'contributors',
             'is_quote_status',
             'retweet_count',
             'favorite_count',
             'favorited',
             'retweeted',
             'possibly_sensitive',
             'lang'
            ]
    t_dt = {k: tweet[k] for k in tweet.keys() if k in tvals}
    
    e_dt = tweet['entities']
    t_dt['hashtags'] = ';'.join([hs['text'] for hs in e_dt['hashtags']])
    t_dt['user_mentions'] = ';'.join([um['screen_name'] for um in e_dt['user_mentions']])
    t_dt['user_mentions_ids'] = ';'.join([umi['id_str'] for umi in e_dt['user_mentions']])

    user = ['id_str', 
            'screen_name', 
            'location', 
            'description', 
            'followers_count', 
            'friends_count', 
            'listed_count', 
            'created_at', 
            'verified']
    u_dt = {'user_' + k: tweet['user'][k] for k in user}
    t_dt.update(u_dt)
    
    return t_dt


def get_tweet_data(tweets):
    for tweet in tweets:
        yield parse_tweet(tweet)  
