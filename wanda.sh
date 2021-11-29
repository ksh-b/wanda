#!/data/data/com.termux/files/usr/bin/bash

source="unsplash"
query=""
home="false"
lock="false"
version=0.3
no_results="No results for $query. Try another source/keyword"

usage() {
  echo "wanda ($version)"
  echo "Usage:"
  echo "  wanda [-s source] [-t search term] [-o] [-l] [-h]"
  echo "  -s  source      [un]splash,[wa]llhaven,[re]ddit,[lo]cal"
  echo "                  [4c]han,[ca]nvas,[ea]rthview"
  echo "  -t  t           search term."
  echo "  -o  homescreen  set wallpaper on homescreen"
  echo "  -l  lockscreen  set wallpaper on lockscreen"
  echo "  -h  help        this help message"
  echo "  -u  update      update wanda"
  echo "  -v  version     current version"
  echo ""
  echo "Examples:"
  echo "  wanda"
  echo "  wanda -s ea"
  echo '  wanda -s un -t "eiffel tower" -ol'
  echo "  wanda -s lo -t folder/path -ol"
  echo "  wanda -s wa -t stars,clouds -ol"
  echo "  wanda -s 4c -t https://boards.4chan.org/wg/thread/7812495"
}

set_wp_url() {
  validate_url
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
}

validate_url() {
  if [ -z "$url" ]; then
    echo "$no_results"
    exit 1
  fi
  urlstatus=$(curl -o /dev/null --silent --head --write-out '%{http_code}' "$url")
  if [ $urlstatus != 200 ]; then
    echo "[$urlstatus] Failed to load url: $url."
    exit 1
  fi
}

install_package() {
  convert -version 1>/dev/null
  if [ "$?" != 0 ]; then
    echo "$1 is required. Install required package now [y/n]?"
    read agree
    if [ "$agree" = "y" ] || [ "$agree" = "Y" ]; then
      pkg in $2
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

clean() {
  rm "$1" &>/dev/null
}

update() {
  check_connectivity
  res=$(curl -s curl "https://gitlab.com/api/v4/projects/29639604/repository/files/manifest.json/raw?ref=lite")
  latest_version=$(echo "$res" | jq --raw-output ".version")
  if (($(echo "$latest_version $version" | awk '{print ($1 > $2)}'))); then
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

# main
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
    echo "wanda ($version)"
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
  res=$(curl -s "https://wallhaven.cc/api/v1/search?q=$query&ratios=portrait&sorting=random")
  url=$(echo "$res" | jq --raw-output ".data[0].path")
  set_wp_url "$url"
  ;;
unsplash | un)
  check_connectivity
  res="https://source.unsplash.com/random/1440x2560/?$query"
  url=$(curl -Ls -o /dev/null -w %{url_effective} "$res")
  if [[ $url == *"source-404"* ]]; then
    echo "$no_results"
  fi
  set_wp_url "$url"
  ;;
reddit | re)
  check_connectivity
  api="https://old.reddit.com/r/MobileWallpaper/search.json?q=$query&restrict_sr=on&limit=$posts"
  res=$(curl -s -A "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0" "$api")
  url=$(echo "$res" | jq --raw-output ".data.children[$rand].data.url")
  posts=$(echo "$res" | jq --raw-output ".data.dist")
  rand=$(shuf -i 0-$posts -n 1)
  while [[ $url == *"/gallery/"* ]]; do
    rand=$(shuf -i 0-$posts -n 1)
    url=$(echo "$res" | jq --raw-output ".data.children[$rand].data.url")
  done
  set_wp_url $url
  ;;
local | lo)
  filepath=$(find "$HOME/storage/shared/$query" -type f -exec file --mime-type {} \+ | awk -F: '{if ($2 ~/image\//) print $1}' | shuf -n 1)
  set_wp_file "$filepath"
  ;;
canvas | ca)
  install_package "Imagemagick" "imagemagick"
  filepath="$PREFIX/tmp/canvas.png"
  . canvas.sh
  case $query in
  1 | solid) solid ;;
  2 | linear) linear_gradient ;;
  3 | radial) radial_gradient ;;
  4 | twisted) twisted_gradient ;;
  5 | bilinear) bilinear_gradient ;;
  6 | plasma) plasma ;;
  7 | blurred) blurred_noise ;;
  *) randomize ;;
  esac
  set_wp_file "$filepath"
  #clean "$filepath"
  ;;
4chan | 4c)
  check_connectivity
  board=$(echo $query | cut -d'/' -f4)
  image_host="https://i.4cdn.org/${board}/"
  api="${query/"boards.4chan.org"/"a.4cdn.org"}.json"
  res=$(curl -s "$api")
  posts=$(echo "$res" | jq '.[] | length')
  rand=$(shuf -i 0-$posts -n 1)
  post_image=$(echo "$res" | jq ".[][$rand].tim")
  # if post has no image, loop till post with image is found
  while [ "$post_image" = "null" ]; do
    rand=$(shuf -i 0-$posts -n 1)
    post_image=$(echo "$res" | jq ".[][$rand].tim")
  done
  post_exten=$(echo "$res" | jq --raw-output ".[][$rand].ext")
  url="${image_host}${post_image}${post_exten}"
  set_wp_url "$url"
  ;;
earthview | ea)
  install_package "xmllint" "libxml2-utils"
  check_connectivity
  if [[ -z $link ]]; then
    link=$(curl -s "https://earthview.withgoogle.com" | xmllint --html --xpath 'string(//a[@title="Next image"]/@href)' - 2>/dev/null)
  fi

  api="https://earthview.withgoogle.com/_api$link.json"
  res=$(curl -s "${api}")
  url=$(echo "$res" | jq --raw-output ".photoUrl")
  validate_url

  filepath="$PREFIX/tmp/earthview.jpg"
  curl -s "$url" -o "$filepath"
  mogrify -rotate 90 "$filepath"
  set_wp_file $filepath
  #clean "$filepath"
  ;;
*)
  echo "Unknown source $source"
  usage
  ;;
esac
