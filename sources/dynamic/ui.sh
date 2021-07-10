#!/data/data/com.termux/files/usr/bin/bash
. "$SCRIPT_DIR/tools/util.sh"

# TODO: ask for setup if no imagesets present

imagesets=""
# imageset
for f in "$SCRIPT_DIR"/sources/dynamic/images/*; do
    imagesets="$imagesets$(basename "$f,")"
done

u_input=$(get_input radio "Dynamic: Choose a set" "${imagesets::-1}")
config_set "imageset" "$u_input"
