# wanda
Bash script to set randomly picked wallpaper using [termux](https://github.com/termux/termux-app)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7c33b1c42b8d4a3fb80c74c9c8ececb9)](https://www.codacy.com/gl/kshib/wanda/dashboard?utm_source=gitlab.com&amp;utm_medium=referral&amp;utm_content=kshib/wanda&amp;utm_campaign=Badge_Grade)

## Installation

1. Install [termux](https://f-droid.org/en/packages/com.termux/) and [termux-api](https://f-droid.org/en/packages/com.termux.api/)

2. Install wanda

- Download latest release from [here](https://gitlab.com/kshib/wanda/-/releases)
- Install it
```
termux-setup-storage
pkg in ./wanda_version_all.deb
```

## Usage
```
wanda [-s source] [-t search term] [-o] [-l] [-h]
  -s  source      [un]splash,[wa]llhaven,[re]ddit,[lo]cal
                  [4c]han,[ca]nvas,[ea]rthview
  -t  term        search term.
  -o  homescreen  set wallpaper on homescreen
  -l  lockscreen  set wallpaper on lockscreen
  -h  help        this help message
  -u  update      update wanda
  -v  version     current version

Examples:
  wanda
  wanda -s ea
  wanda -s un -t eiffel tower -ol
  wanda -s lo -t folder/path -ol
  wanda -s wa -t stars,clouds -ol
  wanda -s 4c -t https://boards.4chan.org/wg/thread/7812495

```

## Supported sources

- [local](https://wiki.termux.com/wiki/Termux-setup-storage)
- [reddit](https://reddit.com)
- [unsplash](https://unsplash.com)
- [wallhaven](https://wallhaven.cc)
- [4chan](https://boards.4chan.org)
- [canvas](https://github.com/adi1090x/canvas)
- [earthview](https://earthview.withgoogle.com)

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
