#!/data/data/com.termux/files/usr/bin/bash
. ./wallhaven/config
keys=(apikey q categories purity sorting order topRange atleast resolutions ratios colors page seed)
for i in "${keys[@]}";
  do if [ -n "${!i}" ]; then
    params="${params}$i=${!i}&"
  fi
done
api="https://wallhaven.cc/api/v1/search?$params"
url=$(curl -s $api | jq --raw-output '.data[0].path')
echo $url
