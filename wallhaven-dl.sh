#!/data/data/com.termux/files/usr/bin/bash
mkdir -p wallpaper
config=$(cat wallhaven-config.json)
api_key=$(echo $config| jq --raw-output '.api_key')
purity=$(echo $config | jq --raw-output '.purity')
categories=$(echo $config | jq --raw-output '.categories')
sorting=$(echo $config | jq --raw-output '.sorting')
order=$(echo $config | jq --raw-output '.order')
topRange=$(echo $config | jq --raw-output '.topRange')
atleast=$(echo $config | jq --raw-output '.atleast')
resolutions=$(echo $config | jq --raw-output '.resolutions')
ratios=$(echo $config | jq --raw-output '.ratios')
colors=$(echo $config | jq --raw-output '.colors')
page=$(echo $config | jq --raw-output '.page')
seed=$(echo $config | jq --raw-output '.seed')
cd wallpaper && rm *
url="https://wallhaven.cc/api/v1/search?apikey=$api_key&categories=$categories&purity=$purity&ratios=$ratios&page=$page&sorting=$sorting&order=$order&topRange=$topRange&atleast=$atleast&resolutions=$resolutions&ratios=$ratios&colors=$colors&seed=$seed"
op=$(curl -s $url | jq --raw-output '.data[0].path')
wall=$(basename $op)
curl --silent -o $wall $op
termux-wallpaper -lf $wall
termux-wallpaper -f $wall
