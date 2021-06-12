#!/data/data/com.termux/files/usr/bin/bash
. "$SCRIPT_DIR/picsum/config"
seed=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 10 ; echo '')
api="https://picsum.photos/seed/$seed/$width/$height"
url=$(curl -Ls -o /dev/null -w %{url_effective} "$api")
echo "$url"
