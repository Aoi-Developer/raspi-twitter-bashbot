#!/bin/sh
echo "#TwShell Ver2.0"
#OSをチェックします
if [ "$(uname)" == 'Darwin' ]; then
  echo "このOSでは実行できません"
  exit 1
fi

if [ "$1" = "-h" ]; then
  echo "twitterのPOSIXコマンドbotを簡単に構築できます"
  echo "対話形式でセットアップできるため初心者でも比較的簡単に使用できます"
  echo "Botが異常停止した際自動復帰するため、root権限で実行することをお勧めします"
  echo
  echo "Usage: sudo bash twshell.sh [option]"
  echo
  echo "  [-h] ヘルプを表示"
  echo "  [-r]botの環境を削除する"
  echo "  [指定なし]対話形式のセットアップをする"
  echo
  exit
fi

if [ "$1" = "-r" ]; then
  sudo rm -r twshell
  echo "構築した環境を削除しました"
  exit
fi


if [ -f twshell/raspi-twitter-bashbot-main/setting.txt ]; then
  echo
else
  if [ $# = 5 ]; then
    apikey=$2
    apiselect=$3
    accesstoken=$4
    accesstokenselect=$5
    accountname=$1
  else
    echo -n "Twitterの開発者アカウントを取得していてAPI及びトークンが確認できる状態ですか？ [y/N]: "
    read ANS

    case $ANS in
      [Yy]* )
        # ここに「Yes」の時の処理を書く
        echo "対話形式のセットアップを開始します"
        echo
        echo "あなたのユーザIDを入力してください(先頭の@は入力しないでください)"
        echo -n "ユーザー名:"
        read accountname
        echo
        echo "API Keyを入力してください"
        echo -n "API Key:"
        read apikey
        echo
        echo "API Select Keyを入力してください"
        echo -n "API Select Key:"
        read apiselect
        echo
        echo "Access Tokenを入力してください"
        echo -n "Access Token:"
        read accesstoken
        echo
        echo "Access Token Selectを入力してください"
        echo -n "Access Token Select:"
        read accesstokenselect
        echo "環境の構築を始めます。途中でパスワードが求められることがあります"
        ;;
      * )
        # ここに「No」の時の処理を書く
        echo "以下URLにアクセスして開発者アカウントを取得してください"
        echo ”https://developer.twitter.com/en”
        exit 1
        ;;
    esac
  fi
fi
#依存関係を確認します
sudo which debootstrap >/dev/null 2>&1 && which pip3 >/dev/null 2>&1 && which curl >/dev/null 2>&1 && which unzip >/dev/null 2>&1 && which jq >/dev/null 2>&1
if [ $? -ne 0 ] ; then
  sudo apt install debootstrap python3-pip curl jq unzip -y
fi

sudo pip3 show tweepy >/dev/null 2>&1
if [ $? -ne 0 ] ; then
  sudo pip3 install tweepy
fi

#ディレクトリ作成
if [ -d twshell ]; then
  cd twshell
else
  mkdir twshell
  cd twshell
fi

if [ -d chroot ]; then
  cd chroot
else
  mkdir chroot
  cd chroot
fi

#安全な環境を構築
ls etc/os-release >/dev/null 2>&1
if [ $? -ne 0 ] ; then
  sudo debootstrap buster `pwd` http://ftp.jp.debian.org/debian
  sudo chroot `pwd` apt update
  sudo chroot `pwd` apt install unzip zip neofetch git sl sudo wget curl jq golang make g++ gcc -y
  sudo chroot `pwd` useradd test
  sudo chroot `pwd` mkdir /home/test
  sudo chroot `pwd` chmod -R 777 /home/test
  sudo chroot `pwd` sudo gpasswd -a test sudo
fi

#Bot用のプログラムが存在するかチェック
cd ../
pwd
if [ -f raspi-twitter-bashbot-main/tweet.py ]; then
  echo
else
  curl -OL "https://github.com/Aoi-Developer/raspi-twitter-bashbot/archive/refs/heads/main.zip"
  unzip main.zip
  rm main.zip
fi

#設定用ファイルの生成
if [ -f raspi-twitter-bashbot-main/setting.txt ]; then
  echo
else
  echo $accountname > raspi-twitter-bashbot-main/setting.txt
  echo $apikey >> raspi-twitter-bashbot-main/setting.txt
  echo $apiselect >> raspi-twitter-bashbot-main/setting.txt
  echo $accesstoken >> raspi-twitter-bashbot-main/setting.txt
  echo $accesstokenselect >> raspi-twitter-bashbot-main/setting.txt
  curl -u $apikey:$apiselect --data 'grant_type=client_credentials' 'https://api.twitter.com/oauth2/token' | jq -r '.access_token' >> raspi-twitter-bashbot-main/setting.txt
fi

#chroot動作のためrootでbot開始
cd raspi-twitter-bashbot-main
echo "Botを起動しました"
while true
do
  sudo python3 tweet.py
  echo "Botを再起動します"
done
