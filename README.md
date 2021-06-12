# wanda

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6d0c308cef4e44909a2b139294aa368f)](https://app.codacy.com/gh/ksyko/wanda?utm_source=github.com&utm_medium=referral&utm_content=ksyko/wanda&utm_campaign=Badge_Grade_Settings)

Simple script to set random wallpaper using [termux](https://github.com/termux/termux-app)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ksyko/wanda) ![GitHub](https://img.shields.io/github/license/ksyko/wanda)

<details open>
<summary>Installation</summary>
<br>

1. Install [termux](https://f-droid.org/en/packages/com.termux/) and [termux-api](https://f-droid.org/en/packages/com.termux.api/)
2. Open termux and paste the following:

```
curl -L https://git.io/JZXCp | bash
```
  
2. Edit the config files to your liking. See below sections for more details.
3. Run the script
```
cd wanda
bash wanda.sh
```

</details>


<details>
<summary>Sources and editing config files</summary>
<br>
  config files for sources are present in their respective folders.
  format is key=value

  * /config
    * source - set source of your wallpaper. [wallhaven, chan, picsum, reddit, local]
    * screen - screens to set wallpaper. [home, lock, both]
    * keep - save used wallpaper to local [true, false]
    * offline_use_local - use local wallpapers when offline (set local directory in /local/config) [true, false]
    * autocrop - for autocrop and related config, see [autocrop](#autocrop) section.
  * /[wallhaven](https://wallhaven.cc/)/config
    * all the options are specified [here](https://wallhaven.cc/help/api)
  * /[chan](https://4chan.org/)/config
    * board - board where the thread belongs
    * thread - thread number
  * /[picsum](https://picsum.photos/)/config
    * height - desired image height
    * width - desired image width
  * /[reddit](https://old.reddit.com/)/config
    * sub - subreddit name
    * sort - sort by [hot, new, rising, controversial, top, gilded]
  * /local/config
    * images_path - folder path to get images from


</details>

<details>
<summary>Automate</summary>
<br>

* To set wallpaper at regular intervals automatically:

0. You might have to 'Acquire Wakelock' from the termux notification for this to run properly.
1. Install:
```
pkg in cronie termux-services nano
sv-enable crond
```
2. Check if crond is running
```
pidof crond
```
3. Edit crontab
```
crontab -e
```
4. Set your desired interval [(guide)](https://crontab.guru/#20_4_*_*_*).<br>Example: For hourly:
```
0 * * * *   cd storage/shared/wanda && $PREFIX/bin/bash wanda.sh
```
5. ctrl+o to save, ctrl+x to exit the editor


</details>

<details>
<summary>Autocrop [Optional]</summary>
<br>
  
  Autocrop tries to find the subject in the image and crops the image accordingly. <br>
  Useful for when the image is horizontal and subject is at either end of the image. [Example](https://miro.medium.com/max/2048/0*sRE3XCJI0s00wFb-). <br>
  Imagga API provides the co-ordinates for crop. Imagemagick crops the images. <br>
  
  * `pkg in imagemagick`
  * Create [imagga](https://imagga.com/auth/signup) account. Its free to sign up, [one time emails](https://privacytoolslist.com/#one-time-emails) can work too 😉 
  * Once the account is created, go to [dashboard](https://imagga.com/profile/dashboard). Copy key and secret.
  * open /config and edit the following
    * Enable autocrop: set `autocrop` to `true`.
    * Set `imagga_key` value as `key`:`secret`.
    * Set your device screen `height` and `width`.
  
</details>
