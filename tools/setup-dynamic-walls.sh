#!/data/data/com.termux/files/usr/bin/bash
SCRIPT_DIR="$( cd "../$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DYN_DIR="$SCRIPT_DIR"/sources/dynamic
mkdir -p "$DYN_DIR"
cd "$DYN_DIR" || (echo "Failed to setup" && exit 1)
curl -L -o "$DYN_DIR/dynamic.zip" "https://github.com/GitGangGuy/dynamic-wallpaper-improved/archive/refs/heads/master.zip"
unzip "$DYN_DIR/dynamic.zip" "dynamic-wallpaper-improved-master/images/*"
mv "$DYN_DIR/dynamic-wallpaper-improved-master/images/" "$SCRIPT_DIR"/dynamic
rm "$DYN_DIR/dynamic.zip"
