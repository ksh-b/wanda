#!/data/data/com.termux/files/usr/bin/bash
. "$SCRIPT_DIR/sources/dynamic/config"

# get hour
h=$(date +"%-H")

# symlinks dont get extracted from the zip
# workaround - get the file from latest recent hour
if [ ! -f "$filepath" ]; then
  h=$((h-1))
fi

# apply wallpaper
filepath="$SCRIPT_DIR/sources/dynamic/images/$imageset/$h.jpg"
echo "$filepath"
