#!/data/data/com.termux/files/usr/bin/bash
. "$SCRIPT_DIR/tools/util.sh"

# grayscale
u_input=$(get_input "radio" "Picsum: Apply grayscale" "true,false")
config_set "grayscale" "$u_input"

# blur
u_input=$(get_input "counter" "Picsum: Apply blur? (0 for off)" "0,10,0")
config_set "blur" "$u_input"
