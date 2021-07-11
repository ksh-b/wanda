#!/data/data/com.termux/files/usr/bin/bash

# get saved slug
link=$(config_get "next")

# if no slug is saved, get new one
if [[ -z $link ]]; then
  link=$(curl -s "https://earthview.withgoogle.com" | xmllint --html --xpath 'string(//a[@title="Next image"]/@href)' - 2>/dev/null)
fi

# get image and next slug
api="https://earthview.withgoogle.com/_api$link.json"
res=$(curl -s "${api}")
url=$(echo "$res" | jq --raw-output ".photoUrl")
slug=$(echo "$res" | jq --raw-output ".slug")
next_slug=$(echo "$res" | jq --raw-output ".nextSlug")
config_set "next" "/$next_slug"

# download and rotate the image
filepath="$SCRIPT_DIR/downloads/${slug}.jpg"
curl -s "$url" -o "$filepath"
mogrify -rotate 90 "$filepath"

# set rotated image as wallpaper
case "$screen" in
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

# keep or remove downloaded file as per config
if [ "$keep" = "false" ]; then
  rm "$filepath"
fi
exit 0
