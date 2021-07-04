#!/data/data/com.termux/files/usr/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CONFIG_FILE="$SCRIPT_DIR/sources/$source/config"
. "$SCRIPT_DIR/tools/util.sh"
. "$SCRIPT_DIR/config"

# sub
u_input=$(get_input radio "Reddit: Choose a subreddit" "iWallpaper,MobileWallpaper,Verticalwallpapers,Amoledbackgrounds,AnimePhoneWallpapers,ComicWalls,wallpaper+wallpapers")
config_set "sub" "$u_input"

# sort
u_input=$(get_input radio "sort" "hot,new,rising,top,gilded")
config_set "sort" "$u_input"
