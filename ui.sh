#!/data/data/com.termux/files/usr/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
CONFIG_FILE="$SCRIPT_DIR/config"
. "$CONFIG_FILE"
. "$SCRIPT_DIR/tools/util.sh"

# source
u_input=$(get_input radio "Wanda: Choose a source" "4chan,dynamic,earthview,imagemagick,local,picsum,reddit,wallhaven")
config_set "source" "$u_input"

# screen
u_input=$(get_input radio "Wanda: Choose which screen(s) you want to set wallpaper" "home,lock,both")
config_set "screen" "$u_input"

# keep
u_input=$(get_input radio "Wanda: Save downloaded wallpapers?" "true,false")
config_set "keep" "$u_input"

# resolution
resolution=$(get_input radio "Wanda: Choose screeen resolution" "480x800,540x960,720x1280,768x1280,1080x1920,1280x720,1440x2560,1920x1080,2960x1440")
IFS="x"
read -ra strarr <<< "$resolution"
config_set "width" "${strarr[1]}"
config_set "height" "${strarr[2]}"

# offline mode
u_input=$(get_input radio "Wanda: Offline mode" "off,local,imagemagick")
config_set "offline_mode" "$u_input"
