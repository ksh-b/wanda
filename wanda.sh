#!/data/data/com.termux/files/usr/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
. $SCRIPT_DIR/config
. $SCRIPT_DIR/$source/pick.sh

if [ "$source" = "local" ]; then
  case $screen in
      both)
          termux-wallpaper -f "$filepath"
          termux-wallpaper -lf "$filepath"
          ;;
      home)
          termux-wallpaper -f "$filepath"
          ;;
      lock)
          termux-wallpaper -lf "$filepath"
          ;;
  esac
else
  case $screen in
      both)
          termux-wallpaper -u "$url"
          termux-wallpaper -lu "$url"
          ;;
      home)
          termux-wallpaper -u "$url"
          ;;
      lock)
          termux-wallpaper -lu "$url"
          ;;
  esac
fi
