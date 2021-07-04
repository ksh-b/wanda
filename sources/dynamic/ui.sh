#!/data/data/com.termux/files/usr/bin/bash

# TODO: ask for setup if no imagesets present

imagesets=""
# imageset
for f in "$SCRIPT_DIR"sources/dynamic/images/*; do
    imagesets="$imagesets""$(basename "$f,")"
done

u_input=$(get_input radio "Dynamic: Choose a set" "$imagesets")
config_set "imageset" "$u_input"
