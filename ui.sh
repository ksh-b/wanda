#!/data/data/com.termux/files/usr/bin/bash
export SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. "$SCRIPT_DIR/tools/util.sh"

setup_wanda() {
  export CONFIG_FILE="$SCRIPT_DIR/config"
  . "$SCRIPT_DIR/tools/util.sh"

  u_input=$(get_input radio "Wanda: Config" "source,screen,download,screen resolution,offline mode")

  case "$u_input" in
    "source")
    u_input=$(get_input radio "Wanda: Choose a source" "4chan,dynamic,earthview,imagemagick,local,picsum,reddit,wallhaven")
    config_set "source" "$u_input"
    ;;
    "screen")
    u_input=$(get_input radio "Wanda: Choose which screen(s) you want to set wallpaper" "home,lock,both")
    config_set "screen" "$u_input"
    ;;
    "download")
    u_input=$(get_input radio "Wanda: Save downloaded wallpapers?" "true,false")
    config_set "keep" "$u_input"
    ;;
    "screen resolution")
    resolution=$(get_input radio "Wanda: Choose screeen resolution" "480x800,540x960,720x1280,768x1280,1080x1920,1280x720,1440x2560,1920x1080,2960x1440")
    IFS="x"
    read -ra strarr <<< "$resolution"
    config_set "width" "${strarr[0]}"
    config_set "height" "${strarr[1]}"
    ;;
    "offline mode")
    u_input=$(get_input radio "Wanda: Offline mode" "off,local,imagemagick")
    config_set "offline_mode" "$u_input"
    ;;
  esac





}

# entry
u_input=$(get_input radio "🪄 Wanda 🪄" "✨Apply wallpaper,⚙️ Configure wanda,⚙️ Configure source,🌌 Setup dynamic walls,📝 View Readme / Report Issue")
case "$u_input" in
  "✨Apply wallpaper")
  . "$SCRIPT_DIR/wanda.sh"
  ;;
  "⚙️ Configure wanda")
  setup_wanda
  ;;
  "⚙️ Configure source")
  u_input=$(get_input radio "Select source to config" "4chan,dynamic,imagemagick,local,picsum,reddit,wallhaven")
  export CONFIG_FILE="$SCRIPT_DIR/sources/$u_input/config"
  bash "$SCRIPT_DIR/sources/$u_input/ui.sh"
  ;;
  "🌌 Setup dynamic walls")
  bash "$SCRIPT_DIR/tools/setup-dynamic-walls.sh"
  ;;
  "📝 View Readme / Report Issue")
  termux-open "https://git.io/wanda"
  ;;
esac
