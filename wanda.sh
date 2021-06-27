#!/data/data/com.termux/files/usr/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. "$SCRIPT_DIR/config"

# try to connect to internet
curl -s "https://detectportal.firefox.com/success.txt" 1> /dev/null

# if offline, use local or skip
if [ "$?" != 0 ]; then
  case "$offline_mode" in
    off)
      exit 0
      ;;
    local|imagemagick|dynamic)
      source="$offline_mode"
      ;;
    *)
      echo "This source doesn't support offline mode"
      exit 1
      ;;
  esac
fi

. "$SCRIPT_DIR/$source/pick.sh"

if [ "$autocrop" = "true" ]; then
  ofile=$SCRIPT_DIR/downloads/$(basename "$url")
  cfile=$SCRIPT_DIR/downloads/cropped/$(basename "$url")
  curl -s "$url" --output "$ofile"
  w=$(identify -format "%w" "$ofile")> /dev/null
  h=$(identify -format "%h" "$ofile")> /dev/null
  if [ "$w" -gt "$h" ]; then
    cropped=$(curl -s --user "$imagga_key" "https://api.imagga.com/v2/croppings?image_url=$url&resolution=${width}x$height")
    status=$(echo "$cropped" |  jq --raw-output ".status.type")
    if [ "$status" = "success" ]; then
      x1=$(echo "$cropped" |  jq --raw-output ".result.croppings[0].x1")
      x2=$(echo "$cropped" |  jq --raw-output ".result.croppings[0].x2")
      y1=$(echo "$cropped" |  jq --raw-output ".result.croppings[0].y1")
      y2=$(echo "$cropped" |  jq --raw-output ".result.croppings[0].y2")
      convert "$ofile" -crop "${x2}x${y2}+${x1}+${y1}" "$cfile"
      source="local"
      filepath="$cfile"
    fi
  fi
  # keep or remove file as per config
  if [ "$keep" = "false" ]; then
    rm -f "$ofile"
  fi
  if [ "$keep_crop" = "false" ]; then
    rm -f "$cfile"
  fi
fi

# set wallpaper according to source
if [ $source = "local" ] || [ $source = "imagemagick" ] || [ $source = "dynamic" ]; then
  case "$screen" in
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
  case "$screen" in
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

if [ "$keep" = "true" ]; then
  curl -s "$url" -o "$SCRIPT_DIR/downloads/$(basename "$url")"
else
  if [ "$source" = "imagemagick" ]; then
    rm -f "$filepath"
  fi
fi
