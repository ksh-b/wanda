#!/data/data/com.termux/files/usr/bin/bash
. "$SCRIPT_DIR/tools/util.sh"

# board
u_input=$(get_input "radio" "4chan: Choose board" "wg,w,hr")
config_set "board" "$u_input"

# thread
api="https://a.4cdn.org/$u_input/catalog.json"
res=$(curl -s "$api")
posts_count=$(echo "$res" | jq '.[0].threads | length')
posts=""
threads=$(echo "$res" | jq -cr '.[0].threads[] | { no: .no, des: .semantic_url }')

echo "Generating thread list. Please wait."
i=0
for thread in $threads; do
  i=$((i+1))
  n=$(echo "$thread" | jq '.no')
  d=$(echo "$thread" | jq --raw-output '.des')
  posts="${posts}$d $n,"
  echo "$i/$posts_count"
done


u_input=$(get_input "radio" "4chan: Choose thread" "${posts::-1}")
IFS=" "
read -ra strarr <<< "$u_input"
config_set "board" "${strarr[1]}"
