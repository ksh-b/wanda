#!/data/data/com.termux/files/usr/bin/bash
. "$SCRIPT_DIR/tools/util.sh"

# collection
u_input=$(get_input text "Unsplash: Enter collection id" "$(config_get "collection")")
config_set "collection" "$u_input"
