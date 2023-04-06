from requests_oauthlib import OAuth1Session
import urllib.parse
import tweepy

CONSUMER_KEY = "3rJOl1ODzm9yZy63FACdg"
CONSUMER_KEY_SECRET = "5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8"
API_ROOT = "https://api.twitter.com"

session = OAuth1Session(CONSUMER_KEY, CONSUMER_KEY_SECRET)
token_endpoint = API_ROOT + "/oauth/request_token"
response = session.post(token_endpoint, params={"oauth_callback": "oob"})
oauth_token = dict(urllib.parse.parse_qsl(response.text))["oauth_token"]

auth_endpoint = API_ROOT + "/oauth/authenticate"
auth_url = f"{auth_endpoint}?oauth_token={oauth_token}"
print("URLを作成しました。アドレスにアクセスして認証した後、表示されたPINを入力してください")
print(auth_url)
# ユーザにPIN番号を入力させる
oauth_verifier = input("PIN入力: ")

# 手順3
access_token_endpoint = API_ROOT + "/oauth/access_token"
session = OAuth1Session(CONSUMER_KEY, CONSUMER_KEY_SECRET,
                        oauth_token, oauth_verifier)

response = session.post(
    access_token_endpoint,
    params={"oauth_verifier": oauth_verifier},
)

parsed_response = dict(urllib.parse.parse_qsl(response.text))
oauth_token = parsed_response["oauth_token"]
oauth_token_secret = parsed_response["oauth_token_secret"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
auth.set_access_token(oauth_token, oauth_token_secret)
api = tweepy.API(auth)
user = api.verify_credentials()

f = open("setting.txt", mode="w")
f.write(str(user.screen_name) + '\n' + str(CONSUMER_KEY) + '\n' + str(CONSUMER_KEY_SECRET) + '\n' + str(oauth_token) + '\n' + str(oauth_token_secret))
f.close()
print("トークンの取得に成功しました。")
print('id:' + user.screen_name)
print("oauth_token:",oauth_token)
print("oauth_token_secret:",oauth_token_secret)
