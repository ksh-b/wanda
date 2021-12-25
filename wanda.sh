#!/data/data/com.termux/files/usr/bin/bash

source="unsplash"
query=""
home="false"
lock="false"
version=0.37
no_results="No results found. Try another source/term."
user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"
tmp="$PREFIX/tmp"
CONFIG_FILE="$PREFIX/etc/wanda.conf"

usage() {
  echo "wanda ($version)"
  echo "Usage:"
  echo "  wanda [-s source] [-t search term] [-o] [-l] [-h]"
  echo "  -s  source      unsplash,wallhaven,reddit"
  echo "                  4chan,canvas,earthview,imgur"
  echo "                  artstation,local"
  echo "  -t  term        search term"
  echo "  -o  homescreen  set wallpaper on homescreen"
  echo "  -l  lockscreen  set wallpaper on lockscreen"
  echo "  -d  download    save current wallpaper to storage"
  echo "  -h  help        this help message"
  echo "  -u  update      update wanda"
  echo "  -v  version     current version"
  echo ""
  echo "Examples:"
  echo "  wanda"
  echo "  wanda -s ea"
  echo '  wanda -s un -t eiffel tower -ol'
  echo "  wanda -s lo -t folder/path -ol"
  echo "  wanda -s wa -t stars,clouds -ol"
  echo "  wanda -s 4c -t https://boards.4chan.org/wg/thread/7812495"
}

set_wp_url() {
  validate_url $1
  if [ "$home" = "false" ] && [ "$lock" = "false" ]; then
    termux-wallpaper -u "$1"
  fi
  if [ "$home" = "true" ]; then
    termux-wallpaper -u "$1"
  fi
  if [ "$lock" = "true" ]; then
    termux-wallpaper -lu "$1"
  fi
  config_set "last_wallpaper_path" "$1"
  config_set "last_wallpaper_time" "$(date)"
}

set_wp_file() {
  if [ "$home" = "false" ] && [ "$lock" = "false" ]; then
    termux-wallpaper -f "$1"
  fi
  if [ "$home" = "true" ]; then
    termux-wallpaper -f "$1"
  fi
  if [ "$lock" = "true" ]; then
    termux-wallpaper -lf "$1"
  fi
  config_set "last_wallpaper_path" "$1"
  config_set "last_wallpaper_time" "$(date)"
}

validate_url() {
  if [[ $1 != *"http"* ]]; then
    echo "$no_results"
    exit 1
  fi
}

install_package() {
  convert -version 1>/dev/null
  if [ "$?" != 0 ]; then
    echo "$1 is required. Install required package now [y/n]?"
    read agree
    if [ "$agree" = "y" ] || [ "$agree" = "Y" ]; then
      pkg in "$2"
    fi
    exit 0
  fi
}

check_connectivity() {
  curl -s "https://detectportal.firefox.com/success.txt" 1>/dev/null
  if [ "$?" != 0 ]; then
    echo "Please check your internet connection and try again."
    exit 1
  fi
}

update() {
  check_connectivity
  res=$(curl -s "https://gitlab.com/api/v4/projects/29639604/repository/files/manifest.json/raw")
  latest_version=$(echo "$res" | jq --raw-output ".version")
  if (($(echo "$latest_version $version" | awk '{print ($1 > $2)}'))); then
    latest_version=$(echo "$res" | jq --raw-output ".version")
    res=$(curl -s "https://gitlab.com/api/v4/projects/29639604/releases/v$latest_version/assets/links")
    link=$(echo "$res" | jq --raw-output ".[].url")
    binary=$(basename "$link")
    curl -L "$link" -o "$binary"
    pkg in "./$binary"
    rm "$binary"
    wanda -h
  else
    echo "Already latest version ($version)"
  fi
}

wallhaven() {
  res=$(curl -s "https://wallhaven.cc/api/v1/search?q=$1&ratios=portrait&sorting=random")
  echo "$(echo "$res" | jq --raw-output ".data[0].path")"
}

unsplash() {
  local url
  res="https://source.unsplash.com/random/1440x2560/?$1"
  url=$(curl -Ls -o /dev/null -w "%{url_effective}" "$res")
  if [[ $url == *"source-404"* ]]; then echo "$no_results"; fi
  echo "$url"
}

earthview() {
  slug=$(config_get "earthview_slug")
  if [[ -z $slug ]]; then
    slug=$(curl -s "https://earthview.withgoogle.com" | xmllint --html --xpath 'string(//a[@title="Next image"]/@href)' - 2>/dev/null)
  fi
  api="https://earthview.withgoogle.com/_api$slug.json"
  res=$(curl -s "${api}")
  slug=$(echo "$res" | jq --raw-output ".nextSlug")
  url=$(echo "$res" | jq --raw-output ".photoUrl")
  config_set "earthview_slug" "$slug"
  validate_url $url
  filepath="$tmp/earthview.jpg"
  curl -s "$url" -o "$filepath"
  mogrify -rotate 90 "$filepath"
  config_set "last_wallpaper_path" "$url"
  config_set "last_wallpaper_time" "$(date)"
  echo "$filepath"
}

fourchan() {
  # handle no search term -> find threads with mobile/phone in their title.
  # if no threads with mobile/phone in their title exists, first thread is selected
  if [ -z "$1" ]; then
    api="https://a.4cdn.org/wg/catalog.json"
    res=$(curl -s "$api")
    thread=$(echo "$res" | jq '[.[].threads[] | {title: .semantic_url, no: .no} | select( .title | contains("mobile")).no ][0]')
    if [[ -z $thread ]]; then
      thread=$(echo "$res" | jq '[.[].threads[] | {title: .semantic_url, no: .no} | select( .title | contains("phone")).no ][0]')
    fi
    if [[ -z $thread ]]; then
      thread=$(echo "$res" | jq '.[0].threads[1].no')
    fi
    board="wg"
    api="https://a.4cdn.org/$board/thread/$thread.json"
  else
    api="${1/"boards.4chan.org"/"a.4cdn.org"}.json"
    board=$(echo "$1" | cut -d'/' -f4)
  fi
  image_host="https://i.4cdn.org/${board}/"
  res=$(curl -s "$api")
  if [[ -z $res ]]; then
    validate_url 0
  fi
  posts=$(echo "$res" | jq '.[] | length')
  rand=$(shuf -i 0-$posts -n 1)
  post_image=$(echo "$res" | jq ".[][$rand].tim")
  # if post has no image, loop till post with image is found
  while [ "$post_image" = "null" ]; do
    rand=$(shuf -i 0-$posts -n 1)
    post_image=$(echo "$res" | jq ".[][$rand].tim")
  done
  post_exten=$(echo "$res" | jq --raw-output ".[][$rand].ext")
  echo "${image_host}${post_image}${post_exten}"
}

reddit() {
  if [[ -z $1 ]]; then
    api="https://old.reddit.com/r/MobileWallpaper+AMOLEDBackgrounds+VerticalWallpapers.json?limit=100"
  else
    api="https://old.reddit.com/r/MobileWallpaper+AMOLEDBackgrounds+VerticalWallpapers/search.json?q=$1&restrict_sr=on&limit=100"
  fi
  curl -s "$api" -A "$user_agent" -o "$tmp/temp.json"
  posts=$(jq --raw-output ".data.dist" <"$tmp/temp.json")
  rand=$(shuf -i 0-"$posts" -n 1)
  url=$(jq --raw-output ".data.children[$rand].data.url" <"$tmp/temp.json")
  while [[ $url == *"/gallery/"* ]]; do
    rand=$(shuf -i 0-$posts -n 1)
    url=$(cat "$tmp/temp.json" | jq --raw-output ".data.children[$rand].data.url")
  done
  echo "$url"
}

imgur() {
  if [[ -z $1 ]]; then
    rand=$(($((RANDOM % 10)) % 2))
    if [ $rand -eq 1 ]; then
      api="https://old.reddit.com/r/wallpaperdump/search.json?q=mobile&restrict_sr=on&limit=100"
    else
      api="https://old.reddit.com/r/wallpaperdump/search.json?q=phone&restrict_sr=on&limit=100"
    fi
    curl -s "$api" -A $user_agent -o "$tmp/temp.json"
    posts=$(cat "$tmp/temp.json" | jq --raw-output ".data.dist")
    rand=$(shuf -i 0-"$posts" -n 1)
    url=$(cat "$tmp/temp.json" | jq --raw-output ".data.children[$rand].data.url")
    while [[ $url != *"/gallery/"* ]]; do
      rand=$(shuf -i 0-$posts -n 1)
      url=$(cat "$tmp/temp.json" | jq --raw-output ".data.children[$rand].data.url")
    done
  else
    url="https://imgur.com/gallery/$1"
  fi
  res=$(curl -A "$user_agent" -s "${url/http:/https:}" | xmllint --html --xpath 'string(//script[1])' - 2>/dev/null)
  if [[ $res != *"i.imgur.com"* ]]; then
    validate_url 0
  else
    clean=${res//\\\"/\"}
    clean=${clean/window.postDataJSON=/}
    clean=${clean/\\\'/\'}
    clean=$(sed -e 's/^"//' -e 's/"$//' <<<"$clean")
    posts=$(echo "$clean" | jq --raw-output ".image_count")
    rand=$(shuf -i 0-$posts -n 1)
    echo "$(echo "$clean" | jq --raw-output ".media[$rand].url")"
  fi
}

artstation() {
  if [[ -z $1 ]]; then
    artists=("huniartist" "tohad" "snatti" "aenamiart" "seventeenth" "andreasrocha" "slawekfedorczuk")
    i=0
    if [[ $(basename "$SHELL") == "zsh" ]]; then
      i=1
    fi
    query=${artists[$((RANDOM % ${#artists[@]} + i))]}
  else
    query=$1
  fi
  api="https://www.artstation.com/users/$query/projects.json?page=1&per_page=50"
  res=$(curl -s -A "$user_agent" "${api}")
  if [[ -z $res ]]; then
    echo $no_results
  fi
  posts=$(echo -E "$res" | jq --raw-output ".total_count")
  rand=$(shuf -i 0-49 -n 1)
  id=$(echo -E "$res" | jq --raw-output ".data[$rand].id")
  res=$(curl -s -A "$user_agent" "https://www.artstation.com/projects/$id.json")
  res=$(echo -E "$res" | jq --raw-output ".assets[0].image_url")
  echo "$res"
}

canvas() {
  filepath="$tmp/canvas.png"
  . canvas
  case $1 in
  1 | solid) solid ;;
  2 | linear) linear_gradient ;;
  3 | radial) radial_gradient ;;
  4 | twisted) twisted_gradient ;;
  5 | bilinear) bilinear_gradient ;;
  6 | plasma) plasma ;;
  7 | blurred) blurred_noise ;;
  *) randomize ;;
  esac
  config_set "last_wallpaper_path" "canvas"
  config_set "last_wallpaper_time" "$(date)"
  retry=10
  while ! test -f "$filepath"; do
    sleep 2
    retry=$(( retry - 1 ))
    if [[ $retry == 0 ]];then
      break
    fi
  done
  echo "$filepath"
}

### config editor ###
# https://stackoverflow.com/a/60116613
# https://stackoverflow.com/a/2464883
# https://unix.stackexchange.com/a/331965/312709
# thanks to ixz in #bash on irc.freenode.net
config_set() {
  if [[ $2 == *"<CANCEL>"* ]]; then
    exit 0
  fi
  local file=$CONFIG_FILE
  local key=$1
  local val=${*:2}
  ensureConfigFileExists "${file}"
  if ! grep -q "^${key}=" "$file"; then
    printf "\n%s=" "${key}" >>"$file"
  fi
  chc "$file" "$key" "$val"
}

ensureConfigFileExists() {
  if [ ! -e "$1" ]; then
    if [ -e "$1.example" ]; then
      cp "$1.example" "$1"
    else
      touch "$1"
    fi
  fi
}

chc() {
  gawk -v OFS== -v FS== -e \
    'BEGIN { ARGC = 1 } $1 == ARGV[2] { print ARGV[4] ? ARGV[4] : $1, ARGV[3]; next } 1' \
    "$@" <"$1" >"$1.1"
  mv "$1"{.1,}
}

config_get() {
  val="$(config_read_file "$CONFIG_FILE" "${1}")"
  if [ "${val}" = "__UNDEFINED__" ]; then
    val="$(config_read_file "$CONFIG_FILE".example "${1}")"
  fi
  printf -- "%s" "${val}"
}

config_read_file() {
  (grep -E "^${2}=" -m 1 "${1}" 2>/dev/null || echo "VAR=__UNDEFINED__") | head -n 1 | cut -d '=' -f 2-
}
### ### ###

# main
while getopts ':s:t:huvdlo' flag; do
  case "${flag}" in
  s) source="${OPTARG}" ;;
  t) query="${OPTARG//\//%20}" ;;
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
    echo "wanda ($version)"
    exit 0
    ;;
  d)
    url=$(config_get "last_wallpaper_path")
    mkdir -p "$HOME/storage/shared/Download/wanda/"
    path="$HOME/storage/shared/Download/wanda/$(basename "$url")"
    curl -s "$url" -o "$path"
    echo "Saved to $path"
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
wallhaven | wa)
  check_connectivity
  set_wp_url "$(wallhaven "$query")"
  ;;
unsplash | un)
  check_connectivity
  set_wp_url "$(unsplash "$query")"
  ;;
local | lo)
  filepath=$(find "$HOME/$query" -type f -exec file --mime-type {} \+ | awk -F: '{if ($2 ~/image\//) print $1}' | shuf -n 1)
  set_wp_file "$filepath"
  ;;
canvas | ca)
  install_package "Imagemagick" "imagemagick"
  filepath="$(canvas "$query")"
  set_wp_file "$filepath"
  rm -rf "$filepath"
  ;;
4chan | 4c)
  check_connectivity
  set_wp_url "$(fourchan "$query")"
  ;;
earthview | ea)
  install_package "xmllint" "libxml2-utils"
  check_connectivity
  filepath="$(earthview)"
  set_wp_file "$filepath"
  rm -rf "$filepath"
  ;;
reddit | re)
  check_connectivity
  set_wp_url "$(reddit "$query")"
  ;;
imgur | im)
  check_connectivity
  set_wp_url "$(imgur "$query")"
  ;;
artstation | ar)
  check_connectivity
  set_wp_url "$(artstation "$query")"
  ;;
*)
  echo "Unknown source $source"
  usage
  ;;
esac
