from flask import Flask,render_template,request,redirect,url_for
import sys
import sqlite3 as sql
app=Flask(__name__)

import tweepy
 
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import *

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/Tweets',methods=['POST','GET'])
def Tweets():
    if request.method=='POST':
        USER=request.form['USER']
        ACCESS_TOKEN=request.form['ACCESS_TOKEN']
        ACCESS_SECRET=request.form['ACCESS_SECRET']
        CONSUMER_KEY=request.form['CONSUMER_KEY']
        CONSUMER_SECRET=request.form['CONSUMER_SECRET']

        oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
        api = tweepy.API(auth)

        # user = api.me()
 
        # print('Name: ' + user.name)
        # print('Location: ' + user.location)
        # print('Friends: ' + str(user.friends_count))

        # Initiate the connection to Twitter Streaming API
        twitter_stream = TwitterStream(auth=oauth)
        twitter_api =Twitter(auth=oauth)

        # Get a sample of the public data following through Twitter
        # iterator = twitter_stream.statuses.sample()
        #twitter_userstream = TwitterStream(auth=oauth, domain='userstream.twitter.com')
        #user="RahulGandi"
        # iterator = twitter_stream.statuses.user_timeline(user_id="3258524467")
        iterator = twitter_api.statuses.home_timeline()
        #iterator = api.home_timeline()
        # Print each tweet in the stream to the screen 
        # Here we set it to stop after getting 1000 tweets. 
        # You don't have to set it to stop, but can continue running 
        # the Twitter API to collect data for days or even longer.
        tweets_filename = 'testnew.json'
        tweets_file = open(tweets_filename,"w") 
        tweet_count = 5
        for tweet in iterator:
            tweet_count -= 1
            data=json.dumps(tweet)
            tweets_file.write(data)
            tweets_file.write("\n") 

               
            if tweet_count <= 0:
                break 

        # Import the necessary package to process data in JSON format
        import sqlite3 as sql
        import re
        def extract_link(text):
            regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
            match = re.search(regex, text)
            if match:
                return match.group()
            return ''

        # We use the file saved from last step as example
        tweets_filename = 'testnew.json'
        tweets_file = open(tweets_filename, "r")
        con=sql.connect("Twitter_database.db")
        con.execute("DROP TABLE MyTweets")
        con.execute("CREATE TABLE MyTweets(UserID TEXT,TweetID TEXT,TweetTime TEXT,Urls TEXT)")
        for line in tweets_file:
            try:
                cur=con.cursor()
                # Read in one line of the file, convert it into a json object 
                tweet = json.loads(line.strip())
                if 'text' in tweet: # only messages contains 'text' field is a tweet
                    t_id = tweet['id']
                    t_ct = tweet['created_at']
                    t_text = extract_link(tweet['text'])
                    if(t_text==''):
                        continue
                    t_uid = tweet['user']['id']
                    #q1="INSERT INTO MyTweets(UserID,TweetID,TweetTime,Urls) VALUES(\'"+str(t_uid)+"\',\'"+str(t_idt)+"\',\'"+str(t_ct)+"\',\'"+str(t_text)+"\')"
                    q1="INSERT INTO MyTweets(UserID,TweetID,TweetTime,Urls) values (\'" + str(t_uid) + "\',\'" + str(t_id) + "\',\'" + str(t_ct) +"\',\'" + str(t_text) + "\')"
                    #print(q1)
                    cur.execute(q1)
                    con.commit()

            except:
                # read in a line is not in JSON format (sometimes error occured)
                continue
        tweets_file.close()
        con.row_factory=sql.Row
        cur=con.cursor()
        cur.execute("SELECT * FROM MyTweets")
        rows=cur.fetchall()
        return render_template("listTweets.html",rows=rows)
        con.close()

if __name__=="__main__":
    app.run(debug=True) 