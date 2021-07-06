#!/data/data/com.termux/files/usr/bin/bash
. "$SCRIPT_DIR/tools/util.sh"

# board
u_input=$(get_input "radio" "4chan: Choose board" "wg,w,hr")
config_set "board" "$u_input"

# thread
api="https://a.4cdn.org/wg/catalog.json"
res=$(curl -s "$api")
posts_count=$(echo "$res" | jq '.[0].threads | length')
posts=""
threads=$(echo "$res" | jq -cr '.[].threads[] | { no: .no, des: .semantic_url }')
for thread in $threads; do
  n=$(echo "$thread" | jq '.no')
  d=$(echo "$thread" | jq --raw-output '.des')
  posts="${posts}$d $n,"
done
IFS=" "
read -ra strarr <<< "$posts"
config_set "colors" "${strarr[1]}"

u_input=$(get_input "radio" "4chan: Choose thread" "${posts::-1}")
config_set "board" "$u_input"
