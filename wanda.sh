#!/data/data/com.termux/files/usr/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. $SCRIPT_DIR/config

# try to connect to internet
curl -s "https://detectportal.firefox.com/success.txt" 1> /dev/null

# if offline, use local or skip
if [ $? != 0 ]; then
  if [ $offline_use_local = "true" ]; then
    source="local"
  else
    exit 0
  fi
fi

. $SCRIPT_DIR/$source/pick.sh

if [ $autocrop = "true" ]; then
  cropped=$(curl -s --user "$imagga_key" "https://api.imagga.com/v2/croppings?image_url=$url&resolution=${width}x$height")
  x1=$(echo $cropped |  jq --raw-output ".result.croppings[0].x1")
  x2=$(echo $cropped |  jq --raw-output ".result.croppings[0].x2")
  y1=$(echo $cropped |  jq --raw-output ".result.croppings[0].y1")
  y2=$(echo $cropped |  jq --raw-output ".result.croppings[0].y2")
  curl -s $url --output original.jpg
  w=$(identify -format "%w" "original.jpg")> /dev/null
  h=$(identify -format "%h" "original.jpg")> /dev/null
  if [ $w -gt $h ]; then
    convert original.jpg -crop ${x2}x${y2}+${x1}+${y1} "cropped.jpg"
    filepath="cropped.jpg"
  fi
fi

# set wallpaper according to source
if [ "$source" = "local" ]; then
  case $screen in
      both)
          termux-wallpaper -f "$filepath"
          termux-wallpaper -lf "$filepath"
          ;;
      home)
          termux-wallpaper -f "$filepath"
          ;;
      lock)
          termux-wallpaper -lf "$filepath"
          ;;
  esac
else
  case $screen in
      both)
          termux-wallpaper -u "$url"
          termux-wallpaper -lu "$url"
          ;;
      home)
          termux-wallpaper -u "$url"
          ;;
      lock)
          termux-wallpaper -lu "$url"
          ;;
  esac
fi

rm cropped.jpg original.jpg
