#!/data/data/com.termux/files/usr/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. "$SCRIPT_DIR/config"

# source
u_input=$(get_input radio "Wanda: Choose a source" "4chan,dynamic,earthview,imagemagick,local,picsum,reddit,wallhaven")
config_set "$CONFIG_FILE" "source" "$u_input"

# screen
u_input=$(get_input radio "Wanda: Choose which screen(s) you want to set wallpaper" "home,lock,both")
config_set "$CONFIG_FILE" "screen" "$u_input"

# keep
u_input=$(get_input radio "Wanda: Save downloaded wallpapers?" "true,false")
config_set "$CONFIG_FILE" "keep" "$u_input"

# resolution
resolution=$(get_input radio "Wanda: Choose screeen resolution" "480x800,540x960,720x1280,768x1280,1080x1920,1280x720,1440x2560,1920x1080,2960x1440")
IFS="x"
read -ra strarr <<< "$resolution"
config_set "$CONFIG_FILE" "width" "${strarr[1]}"
config_set "$CONFIG_FILE" "height" "${strarr[2]}"

# offline mode
u_input=$(get_input radio "Wanda: Offline mode" "off,local,imagemagick")
config_set "$CONFIG_FILE" "offline_mode" "$u_input"
