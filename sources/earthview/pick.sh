#!/data/data/com.termux/files/usr/bin/bash
link=$(curl -s "https://earthview.withgoogle.com" | xmllint --html --xpath 'string(//a[@title="Next image"]/@href)' - 2>/dev/null)
api="https://earthview.withgoogle.com/_api$link.json"
res=$(curl -s "${api}")
url=$(echo "$res" | jq --raw-output ".photoUrl")
filepath=$SCRIPT_DIR/downloads/$(basename "$url")
curl -s "$url" -o "$filepath"
mogrify -rotate 90 "$filepath"
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
if [ "$keep" = "false" ]; then
  rm "$filepath"
fi
exit 0
