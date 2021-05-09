# wallpaper-android
Simple script to set wallpaper using termux

Wallpapers are downloaded from wallhaven.

Usage:
1. Refer the api: https://wallhaven.cc/help/api, get your api key: https://wallhaven.cc/settings/account
2. pkg install termux-api git jq
3. git clone https://github.com/ksyko/wallpaper-android.git
4. Edit the config file to your liking.
5. sh wallhaven-dl.sh

You can pair this with crontab to change wallpaper periodically :)
crontab termux: https://github.com/termux/termux-app/issues/1091#issuecomment-809069738
