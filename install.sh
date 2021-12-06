#!/data/data/com.termux/files/usr/bin/bash

check_connectivity() {
  curl -s "https://detectportal.firefox.com/success.txt" 1>/dev/null
  if [ "$?" != 0 ]; then
    echo "Please check your internet connection and try again."
    exit 1
  fi
}

update() {
  pkg in curl jq
  check_connectivity
  res=$(curl -s curl "https://gitlab.com/api/v4/projects/29639604/repository/files/manifest.json/raw")
  latest_version=$(echo "$res" | jq --raw-output ".version")
  res=$(curl -s curl "https://gitlab.com/api/v4/projects/29639604/releases/v$latest_version/assets/links")
  link=$(echo "$res" | jq --raw-output ".[].url")
  binary=$(basename "$link")
  curl -L "$link" -o "$binary"
  pkg in "./$binary"
  rm "$binary"
  wanda -h
}

update
