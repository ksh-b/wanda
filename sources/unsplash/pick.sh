#!/data/data/com.termux/files/usr/bin/bash
case $mode in
collection)
  api="https://source.unsplash.com/collection/$collection/$size"
  ;;
search)
  api="https://source.unsplash.com/$size/?$terms"
  ;;
user)
  api="https://source.unsplash.com/user/$user/$size"
  ;;
likes)
  api="https://source.unsplash.com/user/$user/likes/$size"
  ;;
regular)
  api="https://source.unsplash.com/$regular?$terms"
  ;;
esac
url=$(curl -Ls -o /dev/null -w %{url_effective} "$api")
echo "$url"
