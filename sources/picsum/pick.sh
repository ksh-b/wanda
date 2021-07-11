#!/data/data/com.termux/files/usr/bin/bash
seed=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 10 ; echo '')
params=""
if [ "$grayscale" = "true" ]; then
  params="grayscale"
fi
if [ "$blur" -gt "0" ]; then
  params="$params&blur=$blur"
fi
api="https://picsum.photos/seed/$seed/$width/$height?$params"
url=$(curl -Ls -o /dev/null -w %{url_effective} "$api")
echo "$url"
