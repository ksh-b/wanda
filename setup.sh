#!/data/data/com.termux/files/usr/bin/bash
clear
pkg up
pkg in termux-api curl jq file
termux-setup-storage
cd "$HOME" || (echo "Error. Could not navigate to home." && exit 1)
wanda_dir="$HOME/storage/shared/scripts/wanda"
(mkdir -p "$wanda_dir" && cd "$wanda_dir") || (echo "Error. Check storage permissions." && exit 1)
curl -L -O -s "https://github.com/ksyko/wanda/releases/download/v0.03/wanda.tar.gz" && tar -xzf wanda.tar.gz && echo "Downloaded wanda to $(pwd)" || echo "Failed to download wanda"
mkdir -p "$wanda_dir/downloads/cropped/"
rm wanda.tar.gz
