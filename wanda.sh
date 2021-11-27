#!/data/data/com.termux/files/usr/bin/bash

source="unsplash"
query=""
home="false"
lock="false"
version="lite-0.1"

usage() {
  echo "wanda ($version)"
  echo "Usage:"
  echo "  wanda [-s source] [-t search term] [-o] [-l] [-h]"
  echo "  -s  source      unsplash,wallhaven,reddit,local"
  echo "  -t  t           search term."
  echo "  -o  homescreen  set wallpaper on homescreen"
  echo "  -l  lockscreen  set wallpaper on lockscreen"
  echo "  -h  help        this help message"
  echo ""
  echo "Example:"
  echo "  wanda -s wallhaven -t mountain -ol"
  echo "  wanda -s local -t folder/path -o"
  echo ""
  echo "Tips:"
  echo "* None of the parameters are mandatory. Default source is unsplash."
  echo "* Multiple search terms are possible on unsplash and wallhaven using ','"
}

setwp() {
  if [ "$home" = "false" ] && [ "$lock" = "false" ]; then
    termux-wallpaper -u "$1"
  fi
  if [ "$home" = "true" ]; then
    termux-wallpaper -u "$1"
  fi
  if [ "$lock" = "true" ]; then
    termux-wallpaper -lu "$1"
  fi
}

while getopts ':s:t:olh' flag; do
  case "${flag}" in
  s) source="${OPTARG}" ;;
  t) query="${OPTARG}" ;;
  o) home="true" ;;
  l) lock="true" ;;
  h)
    usage
    exit 0
    ;;
  :)
    echo "The $OPTARG option requires an argument."
    usage
    exit 1
    ;;
  \?)
    echo "$OPTARG is not a valid option."
    usage
    exit 1
    ;;
  esac
done

case $source in
wallhaven | wh)
  res=$(curl -s "https://wallhaven.cc/api/v1/search?q=$query&ratios=$ratio&sorting=random")
  url=$(echo "$res" | jq --raw-output ".data[0].path")
  setwp $url
  ;;
unsplash | us)
  res="https://source.unsplash.com/random/1440x2560/?$query"
  url=$(curl -Ls -o /dev/null -w %{url_effective} "$res")
  setwp $url
  ;;
reddit | ri)
  posts=100
  api="https://old.reddit.com/r/MobileWallpaper/search.json?q=$query&restrict_sr=on&limit=$posts"
  res=$(curl -s -A "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0" "$api")
  rand=$(shuf -i 0-$posts -n 1)
  url=$(echo "$res" | jq --raw-output ".data.children[$rand].data.url")
  while [[ $url == *"/gallery/"* ]]; do
    rand=$(shuf -i 0-$posts -n 1)
    url=$(echo "$res" | jq --raw-output ".data.children[$rand].data.url")
  done
  setwp $url
  ;;
local | lc)
  filepath=$(find "$HOME/storage/shared/$query" -type f -exec file --mime-type {} \+ | awk -F: '{if ($2 ~/image\//) print $1}' | shuf -n 1)
  if [ "$home" = "false" ] && [ "$lock" = "false" ]; then
    termux-wallpaper -f "$filepath"
  fi
  if [ "$home" = "true" ]; then
    termux-wallpaper -f "$filepath"
  fi
  if [ "$lock" = "true" ]; then
    termux-wallpaper -lf "$filepath"
  fi
  ;;
esac
