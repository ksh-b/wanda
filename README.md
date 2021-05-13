# wanda
Simple script to set random wallpaper using termux

Wallpapers are downloaded from wallhaven.

Usage:

1. Get requirements and the script:
```
pkg update && pkg upgrade
pkg install termux-api git curl jq
git clone https://github.com/ksyko/wanda.git
```
2. Edit the config file to your liking and add your api key to it. Refer the [wallhaven api](https://wallhaven.cc/help/api) for available options
3. `sh wallhaven-dl.sh`

You can pair this with [crontab](https://github.com/termux/termux-app/issues/1091#issuecomment-809069738) to change wallpaper periodically :)
