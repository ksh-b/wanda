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
  ofile=$SCRIPT_DIR/downloads/$(basename $url)
  cfile=$SCRIPT_DIR/downloads/cropped/$(basename $url)
  cropped=$(curl -s --user "$imagga_key" "https://api.imagga.com/v2/croppings?image_url=$url&resolution=${width}x$height")
  x1=$(echo $cropped |  jq --raw-output ".result.croppings[0].x1")
  x2=$(echo $cropped |  jq --raw-output ".result.croppings[0].x2")
  y1=$(echo $cropped |  jq --raw-output ".result.croppings[0].y1")
  y2=$(echo $cropped |  jq --raw-output ".result.croppings[0].y2")
  curl -s $url --output $ofile
  w=$(identify -format "%w" $ofile)> /dev/null
  h=$(identify -format "%h" $ofile)> /dev/null
  if [ $w -gt $h ]; then
    convert $ofile -crop ${x2}x${y2}+${x1}+${y1} $cfile
    source="local"
    filepath=$cfile
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
