#!/data/data/com.termux/files/usr/bin/bash
mkdir -p wallpaper
. ./wallhaven.config
cd wallpaper && rm *
url="https://wallhaven.cc/api/v1/search?apikey=$api_key&categories=$categories&purity=$purity&ratios=$ratios&page=$page&sorting=$sorting&order=$order&topRange=$topRange&atleast=$atleast&resolutions=$resolutions&colors=$colors&seed=$seed"
op=$(curl -s $url | jq --raw-output '.data[0].path')
echo $op
wall=$(basename $op)
curl --silent -o $wall $op
case $screen in
    both)
        termux-wallpaper -lu $op
        termux-wallpaper -u $op
        echo both
        ;;
    home)
        echo home
        termux-wallpaper -u $op
        ;;
    lock)
        echo lock
        termux-wallpaper -lu $op
        ;;
esac
