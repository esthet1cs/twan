# -*- coding: utf-8 -*-

import tweepy
import json
import os

# authentication
################

# read credentials
twan_dir = os.path.expanduser('~') + '/.twan/'

with open(twan_dir + 'credentials', 'r') as f:
    credentials = [line.strip() for line in f if line.strip() != '']    # read the credentials line by line

creds = {}                                      # initialize a dictionary for storing the credentials
for cred in credentials:                        # iterate over the four entries
    cred = cred.split('=')                      # split the line into name and value
    creds[cred[0].strip()] = cred[1].strip()    # add it to the credentials store


def authenticate(consumer_key, consumer_secret, access_token, access_token_secret):
    '''
    authenticates with the necessary credentials, returns the shortened api
    '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api

api = authenticate(creds['consumer_key'], creds['consumer_secret'], creds['access_token'], creds['access_token_secret'])


# get all tweets from the user and print them
def getAllTweets():
    '''
    gets all tweets and prints them
    '''
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

def getMyTweets(numberOfTweets):
    '''
    gets the specified number of tweets and prints them
    '''
    tweets = []
    for status in tweepy.Cursor(api.home_timeline).items(numberOfTweets):
        tweets.append(status.text)
    return tweets 

### search ###

def twitSearch(keyword, numberOfTweets):
    '''
    makes a search on twitter, returns a list with the json-data from the twitter api
    '''
    tweets = []
    data = tweepy.Cursor(api.search, q=keyword, tweet_mode='extended').items(numberOfTweets)
    for tweet in data:
        tweets.append(json.loads(json.dumps(tweet._json)))
    return tweets

def twitSearchAndSave(keyword, numberOfTweets, datafile):
    '''
    makes a search on twitter, returns a list with the json-data from the twitter api and saves the data in a given datafile
    '''
    tweets = []
    data = tweepy.Cursor(api.search, q=keyword, tweet_mode='extended').items(numberOfTweets)
    with open(datafile, 'w') as myfile:
        for tweet in data:
            tweets.append(json.loads(json.dumps(tweet._json)))
            myfile.write(json.dumps(tweet._json))
            myfile.write("\n")
    return tweets

### get thread ###

# suppose we have one tweet and want to reconstruct the whole thread that it's part of
# get the upper part of the tree (only the thread that this tweet is a part of (keine nebenäste)
# get all replies to the tweet down to the end of the tree that our tweet is the base node of
    # get replies to one tweet
    # get the replies to these replies etc. 

# get the upper part of the tree (only the thread that this tweet is a part of (keine nebenäste)
def thread_up(tweet_id):
    '''
    loads all tweets in a thread that are above the given tweet (but not the whole tree, only the thread that leads to this particular tweet)
    returns the thread as a nested dictionary
    '''

### get contacts ###

def getFollowers(ID, user_id = False):
    '''
    get the user_ids of all followers of a single user, either for her user_id or her screen name. If stated explicitly (boolean), the search will explicitly send the user_id, otherwise it's ID (can be screen_name or user_id);
    returns a list with the user_ids of all followers
    '''
    if user_id:     # if we have a screen name and no ID, get the stuff using the screen-name
        followers = limit_handled(tweepy.Cursor(api.followers_ids, user_id = ID).items())
    else:
        followers = limit_handled(tweepy.Cursor(api.followers_ids, id = ID).items())

    followerIDs = []
    for follower in followers:
        followerIDs.append(follower)
    if not followerIDs:                 # if we don't have any followers, mark that too so we know we have processed this user already.
        followerIDs.append('NaN')
    return followerIDs

def getFriends(ID, user_id=False):
    '''
    get the IDs of all friends of a single user, using the api id (can be screen-name or user_id), force user_id for disambiguation
    returns a list with the users friends
    '''
    if not user_id: 
        friends = limit_handled(tweepy.Cursor(api.friends_ids, id = ID).items())
    elif user_id:
        friends = limit_handled(tweepy.Cursor(api.friends_ids, user_id = ID).items())
    friendIDs = []
    for friend in friends:
        friendIDs.append(friend)
    if not friendIDs:
        friendIDs.append('NaN')
    return friendIDs

def getContacts(ID, user_id=False):
    '''
    get all contacts of a user (followers and friends) and return two lists
    '''
    return getFollowers(ID, user_id), getFriends(ID, user_id)


