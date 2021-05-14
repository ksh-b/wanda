# wanda
Simple script to set random wallpaper using [termux](https://github.com/termux/termux-app)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/ksyko/wanda) ![GitHub](https://img.shields.io/github/license/ksyko/wanda)

<details open>
<summary>Installation</summary>
<br>
  
1. Get requirements and the script:
```
pkg up
pkg in termux-api git curl jq file
git clone https://github.com/ksyko/wanda.git
```
2. Edit the wanda.config file to your liking. See below sections for more details.
3. Run the script
```
cd wanda
sh wanda.sh
```

</details>


<details>
<summary>Sources and editing config files</summary>
<br>
  
  * wanda
    * source - set source of your wallpaper. [**wallhaven**, chan, picsum, reddit, local]
    * screen - screens to set wallpaper. [home, lock, **both**]
  * [wallhaven](https://wallhaven.cc/)
    * all the options are specified [here](https://wallhaven.cc/help/api)
    * api key is **not** mandatory
  * [4chan](https://4chan.org/)
    * board - board where the thread belongs
    * thread - thread number 
    * example: https://boards.4chan.org/wg/thread/7738706
      * board=wg
      * thread=7738706
  * [picsum](https://picsum.photos/)
    * height - desired image height
    * width - desired image width
  * [reddit](https://old.reddit.com/)
    * sub - subreddit name
    * sort - sort by [hot, new, rising, controversial, top, gilded]
  * local
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
0 * * * *   cd path/to/wanda && $PREFIX/bin/sh wanda.sh
```
5. ctrl+o to save, ctrl+x to exit the editor


</details>

