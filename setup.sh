#!/data/data/com.termux/files/usr/bin/bash
# experimental
clear
pkg up
pkg in termux-api curl jq file
termux-setup-storage
cd $HOME
wanda_dir="$HOME/storage/shared/scripts/wanda/"
mkdir -p $wanda_dir && cd $wanda_dir
curl -L -O -s "https://github.com/ksyko/wanda/releases/download/v0.03/wanda.tar.gz" && tar -xzf wanda.tar.gz && echo "Downloaded wanda to $(pwd)" || echo "Failed to download wanda"
rm wanda.tar.gz
