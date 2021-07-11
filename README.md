# wanda
Bash script to set randomly picked wallpaper using [termux](https://github.com/termux/termux-app)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ksyko/wanda) ![GitHub](https://img.shields.io/github/license/ksyko/wanda) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/e5aacd529ce04f3fb8c0f9ce6a3bdd9e)](https://www.codacy.com/gh/ksyko/wanda/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ksyko/wanda&amp;utm_campaign=Badge_Grade)

## Installation

1. Install [termux](https://f-droid.org/en/packages/com.termux/) and [termux-api](https://f-droid.org/en/packages/com.termux.api/)
2. Read the [installation script](https://git.io/wanda-install) and then run the same in termux:

```
termux-setup-storage
curl -L https://git.io/wanda-install | bash
```

## Usage

1. Navigate to where you installed the script
  ```
  cd $HOME/storage/shared/scripts/wanda
  ```
2. From here you can use the GUI for setup or continue in shell. For GUI:
```
bash ui.sh
```
3. For Shell:
```
nano config
```
4. Navigate to your preferred source and edit its config if present. Example for wallhaven
```
nano sources/wallhaven/config
```
5. Apply the wallpaper
```
bash wanda.sh
```

## Supported sources
[4chan](https://4chan.org/)

[dynamic](https://github.com/GitGangGuy/dynamic-wallpaper-improved)

[earthview](https://earthview.withgoogle.com/)

[imagemagick](https://legacy.imagemagick.org/Usage/canvas/)

[local](https://wiki.termux.com/wiki/Termux-setup-storage)

[picsum](https://picsum.photos/)

[reddit](https://old.reddit.com/)

[wallhaven](https://wallhaven.cc/)

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
0 * * * *   cd storage/shared/wanda && $PREFIX/bin/bash wanda.sh
```
[(more examples)](https://crontab.guru/examples.html)

4. ctrl+o to save, ctrl+x to exit the editor


## Autocrop [Optional]

  Autocrop tries to find the subject in the image and crops the image accordingly. <br>
  Useful for when the image is horizontal and subject is at either end of the image. [Example](https://miro.medium.com/max/2048/0*sRE3XCJI0s00wFb-). <br>

  * Create [imagga](https://imagga.com/auth/signup) account. Its free to sign up, [one time emails](https://privacytoolslist.com/#one-time-emails) can work too and would recommend using one 😉.
  * Once the account is created, go to [dashboard](https://imagga.com/profile/dashboard). Copy key and secret.
  * open /config and edit the following
    * Enable autocrop: set `autocrop` to `true`.
    * Set `imagga_key` value as `key`:`secret`.
    * Set your device screen `height` and `width`.
