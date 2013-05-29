"""
some implement of twitter timeline api
Gestalt Lur
2013-05-29
"""
import httplib
import os

from obtain_oauth import get_access_token
from obtain_oauth import get_oauth_header 
from gzip_decode import gzip_decode

def get_tweets( user_name, cnt_num ):

    #read consumer_key and consumer_secret from oauth_key.txt
    access_token = get_access_token()
    #try:
    
    #except Exception as e:
    #    print e.value
        #TODO raise a GetTweetError here
    host = 'api.twitter.com'
    url = '/1.1/statuses/user_timeline.json?count=' + str(cnt_num) + '&screen_name=' + user_name

    connect = httplib.HTTPSConnection( host )
    #write headers
    connect.putrequest("GET", url )
    connect.putheader("Host", host )
    connect.putheader("User-Agent", "Scarlet Poppy Anarchistic")
    connect.putheader("Authorization", "Bearer %s" % access_token )   
    #connect.putheader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
    #connect.putheader("Content-Length", "%d" % len( msg ))
    connect.putheader("Accept-Encoding", "gzip" )
    connect.endheaders()

    twitter_response = connect.getresponse()
    #print twitter_response.status

    zipped_tweets = twitter_response.read()

    tweets_entites = gzip_decode( zipped_tweets )

    connect.close()
    
    return tweets_entites

# get follower
def get_follow_list( user_id=None, user_name=None, page=-1 ):

    access_token = get_access_token()

    if ( user_id == None ) and ( user_name == None ):
        return "Must set either user_id or user_name"
    elif ( user_id != None ) and ( user_name != None ):
        return "user_id and user_name can't be used at same time"

    host = 'api.twitter.com'
    if user_name != None:
        url = '/1.1/followers/list.json?cursor=' + str(page) + '&screen_name=' + user_name + '&skip_status=true&include_user_entities=false'
    else:
        url = '/1.1/followers/list.json?cursor=' + str(page) + '&user_id=' + str(user_id) + '&skip_status=true&include_user_entities=false'

    connect = httplib.HTTPSConnection( host )
    #write headers
    connect.putrequest("GET", url )
    connect.putheader("Host", host )
    connect.putheader("User-Agent", "Scarlet Poppy Anarchistic")
    connect.putheader("Authorization", "Bearer %s" % access_token )   
    #connect.putheader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
    #connect.putheader("Content-Length", "%d" % len( msg ))
    connect.putheader("Accept-Encoding", "gzip" )
    connect.endheaders()

    twitter_response = connect.getresponse()
    print twitter_response.status

    zipped_tweets = twitter_response.read()

    follower_entites = gzip_decode( zipped_tweets )

    connect.close()

    return follower_entites

# this function not use a bearer token but a token from dev.twitter.com
# API : user/lookup
def get_user(user_id=None, user_name=None ):

    if ( user_id == None ) and ( user_name == None ):
        return "Must set either user_id or user_name"
    elif ( user_id != None ) and ( user_name != None ):
        return "user_id and user_name can't be used at same time"

    host = 'api.twitter.com'
    if user_name != None:
        url = '/1/users/lookup.json?screen_name=' + user_name + '&include_entities=true'
    else:
        url = '/1/users/lookup.json?user_id=' + str( user_id ) + '&include_entities=true'

    oauth_header = get_oauth_header( "GET", host, url )

    connect = httplib.HTTPSConnection( host )
    #write headers
    connect.putrequest("GET", url )
    connect.putheader("Host", host )
    connect.putheader("User-Agent", "Scarlet Poppy Anarchistic")
    connect.putheader("Authorization", oauth_header )   
    #connect.putheader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
    #connect.putheader("Content-Length", "%d" % len( msg ))
    connect.putheader("Accept-Encoding", "gzip" )
    connect.endheaders()

    twitter_response = connect.getresponse()
    print twitter_response.status

    zipped_tweets = twitter_response.read()

    user_entites = gzip_decode( zipped_tweets )

    connect.close()

    return user_entites
