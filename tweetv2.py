import tweepy
import subprocess

# 認証
api_key = subprocess.run(['sed', '-n', '2P', 'setting.txt'],capture_output=True,text=True).stdout.replace("\n", "")
api_key_secret = subprocess.run(['sed', '-n', '3P', 'setting.txt'],capture_output=True,text=True).stdout.replace("\n", "")
access_token = subprocess.run(['sed', '-n', '4P', 'setting.txt'],capture_output=True,text=True).stdout.replace("\n", "")
access_token_secret = subprocess.run(['sed', '-n', '5P', 'setting.txt'],capture_output=True,text=True).stdout.replace("\n", "")
TWITTER_ID = subprocess.run(['sed', '-n', '1P', 'setting.txt'],capture_output=True,text=True).stdout.replace("\n", "")

#APIv1.1
auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, access_token, access_token_secret)
api = tweepy.API(auth)

#Tweetidを管理するためのDB名を設定
id_list = 'tweetid.txt'

#ツイートを取得
tweets = tweepy.Cursor(api.search_tweets,q="to:" + TWITTER_ID + " シェル",tweet_mode='extended',include_entities=True,result_type='recent',lang='ja').items(30)  # 取得件数

#ツイートを見つけた時の処理
for tweet in tweets:
 f = open(id_list, 'r')
 if str(tweet.id) not in str(f.read()): #テキストに含まれるか確認します
  f = open(id_list, 'a')
  f.write(str(tweet.id) + '\n')
  f.close()
  #以下に処理を記述
  if 'シェル' in tweet.full_text:
   current_time = subprocess.run(['bash' , 'commandstart.sh' , tweet.full_text], stdout=subprocess.PIPE, text=True)
   api.update_status('@%s %s' % (tweet.user.screen_name, current_time.stdout.strip()) , in_reply_to_status_id = tweet.id)
  else:
   print("このリプライは返信対象ではないためスキップします")
   #print(tweet.user.screen_name)
 else:
  f.close()
