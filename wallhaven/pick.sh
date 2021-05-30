#!/data/data/com.termux/files/usr/bin/bash
echo $SCRIPT_DIR
. $SCRIPT_DIR/wallhaven/config

# get parameters with a value
keys=(apikey q categories purity sorting order topRange atleast resolutions ratios colors page seed)
for i in "${keys[@]}";
  do if [ -n "${!i}" ]; then
    params="${params}$i=${!i}&"
  fi
done

# make request with provided parameters
api="https://wallhaven.cc/api/v1/search?"
res=$(curl -s "${api}${params}")
echo $res

# use a random number if sorting is not random
if [ "$sorting" != "random" ]; then
  last=$(echo $res | jq --raw-output '.meta.last_page')
  page=$(shuf -i 1-$last -n 1)
  res=$(curl -s "${api}${params}&page=$page")
  limit=$(echo $res | jq --raw-output '.meta.per_page')
  rand=$(shuf -i 1-$limit -n 1)
else
  rand=0
fi

# get wallpaper link
url=$(echo $res | jq --raw-output ".data[$rand].path")
echo $url
