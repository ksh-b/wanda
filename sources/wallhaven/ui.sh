#!/data/data/com.termux/files/usr/bin/bash
CONFIG_FILE=$SCRIPT_DIR/sources/wallhaven/config
. "$CONFIG_FILE"
. "$SCRIPT_DIR/util.sh"

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
u_sorting=config_get "sorting"
if [ "$u_sorting" = "toplist" ]; then
  u_input=$(get_input radio "Wallhaven: Choose top range" "1d,3d,1w,1M,3M,6M,1y")
  config_set "topRange" "$u_input"
fi

# ratios
u_input=$(get_input radio "Wallhaven: Choose ratio" "9x16,10x16,9x18")
config_set "ratios" "$u_input"

# colors
u_input=$(get_input radio "Wallhaven: Choose color"
"
Blood Red-660000,
Dark Red-990000,
Rosso Corsa-CC0000,
Persian Red-CC3333,
French Rose-EA4C88,
Plum-993399,
Rebecca Purple-663399,
Blue Pigment-333399,
True Blue-0066CC,
Blue Green-0099CC,
Medium Turquoise-66CCCC,
Sheen Green-77CC33,
Olive Drab-669900,
Dark Green-336600,
Antique Bronze-666600,
Citron-999900,
Acid Green-CCCC33,
Lemon Glacier-FFFF00,
Sunglow-FFCC33,
Yellow Orange Color Wheel-FF9900,
Safety Orange Blaze Orange-FF6600,
Chocolate Web-CC6633,
Golden Brown-996633,
Chocolate Traditional-663300,
Black-000000,
Spanish Gray-999999,
Light Gray-CCCCCC,
White-FFFFFF,
Independence-424153,
"
)
IFS="-"
read -ra strarr <<< "$u_input"
config_set "colors" "${strarr[1]}"
