#!/data/data/com.termux/files/usr/bin/bash
clear
apt update
apt -y install termux-api curl jq file imagemagick libxml2-utils
cd "$HOME" || (echo "Error. Could not navigate to home." && exit 1)
wanda_dir="$HOME/storage/shared/scripts/wanda"
(mkdir -p "$wanda_dir" && cd "$wanda_dir") || (echo "Error. Check storage permissions." && exit 1)
curl -L -O -s "https://github.com/ksyko/wanda/releases/download/v0.03/wanda.tar.gz" && tar -xzf wanda.tar.gz --directory "$wanda_dir" && echo "Downloaded wanda to $(pwd)" || echo "Failed to download wanda"
mkdir -p "$wanda_dir/downloads/cropped/"
mkdir -p "$HOME/.shortcuts/tasks"
(cd "$HOME/.shortcuts/tasks" && \
 echo "cd $HOME/storage/shared/scripts/wanda && bash wanda.sh" > file.txt ) || \
 (echo "Error. Could not create shortcut." && exit 1)
rm wanda.tar.gz
