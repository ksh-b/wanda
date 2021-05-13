#!/data/data/com.termux/files/usr/bin/bash
. ./wallhaven/config
api="https://wallhaven.cc/api/v1/search?apikey=$api_key&q=$q&categories=$categories&purity=$purity&ratios=$ratios&page=$page&sorting=$sorting&order=$order&topRange=$topRange&atleast=$atleast&resolutions=$resolutions&colors=$colors&seed=$seed"
url=$(curl -s $api | jq --raw-output '.data[0].path')
echo $url
