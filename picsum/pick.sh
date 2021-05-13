. ./picsum/config
seed=$(xxd -l 8 -c 8 -p < /dev/random)
api="https://picsum.photos/seed/$seed/$width/$height"
echo $api
url=$(curl -Ls -o /dev/null -w %{url_effective} $api)
echo $url
