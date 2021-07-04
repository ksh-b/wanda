#!/data/data/com.termux/files/usr/bin/bash
. "$SCRIPT_DIR/dynamic/config"
h=$(date +"%-H")
if [ ! -f "$filepath" ]; then
  h=$((h-1))
fi
filepath="$SCRIPT_DIR/dynamic/images/$imageset/$h.jpg"
echo "$filepath"
