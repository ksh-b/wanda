
wanda_dir="storage/shared/scripts"
clear
pkg up
pkg in termux-api curl jq file
termux-setup-storage
mkdir -p $wanda_dir && cd $wanda_dir
curl -L -O -s https://github.com/ksyko/wanda/releases/download/v0.01/wanda.tar.gz && tar -xzf wanda.tar.gz && echo "Downloaded wanda to $(pwd)" || echo "Failed to download wanda"
