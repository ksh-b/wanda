# wanda
Bash script to set randomly picked wallpaper using [termux](https://github.com/termux/termux-app)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7c33b1c42b8d4a3fb80c74c9c8ececb9)](https://www.codacy.com/gl/kshib/wanda/dashboard?utm_source=gitlab.com&amp;utm_medium=referral&amp;utm_content=kshib/wanda&amp;utm_campaign=Badge_Grade)

## Installation

1. Install [termux](https://f-droid.org/en/packages/com.termux) and [termux-api](https://f-droid.org/en/packages/com.termux.api)

2. Install wanda

- Download latest release from [gitlab](https://gitlab.com/kshib/wanda/-/releases) or [package-cloud](https://packagecloud.io/kshib/wanda-main)
- Install it
```
termux-setup-storage
pkg in ./wanda_version_all.deb
```

## Usage
```
wanda [-s source] [-t search term] [-o] [-l] [-h]
  -s  source      unsplash,wallhaven,reddit
                  4chan,canvas,earthview,local
  -t  term        search term
  -o  homescreen  set wallpaper on homescreen
  -l  lockscreen  set wallpaper on lockscreen
  -d  download    save current wallpaper to storage
  -h  help        this help message
  -u  update      update wanda
  -v  version     current version
```

## Examples:
- No need for parameters. Random image from unsplash.
  wanda
- First two letters of source is fine (earthview in this case)
  wanda -s ea
- Search terms/tags can be specified using t
  wanda -sun -t eiffel tower
- However some sources have different meaning for t
  imgur takes gallery id. eg: https://imgur.com/gallery/[L8ystCU]
  local takes path wrt $HOME. eg: [storage/shared/Downloads]
  4chan takes full thread url. eg: [https://boards.4chan.org/wg/thread/6872254]
  artstation takes author id. eg: https://www.artstation.com/[huniartist]

## Notes
- By default the source is [unsplash](https://unsplash.com).
- Please be aware that sources like 4chan, artstation or wallhaven may have inapt images sometimes.

## Supported sources

- [4chan](https://boards.4chan.org)
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

0. You might have to 'Acquire Wakelock' from the termux notification for this to run properly.
1. Install:
```
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
git clone https://github.com/termux/termux-create-package.git
git clone https://gitlab.com/kshib/wanda.git
cd wanda
chmod +x wanda
../termux-create-package/termux-create-package manifest.json
```
