#!/data/data/com.termux/files/usr/bin/bash
. "$SCRIPT_DIR/tools/util.sh"
select_wallhaven_options() {
  o1=1
  o2=0
  o3=0
  case "$1" in
  *$2*)
    o1=1
    ;;
  *$3*)
    o2=1
    ;;
  *$4*)
    o3=1
    ;;
  esac
  selection="$o1$o2$o3"
}

# categories
u_input=$(get_input checkbox "Wallhaven: Choose categories" "general,anime,people")
select_wallhaven_options "$u_input" "general" "anime" "people"
config_set "categories" "$selection"

# purity
u_input=$(get_input checkbox "Wallhaven: Choose purity" "sfw,sketchy,nsfw")
select_wallhaven_options "$u_input" "sfw" "sketchy" "nsfw"
config_set "purity" "$selection"

# sorting
u_input=$(get_input radio "Wallhaven: Choose sorting" "date_added,relevance,random,views,favorites,toplist")
config_set "sorting" "$u_input"

# order
u_input=$(get_input radio "Wallhaven: Choose order" "desc,asc")
config_set "order" "$u_input"

# topRange
u_sorting=$(config_get "sorting")
if [ "$u_sorting" = "toplist" ]; then
  u_input=$(get_input radio "Wallhaven: Choose top range" "1d,3d,1w,1M,3M,6M,1y")
  config_set "topRange" "$u_input"
fi

# ratios
u_input=$(get_input radio "Wallhaven: Choose ratio" "9x16,10x16,9x18")
config_set "ratios" "$u_input"

# colors
u_input=$(get_input radio "Wallhaven: Choose color" "maroon-660000,dark_red-990000,orange_red-CC0000,fire_brick-CC3333,hot_pink-EA4C88,purple-993399,rebecca_purple-663399,midnight_blue-333399,royal_blue-0066CC,steel_blue-0099CC,medium_turquoise-66CCCC,yellow_green-77CC33,olive_drab-669900,dark_green-336600,dark_olive-666600,olive-999900,yellow_green-CCCC33,yellow-FFFF00,gold-FFCC33,orange-FF9900,orange_red-FF6600,chocolate-CC6633,sienna-996633,saddle_brown-663300,black-000000,dark_gray-999999,light_gray-CCCCCC,white-FFFFFF,dark_slate_gray-424153,")
IFS="-"
read -ra strarr <<<"$u_input"
config_set "colors" "${strarr[1]}"
