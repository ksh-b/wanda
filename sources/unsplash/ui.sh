#!/data/data/com.termux/files/usr/bin/bash
. "$SCRIPT_DIR/tools/util.sh"

# mode
u_input=$(get_input radio "Unsplash: Select mode" "collection,search,user,likes,regular")
config_set "mode" "$u_input"

case $u_input in
  "collection")
    u_input=$(get_input text "Unsplash: Enter collection id" "$(config_get "collection")")
    config_set "collection" "$u_input"
  ;;
  "search")
    u_input=$(get_input text "Unsplash: Enter search terms (comma separated)" "$(config_get "terms")")
    config_set "terms" "$u_input"
  ;;
  "user")
    u_input=$(get_input text "Unsplash: Enter collection id" "$(config_get "user")")
    config_set "user" "$u_input"
  ;;
  "likes")
    u_input=$(get_input text "Unsplash: Enter collection id" "$(config_get "likes")")
    config_set "likes" "$u_input"
  ;;
  "regular")
    u_input=$(get_input radio "Unsplash: Enter regular" "daily,weekly")
    config_set "collection" "$u_input"
  ;;
esac
