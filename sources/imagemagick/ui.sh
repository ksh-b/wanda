#!/data/data/com.termux/files/usr/bin/bash
CONFIG_FILE=$SCRIPT_DIR/sources/imagemagick/config
. "$CONFIG_FILE"
. "$SCRIPT_DIR/util.sh"

# sort
u_input=$(get_input radio "pattern"
"solid,linear,radial,twisted,
bilinear,plasma,blurred,
gradient1,gradient2,plasma1,plasma2"
)
config_set "ImageMagick: Choose a pattern" "$u_input"
