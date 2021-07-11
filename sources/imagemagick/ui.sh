#!/data/data/com.termux/files/usr/bin/bash
. "$SCRIPT_DIR/tools/util.sh"

# sort
u_input=$(get_input radio "pattern" "solid,linear,radial,twisted,bilinear,plasma,blurred,gradient1,gradient2,plasma1,plasma2")
config_set "pattern" "$u_input"
