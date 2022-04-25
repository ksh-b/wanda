# wanda
Bash script to set randomly picked wallpaper using [termux](https://github.com/termux/termux-app)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7c33b1c42b8d4a3fb80c74c9c8ececb9)](https://www.codacy.com/gl/kshib/wanda/dashboard?utm_source=gitlab.com&amp;utm_medium=referral&amp;utm_content=kshib/wanda&amp;utm_campaign=Badge_Grade)

## Desktop version
Try the desktop version [here](https://gitlab.com/kshib/wanda/-/tree/desktop). Should work on most linux systems.

## Installation
1. Install [termux](https://f-droid.org/en/packages/com.termux) and [termux-api](https://f-droid.org/en/packages/com.termux.api)

2. Install wanda
```
curl https://kshib.gitlab.io/termux-repo/install.sh | sh
pkg in wanda
```

## Usage
```
wanda [-s source] [-t search term] [-o] [-l] [-d] [-h] [-v] [-x]
  -s  source      unsplash,wallhaven,reddit
                  4chan,canvas,earthview,imgur
                  artstation,local, 500px
  -t  term        search term
  -o  homescreen  set wallpaper on homescreen only
  -l  lockscreen  set wallpaper on lockscreen only
  -d  download    save current wallpaper to storage
  -v  version     current version
  -x  list        print supported sources
```

## Examples:
- No need for parameters. Random image from unsplash.

  ```
  wanda
  ```
- First two letters of source is fine (earthview in this case)
  ```
  wanda -s ea
  ```
- Search terms/tags can be specified using t
  ```
  wanda -s un -t eiffel tower
  ```
- However some sources have different meaning for t
  - imgur takes gallery id. eg: [L8ystCU]
  - local takes path wrt $HOME. eg: [storage/shared/Downloads]
  - 4chan takes full thread url. eg: [https://boards.4chan.org/wg/thread/6872254]
  - canvas takes texture name. eg: plasma

## Notes
- By default the source is [unsplash](https://unsplash.com).
- Some sources may have inapt images. Use them at your own risk.

## Supported sources

- [4chan](https://boards.4chan.org)
- [500px](https://500px.com)
- [artstation](https://artstation.com)
- [canvas](https://github.com/adi1090x/canvas)
- [earthview](https://earthview.withgoogle.com)
- [imgur](https://imgur.com)
- [local](https://wiki.termux.com/wiki/Termux-setup-storage)
- [reddit](https://reddit.com)
- [unsplash](https://unsplash.com)
- [wallhaven](https://wallhaven.cc)

## Automate

* To set wallpaper at regular intervals automatically:

1. Install:
```
termux-wake-lock
pkg in cronie termux-services nano
sv-enable crond
```
2. Edit crontab
```
crontab -e
```
3. Set your desired interval. For hourly:
```
@hourly wanda -t mountains
```
[(more examples)](https://crontab.guru/examples.html)

4. ctrl+o to save, ctrl+x to exit the editor

## Build
python and [termux-create-package](https://github.com/termux/termux-create-package) are needed
```
pip install termux-create-package
git clone https://gitlab.com/kshib/wanda.git && cd wanda
termux-create-package manifest.json
```

## Uninstall
```
pkg un wanda
rm $PREFIX/etc/apt/sources.list.d/kshib.list
```

## License
MIT
