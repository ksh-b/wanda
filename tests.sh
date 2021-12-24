#!/usr/bin/bash

. "./wanda.sh"
mkdir -p "./etc"
mkdir -p "./tmp"
touch "./tmp/temp.json"
user_agent="Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"

query=""
failed=0

encode() {
  query="${1//\//%20}"
}

contains() {
  if [[ "$1" == *"$2"* ]]; then
    echo "pass"
    return 0
  else
    echo "fail"
    echo "Actual:$1"
    echo "Expected:$2"
    echo ""
    return 1
  fi
}

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# echo "wallhaven tests"
# contains "$(wallhaven)" "https://w.wallhaven.cc/full/"
# failed=$(($failed+$?)); sleep 3
# contains "$(wallhaven "$(encode "eiffel tower")")" "https://w.wallhaven.cc/full/"
# failed=$(($failed+$?)); sleep 3
# contains "$(wallhaven "noresults123")" "null"
# failed=$(($failed+$?)); sleep 3

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# echo "unsplash tests"
#
# contains "$(unsplash)" "https://images.unsplash.com/photo-"
# failed=$(($failed+$?)); sleep 3
# contains "$(unsplash "$(encode "eiffel tower")")" "https://images.unsplash.com/photo-"
# failed=$(($failed+$?)); sleep 3
# contains "$(unsplash "noresults123")" "https://images.unsplash.com/source-404"
# failed=$(($failed+$?)); sleep 3

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# echo "reddit tests"
#
# contains "$(reddit)" "https://i.redd.it/"
# failed=$(($failed+$?)); sleep 3
# contains "$(reddit "$(encode "eiffel tower")")" "https://i.redd.it/"
# failed=$(($failed+$?)); sleep 3
# contains "$(reddit "noresults123")" "null"
# failed=$(($failed+$?)); sleep 3

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

# echo "imgur tests"
#
# contains "$(imgur)" "https://i.imgur.com/"
# failed=$(($failed+$?)); sleep 3
# contains "$(imgur "XlfFj3g")" "https://i.imgur.com/"
# failed=$(($failed+$?)); sleep 3
# contains "$(imgur "noresults123")" "No results"
# failed=$(($failed+$?)); sleep 3

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

echo "artstation tests"

contains "$(artstation)" "artstation.com/p/assets/images/images/"
failed=$(($failed+$?)); sleep 3
contains "$(artstation "huniartist")" "artstation.com/p/assets/images/images/"
failed=$(($failed+$?)); sleep 3
contains "$(artstation "noresults123")" "No results"
failed=$(($failed+$?)); sleep 3

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

echo "4chan tests"

contains "$(4chan)" "i.4cdn.org"
failed=$(($failed+$?)); sleep 3
contains "$(artstation "huniartist")" "i.4cdn.org"
failed=$(($failed+$?)); sleep 3
contains "$(artstation "noresults123")" "No results"
failed=$(($failed+$?)); sleep 3

### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###

echo ""
rm -rf "./etc"
rm -rf "./tmp"
echo "$failed tests failed"
exit $failed
