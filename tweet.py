import tweepy
import re
import subprocess
import json

API_KEY = subprocess.run(['sed', '-n', '2P', 'setting.txt'],capture_output=True,text=True).stdout.replace("\n", "")
API_SECRET = subprocess.run(['sed', '-n', '3P', 'setting.txt'],capture_output=True,text=True).stdout.replace("\n", "")
ACCESS_TOKEN = subprocess.run(['sed', '-n', '4P', 'setting.txt'],capture_output=True,text=True).stdout.replace("\n", "")
ACCESS_TOKEN_SECRET = subprocess.run(['sed', '-n', '5P', 'setting.txt'],capture_output=True,text=True).stdout.replace("\n", "")
BEARER_TOKEN = subprocess.run(['sed', '-n', '6P', 'setting.txt'],capture_output=True,text=True).stdout.replace("\n", "")
TWITTER_ID = subprocess.run(['sed', '-n', '1P', 'setting.txt'],capture_output=True,text=True).stdout.replace("\n", "")

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
   current_time = subprocess.run(['bash' , 'commandstart.sh' , name], stdout=subprocess.PIPE, text=True)
   print(current_time.stdout.strip())
   Client.create_tweet(text=current_time.stdout.strip(),in_reply_to_tweet_id=tweet_id)
  else:
    print("このリプライは返信対象ではないためスキップします")

def main():
    printer = IDPrinter(BEARER_TOKEN)
    #printer.add_rules(tweepy.StreamRule(TWITTER_ID))
    printer.add_rules(tweepy.StreamRule("to:" + (TWITTER_ID) + "シェル"))
    printer.filter()

if __name__ == '__main__':
    main()
