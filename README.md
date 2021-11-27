# wanda
Bash script to set randomly picked wallpaper using [termux](https://github.com/termux/termux-app)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ksyko/wanda) ![GitHub](https://img.shields.io/github/license/ksyko/wanda) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/e5aacd529ce04f3fb8c0f9ce6a3bdd9e)](https://www.codacy.com/gh/ksyko/wanda/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ksyko/wanda&amp;utm_campaign=Badge_Grade)

## Installation

1. Install [termux](https://f-droid.org/en/packages/com.termux/) and [termux-api](https://f-droid.org/en/packages/com.termux.api/)

2. Install wanda
```
termux-setup-storage
curl https://gitlab.com/kshib/wanda/uploads/53a3777494b909f07e0ca37f3e6c2017/wanda-lite_0.1_all.deb
pkg in ./wanda-lite_0.1_all.deb
```


## Usage

  wanda [-s source] [-t search term] [-o] [-l] [-h]
  -s  source      unsplash,wallhaven,reddit,local
  -t  t           search term.
  -o  homescreen  set wallpaper on homescreen
  -l  lockscreen  set wallpaper on lockscreen
  -h  help        this help message

Examples:
  wanda -s wallhaven -t mountain -hl
  wanda -s local -t folder/path -h

Tips:
* None of the parameters are mandatory. Default source is unsplash.
* Multiple search terms are possible on unsplash and wallhaven using ','

## Supported sources

- [local](https://wiki.termux.com/wiki/Termux-setup-storage)
- [reddit](https://old.reddit.com/)
- [unsplash](https://unsplash.com/)
- [wallhaven](https://wallhaven.cc/)

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

```
apt install termux-create-package
git clone https://gitlab.com/kshib/wanda.git -b lite
chmod +x wanda
termux-create-package manifest.json
```
[More info](https://github.com/termux/termux-create-package)
