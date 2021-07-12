#!/data/data/com.termux/files/usr/bin/bash
version="v0.07"

# get dependencies
apt update
apt -y install termux-api curl jq file imagemagick libxml2-utils

# setup download folder
cd "$HOME" || (echo "Error. Could not navigate to home." && exit 1)
wanda_dir="$HOME/storage/shared/scripts/wanda"
(mkdir -p "$wanda_dir" && cd "$wanda_dir") || (echo "Error. Check storage permissions." && exit 1)

# download latest release
curl -L -O -s "https://github.com/ksyko/wanda/releases/download/$version/wanda.tar.gz" && tar -xzf wanda.tar.gz --directory "$wanda_dir" && echo "Downloaded wanda to $(pwd)" || echo "Failed to download wanda"
mkdir -p "$wanda_dir/downloads/cropped/"

# create widget task
mkdir -p "$HOME/.shortcuts/tasks"
(cd "$HOME/.shortcuts/tasks" && \
 echo "cd $HOME/storage/shared/scripts/wanda && bash wanda.sh" > wanda.sh \
  && chmod +x wanda.sh && echo "Added shortcut for termux-widget") || \
 (echo "Error. Could not create shortcut." && exit 1)

# cleanup
rm wanda.tar.gz
