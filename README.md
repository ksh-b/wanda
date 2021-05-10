# wallpaper-android
Simple script to set random wallpaper using termux

Wallpapers are downloaded from wallhaven.

Usage:
0. Register/Login on [wallhaven.cc](https://wallhaven.cc/login)
1. Get your wallhaven [api key](https://wallhaven.cc/settings/account)
2. `pkg update && pkg upgrade`
3. `pkg install termux-api git jq curl`
4. `git clone https://github.com/ksyko/wallpaper-android.git`
5. Edit the config file to your liking and add your api key to it. Refer the [wallhaven api] for available options(https://wallhaven.cc/help/api)
6. `sh wallhaven-dl.sh`

You can pair this with [crontab](https://github.com/termux/termux-app/issues/1091#issuecomment-809069738) to change wallpaper periodically :)
