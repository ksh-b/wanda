#!/data/data/com.termux/files/usr/bin/bash

source="unsplash"
query=""
home="true"
lock="true"
version=0.44
no_results="No results found. Try another source/term."
user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"
tmp="$PREFIX/tmp"
CONFIG_FILE="$PREFIX/etc/wanda.conf"

usage() {
  echo "wanda ($version)"
  echo "Usage:"
  echo "  wanda [-s source] [-t search term] [-o] [-l] [-d] [-h] [-v] [-i]"
  echo "  -s  source      unsplash,wallhaven,reddit"
  echo "                  4chan,canvas,earthview,imgur"
  echo "                  artstation,local, 500px, imsea"
  echo "  -t  term        search term"
  echo "  -o  homescreen  set wallpaper on homescreen only"
  echo "  -l  lockscreen  set wallpaper on lockscreen only"
  echo "  -d  download    save current wallpaper to storage"
  echo "  -h  help        this help message"
  echo "  -v  version     current version"
  echo "  -i  list        print supported sources and their specific usage"
  echo ""
  echo "Examples:"
  echo "  wanda"
  echo "  wanda -s earthview"
  echo '  wanda -s un -t eiffel tower'
  echo "  wanda -s lo -t folder/path"
}

set_wp_url() {
  validate_url $1
  if [ "$home" = "false" ] && [ "$lock" = "false" ]; then
    exit 0
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
}

size() {
  hxw=$(getprop "persist.vendor.camera.display.umax")
  if [ -z "$hxw" ]; then
    w=$(cut -d "x" -f1 <<< "$hxw")
    h=$(cut -d "x" -f2 <<< "$hxw")
    echo "$("${w}x${h}")"
  else
    echo "1440x2960"
  fi
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
  slug="$(config_get "earthview_slug")"
  if [[ -z $slug ]]; then
    slug="$(curl -s "https://earthview.withgoogle.com" | xmllint --html --xpath 'string(//a[@title="Next image"]/@href)' - 2>/dev/null)"
  fi
  api="https://earthview.withgoogle.com/_api$slug.json"
  res=$(curl -s -A "$user_agent" "${api}")
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
    query="${1//%20//}"
    api="${query/"boards.4chan.org"/"a.4cdn.org"}.json"
    board=$(echo "$1" | cut -d'/' -f4)
  fi
  image_host="https://i.4cdn.org/${board}/"
  res=$(curl -s "$api")
  if [[ -z $res ]]; then
    validate_url 0
  fi
  posts=$(echo "$res" | jq '.[] | length')
  rand=$(shuf -i 1-$(( posts-1 )) -n 1)
  post_image=$(echo "$res" | jq ".[][$rand].tim")
  # if post has no image, loop till post with image is found
  while [ "$post_image" = "null" ]; do
    rand=$(shuf -i 1-$(( posts-1 )) -n 1)
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
  rand=$(shuf -i 1-$(( posts-1 )) -n 1)
  url=$(jq --raw-output ".data.children[$rand].data.url" <"$tmp/temp.json")
  while [[ $url == *"/gallery/"* ]]; do
    rand=$(shuf -i 1-$(( posts-1 )) -n 1)
    url=$(cat "$tmp/temp.json" | jq --raw-output ".data.children[$rand].data.url")
  done
  echo "$url"
}

imsea() {
  size=$(size)
  if [[ -z $1 ]]; then
    api="https://imsea.herokuapp.com/api/1?q=$size+wallpaper"
  else
    api="https://imsea.herokuapp.com/api/1?q=$size+$1"
  fi
  res=$(curl -s "${api}")
  posts=$(echo "$res" | jq  ".results | length")
  rand=$(shuf -i 1-$(( posts-1 )) -n 1)
  url=$(echo "$res" | jq --raw-output ".results[$rand]")
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
    rand=$(shuf -i 1-$(( posts-1 )) -n 1)
    url=$(cat "$tmp/temp.json" | jq --raw-output ".data.children[$rand].data.url")
    while [[ $url != *"/gallery/"* ]]; do
      rand=$(shuf -i 1-$(( posts-1 )) -n 1)
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
    rand=$(shuf -i 1-$(( posts-1 )) -n 1)
    echo "$(echo "$clean" | jq --raw-output ".media[$rand].url")"
  fi
}

artstation_prints() {
  query=$1
  if [[ -z $query ]]; then
    query="landscape"
  fi
  api="https://www.artstation.com/api/v2/prints/public/printed_products.json?page=1&per_page=30&orientation=portrait&q=$query&sort=trending&visibility=profile&variant_filter=price_limits_per_type"
  res=$(curl -s -A "$user_agent" "${api}")
  if [[ -z $res ]]; then
    echo $no_results
  fi
  posts=$(echo -E "$res" | jq --raw-output ".data | length")
  rand=$(shuf -i 1-$(( posts-1 )) -n 1)
  res=$(echo -E "$res" | jq --raw-output ".data[$rand].print_type_variants[0].image_urls[0].url")
  echo "$res"
}

artstation_alt() {
  query=$1
  if [[ -z $query ]]; then
    query="landscape"
  fi
  api="https://www.artstation.com/api/v2/search/projects.json"
  body='{"query":"'$query'","page":1,"per_page":50,"sorting":"relevance","pro_first":"1","filters":[],"additional_fields":[]}'
  res=$(curl -s -A "$user_agent" -X POST $api \
  -H "Content-Type: application/json" -H "Host: www.artstation.com" \
  -H "User-Agent: PostmanRuntime/7.29.0" \
  -d "$body"
  )
  if [[ -z $res ]]; then
    echo $no_results
  fi
  total=$(echo -E "$res" | jq --raw-output ".total_count")
  if [[ -z $total ]]; then
    echo $no_results
  fi
  posts=$(echo -E "$res" | jq --raw-output ".data | length")
  rand=$(shuf -i 1-$(( posts-1 )) -n 1)
  hash_id=$(echo -E "$res" | jq --raw-output ".data[$rand].hash_id")

  api="https://www.artstation.com/projects/$hash_id.json"
  res=$(curl -s -A "$user_agent" "${api}")
  if [[ -z $res ]]; then
    echo $no_results
  fi
  res=$(echo -E "$res" | jq --raw-output ".assets[0].image_url")
  echo "$res"
}

artstation_artist() {
  query=$1
  if [[ -z $query ]]; then
    query="landscape"
  fi
  api="https://www.artstation.com/users/$query/projects.json"
  res=$(curl -s -A "$user_agent" $api)
  if [[ -z $res ]]; then
    echo $no_results
  fi
  posts=$(echo -E "$res" | jq --raw-output ".data | length")
  rand=$(shuf -i 1-$(( posts-1 )) -n 1)
  hash_id=$(echo -E "$res" | jq --raw-output ".data[$rand].hash_id")

  api="https://www.artstation.com/projects/$hash_id.json"
  res=$(curl -s -A "$user_agent" "${api}")
  if [[ -z $res ]]; then
    echo $no_results
  fi
  res=$(echo -E "$res" | jq --raw-output ".assets[0].image_url")
  echo "$res"
}

canvas() {
  filepath="$tmp/canvas.png"
  . canvas "$(size)"
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
    retry=$((retry - 1))
    if [[ $retry == 0 ]]; then
      break
    fi
  done
  echo "$filepath"
}

fivehundredpx() {
  query=$1
  payload='
{"operationName":"PhotoSearchQueryRendererQuery","variables":{"sort":"RELEVANCE","search":"'$query'"},"query":"query PhotoSearchQueryRendererQuery($sort: PhotoSort, $search: String!) {\n...PhotoSearchPaginationContainer_query_67nah\n}\n\nfragment PhotoSearchPaginationContainer_query_67nah on Query {\nphotoSearch(sort: $sort, first: 20, search: $search) { \nedges { \nnode {\n id\n legacyId\n canonicalPath\n name\n description\n category\n uploadedAt\n location\n width\n height\n isLikedByMe\n notSafeForWork\n tags\n photographer: uploader { \n id \n legacyId \n username \n displayName \n canonicalPath \n avatar { \n images { \n url \n id \n } \n id \n } \n followedByUsers { \n totalCount \n isFollowedByMe \n }\n }\n images(sizes: [33, 35]) { \n size \n url \n jpegUrl \n webpUrl \n id\n }\n __typename \n} \ncursor \n} \ntotalCount \npageInfo { \nendCursor \nhasNextPage \n}\n}\n}\n"}'
  if [[ -z $query ]]; then
    query="landscape"
  fi
  api="https://api.500px.com/graphql"
  res=$(curl -s -A "$user_agent" -X POST $api \
  -H "Content-Type: application/json" -H "Host: api.500px.com" \
  -d "$payload"
  )
  if [[ -z $res ]]; then
    echo $no_results
  fi
  posts=$(echo -E "$res" | jq --raw-output ".data.photoSearch.edges | length")
  rand=$(shuf -i 1-$(( posts-1 )) -n 1)
  url=$(echo -E "$res" | jq --raw-output ".data.photoSearch.edges[$rand].node.images[1].url")
  echo "$url"
}

supported() {
  CYAN="$(printf '\033[36m')"
  MAGENTA="$(printf '\033[35m')"
  ORANGE="$(printf '\033[33m')"
  echo -e "Supported sources."
  echo -e "${CYAN}4c${MAGENTA}han ${ORANGE}[thread url. example: https://boards.4chan.org/wg/thread/1234567]"
  echo -e "${CYAN}5${MAGENTA}00${CYAN}p${MAGENTA}x ${ORANGE}[search term]"
  echo -e "${CYAN}ar${MAGENTA}station ${ORANGE}[search term for prints page]"
  echo -e "${CYAN}ar${MAGENTA}station_${CYAN}a${MAGENTA}rt ${ORANGE}[artist id. example: tohad]"
  echo -e "${CYAN}ar${MAGENTA}station_${CYAN}g${MAGENTA}en ${ORANGE}[search term for main page]"
  echo -e "${CYAN}ca${MAGENTA}nvas ${ORANGE}[solid|linear|radial|twisted|bilinear|plasma|blurred|[1-7]]"
  echo -e "${CYAN}ea${MAGENTA}rthview ${ORANGE}(takes no search term)"
  echo -e "${CYAN}im${MAGENTA}gur ${ORANGE}[gallery id. example: qF259WO]"
  echo -e "${CYAN}lo${MAGENTA}cal ${ORANGE}[path relative to $HOME]"
  echo -e "${CYAN}re${MAGENTA}ddit ${ORANGE}[search term]"
  echo -e "${CYAN}un${MAGENTA}splash ${ORANGE}[search term]"
  echo -e "${CYAN}wa${MAGENTA}llhaven ${ORANGE}[search term]"
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
while getopts ':s:t:hvdloi' flag; do
  case "${flag}" in
  s) source="${OPTARG}" ;;
  t) query="${OPTARG//\//%20}" ;;
  o) lock="false" ;;
  l) home="false" ;;
  h)
    usage
    exit 0
    ;;
  v)
    echo "wanda ($version)"
    exit 0
    ;;
  d)
    url=$(config_get "last_wallpaper_path")
    validate_url $url
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

  i)
    supported
    exit 0
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
imsea | is)
  check_connectivity
  set_wp_url "$(imsea "$query")"
  ;;
artstation | ar)
  check_connectivity
  set_wp_url "$(artstation_prints "$query")"
  ;;
artstation_gen | arg)
  check_connectivity
  set_wp_url "$(artstation_alt "$query")"
  ;;
artstation_art | ara)
  check_connectivity
  set_wp_url "$(artstation_artist "$query")"
  ;;
500px | 5p)
  check_connectivity
  set_wp_url "$(fivehundredpx "$query")"
  ;;
*)
  echo "Unknown source $source"
  supported
  ;;
esac
