#!/data/data/com.termux/files/usr/bin/bash
CONFIG_FILE=$SCRIPT_DIR/local/config
. "$CONFIG_FILE"
. "$SCRIPT_DIR/util.sh"

# images_path
u_input=$(get_input "text" "Enter folder path for wallpaper (from Internal memory)" "Pictures")
config_set "$CONFIG_FILE" "images_path" "$HOME/storage/shared/$u_input"
