# raspi-twitter-bashbot

Twitter v1.1のStreamAPIは10月に終了したため使えません。(中の人が更新サボってる)  

TwitterでPOSIXコマンドの実行結果を返す簡単なPythonスクリプトです
chroot環境でコマンドが実行されるためメインOSに被害なく実行することができます

![test](Docs/tweet.jpg)

# 依存関係

スクリプト実行時に自動でインストールが実施されるため事前準備は必要ありません  
ラズパイ以外でも使えますが必ずDebian派生のOSで実行してください  

# 実行する前に

Twitterの開発者アカウントを必ず取得してください。セットアップ時にAPIKeyとトークンを入力する必要があります
また2GB以上の空き容量が必要です

# 実行の仕方

main.shを実行するとセットアップがスタートします。  
1度セットアップをすれば次回以降同じコマンドでBotを起動できます  
chrootで実行するためrootアカウントでの実行をお勧めします  

対話形式でセットアップする場合は以下コマンドを使用します(初心者向け)  
```sh
bash <(curl -s https://raw.githubusercontent.com/Aoi-Developer/raspi-twitter-bashbot/main/main.sh)
```
対話形式を使用しないで初期設定を行う場合は引数にユーザIDとAPIKey、トークンを指定することでもセットアップできます

```sh
bash <(curl -s https://raw.githubusercontent.com/Aoi-Developer/raspi-twitter-bashbot/main/main.sh) "ユーザID" "API-Key" "API-Select" "AccessToken" "AccessTokenSelect"
```


もしも不正な操作によりBotが破壊されてしまった場合は以下のコマンドで環境を消去できます  

```sh
bash <(curl -s https://raw.githubusercontent.com/Aoi-Developer/raspi-twitter-bashbot/main/main.sh) -r
```
ヘルプを参照したい場合は-hオプションが使用できます
```sh
bash <(curl -s https://raw.githubusercontent.com/Aoi-Developer/raspi-twitter-bashbot/main/main.sh) -h
```
