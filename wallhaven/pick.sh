#!/data/data/com.termux/files/usr/bin/bash
echo $SCRIPT_DIR
. $SCRIPT_DIR/wallhaven/config
keys=(apikey q categories purity sorting order topRange atleast resolutions ratios colors page seed)
for i in "${keys[@]}";
  do if [ -n "${!i}" ]; then
    params="${params}$i=${!i}&"
  fi
done
api="https://wallhaven.cc/api/v1/search?$params"
res=$(curl -s $api)
limit=$(echo $res | jq --raw-output '.meta.per_page')
rand=$(( $RANDOM % limit + 1 ))
url=$(echo $res | jq --raw-output ".data[$rand].path")
echo $url
