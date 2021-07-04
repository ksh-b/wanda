#!/data/data/com.termux/files/usr/bin/bash
. "$SCRIPT_DIR/sources/local/config"
filepath=$(find "$images_path" -type f -exec file --mime-type {} \+ | awk -F: '{if ($2 ~/image\//) print $1}' | shuf -n 1)
echo "$filepath"
