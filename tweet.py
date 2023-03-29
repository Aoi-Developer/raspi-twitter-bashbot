import tweepy
import os
import re
import json

API_KEY = os.popen('sed -n 2P setting.txt').readline().strip()
API_SECRET = os.popen('sed -n 3P setting.txt').readline().strip()
ACCESS_TOKEN = os.popen('sed -n 4P setting.txt').readline().strip()
ACCESS_TOKEN_SECRET = os.popen('sed -n 5P setting.txt').readline().strip()
BEARER_TOKEN = os.popen('sed -n 6P setting.txt').readline().strip()
TWITTER_ID = os.popen('sed -n 1P setting.txt').readline().strip()

Client = tweepy.Client(bearer_token=BEARER_TOKEN, consumer_key=API_KEY, consumer_secret=API_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

class IDPrinter(tweepy.StreamingClient):
 def on_tweet(self, tweet):
  print(tweet.text)
  print(tweet.id)
  name = (tweet.text)
  tweet_id = (tweet.id)

  if 'シェル' in name:
   cmdcode = 'sh commandstart.sh ' +  '"' + (name) + '"'
   current_time = os.popen(cmdcode).readline().strip()
   print(current_time)
   Client.create_tweet(text=current_time,in_reply_to_tweet_id=tweet_id)
  else:
    print("このリプライは返信対象ではないためスキップします")

def main():
    printer = IDPrinter(BEARER_TOKEN)
    #printer.add_rules(tweepy.StreamRule(TWITTER_ID))
    printer.add_rules(tweepy.StreamRule("to:" + (TWITTER_ID) + "シェル"))
    printer.filter()
    
if __name__ == '__main__':
    main()
