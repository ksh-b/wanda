#!/data/data/com.termux/files/usr/bin/bash

# sub
u_input=$(get_input radio "Reddit: Choose a subreddit"
"
iWallpaper,
MobileWallpaper,
Verticalwallpapers,
Amoledbackgrounds,
AnimePhoneWallpapers,
ComicWalls,
wallpaper+wallpapers
")
config_set "sub" "$u_input"

# sort
u_input=$(get_input radio "sort" "hot,new,rising,top,gilded")
config_set "sort" "$u_input"
