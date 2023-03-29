#!/bin/sh

#[twitterID]にTwitterアカウントのIDを入れてください(例:sed -e 's/@Chromium_Linux//g')

account=$(echo -n @ && sed -n 1P setting.txt)

str1=$( echo "$1" | sed -e 's/シェル//g' | sed -e 's/'$account'//g' | tr -d '\n' | sed -e 's/  //g')

str2=$(eval timeout 4 chroot --userspec=test ../chroot $str1 2>&1)

echo "$str2" | sed 's/ //g' | perl -pe 's/\n//g' | cut -c 1-139
