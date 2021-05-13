#!/data/data/com.termux/files/usr/bin/bash
mkdir -p wallpaper
. ./wallhaven.config
cd wallpaper && rm *
api="https://wallhaven.cc/api/v1/search?apikey=$api_key&categories=$categories&purity=$purity&ratios=$ratios&page=$page&sorting=$sorting&order=$order&topRange=$topRange&atleast=$atleast&resolutions=$resolutions&colors=$colors&seed=$seed"
url=$(curl -s $api | jq --raw-output '.data[0].path')
case $screen in
    both)
        termux-wallpaper -lu $url
        termux-wallpaper -u $url
        ;;
    home)
        termux-wallpaper -u $url
        ;;
    lock)
        termux-wallpaper -lu $url
        ;;
esac
