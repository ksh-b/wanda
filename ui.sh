#!/data/data/com.termux/files/usr/bin/bash
export SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. "$SCRIPT_DIR/tools/util.sh"

setup_wanda() {
  export CONFIG_FILE="$SCRIPT_DIR/config"
  . "$SCRIPT_DIR/tools/util.sh"

  u_input=$(get_input radio "Wanda - Config" "source,screen,download,screen resolution,offline mode")

  case "$u_input" in
    "source")
    u_input=$(get_input radio "Select your wallpaper source" "4chan,dynamic,earthview,imagemagick,local,picsum,reddit,unsplash,wallhaven")
    config_set "source" "$u_input"
    ;;
    "screen")
    u_input=$(get_input radio "Choose which screen(s) you want to set wallpaper" "home,lock,both")
    config_set "screen" "$u_input"
    ;;
    "download")
    u_input=$(get_input radio "Save wallpapers?" "true,false")
    config_set "keep" "$u_input"
    ;;
    "screen resolution")
    resolution=$(get_input radio "Choose screeen resolution" "480x800,540x960,720x1280,768x1280,1080x1920,1280x720,1440x2560,1920x1080,2960x1440")
    IFS="x"
    read -ra strarr <<< "$resolution"
    config_set "width" "${strarr[0]}"
    config_set "height" "${strarr[1]}"
    ;;
    "offline mode")
    u_input=$(get_input radio "Select wallpaper source when offline ('off' for no change)" "off,local,imagemagick")
    config_set "offline_mode" "$u_input"
    ;;
    "<CANCEL>" | *)
    exit 0
    ;;
  esac
}


setup_autocrop() {
  export CONFIG_FILE="$SCRIPT_DIR/config"
  . "$SCRIPT_DIR/tools/util.sh"

  u_input=$(get_input radio "Wanda - Autocrop" "Create Imagga Account,Get API keys,Enter API key")
  case "$u_input" in
    "Create Imagga Account")
      u_input=$(get_input confirm "Redirection" "Please go through the 'Autocrop' section in README if not done already. You will be redirected to imagga to create your account. Proceed?")
      if [ "$u_input" = "yes" ]; then
        termux-open "https://imagga.com/auth/signup"
        exit 0
      fi
    ;;
    "Get API keys")
      u_input=$(get_input confirm "Redirection" "You will be redirected to imagga to get your API keys. Proceed?")
      if [ "$u_input" = "yes" ]; then
        termux-open "https://imagga.com/profile/dashboard"
        exit 0
      fi
    ;;
    "Enter API key")
      u_input=$(get_input confirm "API key and secret" "These will be stored on your device in plain text. Proceed?")
      if [ "$u_input" = "yes" ]; then
        api_key=$(get_input text "API key" "Enter API key")
        api_sec=$(get_input text "API secret" "Enter API Secret")
        config_set "imagga_key" "$api_key:$api_sec"
      fi
    ;;

    "Enable autocrop")
    u_input=$(get_input radio "Enable autocrop" "true,false")
    config_set "autocrop" "$u_input"
    ;;
    "Cleanup")
    u_input=$(get_input radio "Save cropped images to device?" "true,false")
    config_set "keep_crop" "$u_input"
    ;;
    "<CANCEL>" | *)
    exit 0
    ;;
  esac
}

# entry
u_input=$(get_input radio "🪄 Wanda 🪄" "✨Apply wallpaper,⚙️ Configure wanda,⚙️ Configure source,🌇🌆🌃 Setup dynamic walls,🤖✂️ Setup autocrop,📝 View Readme / Report Issue,⏏️ Quit")
case "$u_input" in
  "✨Apply wallpaper")
  . "$SCRIPT_DIR/wanda.sh"
  ;;
  "⚙️ Configure wanda")
  setup_wanda
  ;;
  "⚙️ Configure source")
  u_input=$(get_input radio "Select source to config" "4chan,dynamic,imagemagick,local,picsum,reddit,unsplash,wallhaven")
  export CONFIG_FILE="$SCRIPT_DIR/sources/$u_input/config"
  bash "$SCRIPT_DIR/sources/$u_input/ui.sh"
  ;;
  "🌇🌆🌃 Setup dynamic walls")
  bash "$SCRIPT_DIR/sources/dynamic/setup.sh"
  ;;
  "🤖✂️ Setup autocrop")
  setup_autocrop
  ;;
  "📝 View Readme / Report Issue")
  termux-open "https://git.io/wanda"
  ;;
  "⏏️ Quit" | "<CANCEL>" | *)
  exit 0
  ;;
esac

. "$SCRIPT_DIR/ui.sh"
