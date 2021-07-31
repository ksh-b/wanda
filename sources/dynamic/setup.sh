#!/data/data/com.termux/files/usr/bin/bash
DYN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
mkdir -p "$DYN_DIR"
cd "$DYN_DIR" || (echo "Failed to setup" && exit 1)
echo "Downloading imagesets... [~180 MB]"
curl -L -o "$DYN_DIR/dynamic.zip" "https://github.com/GitGangGuy/dynamic-wallpaper-improved/archive/refs/heads/master.zip"
echo "Extracting imagesets..."
unzip "$DYN_DIR/dynamic.zip" "dynamic-wallpaper-improved-master/images/*" &>/dev/null
mv "$DYN_DIR/dynamic-wallpaper-improved-master/images/" "$DYN_DIR"
echo "Cleaning up..."
rm -rf "$DYN_DIR/dynamic-wallpaper-improved-master"
rm "$DYN_DIR/dynamic.zip"
