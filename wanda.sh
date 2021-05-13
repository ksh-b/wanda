. ./wanda.config
. ./$source/pick.sh
case $screen in
    both)
        termux-wallpaper -u $url
        termux-wallpaper -lu $url
        ;;
    home)
        termux-wallpaper -u $url
        ;;
    lock)
        termux-wallpaper -lu $url
        ;;
esac
