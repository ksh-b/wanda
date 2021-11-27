#!/data/data/com.termux/files/usr/bin/bash

source="unsplash"
query=""
home="false"
lock="false"
version=0.2

usage() {
  echo "wanda (lite-$version)"
  echo "Usage:"
  echo "  wanda [-s source] [-t search term] [-o] [-l] [-h]"
  echo "  -s  source      unsplash,wallhaven,reddit,local"
  echo "  -t  t           search term."
  echo "  -o  homescreen  set wallpaper on homescreen"
  echo "  -l  lockscreen  set wallpaper on lockscreen"
  echo "  -h  help        this help message"
  echo "  -u  update      update wanda"
  echo "  -v  version     current version"
  echo ""
  echo "Examples:"
  echo "  wanda -s wallhaven -t mountain -ol"
  echo "  wanda -s local -t folder/path -o"
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

update () {
  res=$(curl -s curl "https://gitlab.com/api/v4/projects/29639604/repository/files/manifest.json/raw?ref=lite")
  latest_version=$(echo "$res" | jq --raw-output ".version")
  if (( $(echo "$latest_version > $version" | bc -l) )); then
    echo "New version found: $latest_version"
    res=$(curl -s curl "https://gitlab.com/api/v4/projects/29639604/releases/v$latest_version-lite/assets/links")
    link=$(echo "$res" | jq --raw-output ".url")
    binary=$(basename $link)
    echo "Downloading..."
    curl $link -o $binary
    echo "Installing..."
    pkg in "./$binary"
    echo "Cleaning up..."
    rm "$binary"
    wanda -h
  else
    echo "Already latest version ($version)"
  fi
}

while getopts ':s:t:olhuv' flag; do
  case "${flag}" in
  s) source="${OPTARG}" ;;
  t) query="${OPTARG}" ;;
  o) home="true" ;;
  l) lock="true" ;;
  h)
    usage
    exit 0
    ;;
  u)
    update
    exit 0
    ;;
  v)
    echo "wanda (lite-$version)"
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
  res=$(curl -s "https://wallhaven.cc/api/v1/search?q=$query&ratios=portrait&sorting=random")
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
