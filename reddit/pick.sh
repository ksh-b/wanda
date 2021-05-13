#!/data/data/com.termux/files/usr/bin/bash
. ./reddit/config
api="https://old.reddit.com/r/${sub}/${sort}.json"
res=$(curl -s $api)
posts=26
rand=$(shuf -i 1-$posts -n 1)
url=$(printf "%s" $res | jq --raw-output ".data.children[$rand].data.url")
echo $url
