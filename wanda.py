import os
import random
import subprocess
from datetime import datetime
from random import randrange
import requests
from lxml import etree

source = "unsplash"
query = ""
home = "true"
lock = "true"
version = 0.45
no_results = "No results found. Try another source/term."
user_agent = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"}
tmp = f"{os.environ.get('PREFIX')}/tmp"
CONFIG_FILE = f"{os.environ.get('PREFIX')}/etc/wanda.conf"


def usage():
    print("wanda ($version)")
    print("Usage:")
    print("  wanda [-s source] [-t search term] [-o] [-l] [-d] [-h] [-v] [-i]")
    print("  -s  source      unsplash,wallhaven,reddit")
    print("                  4chan,canvas,earthview,imgur")
    print("                  artstation,local, 500px, imsea")
    print("  -t  term        search term")
    print("  -o  homescreen  set wallpaper on homescreen only")
    print("  -l  lockscreen  set wallpaper on lockscreen only")
    print("  -d  download    save current wallpaper to storage")
    print("  -h  help        this help message")
    print("  -v  version     current version")
    print("  -i  list        print supported sources and their specific usage")
    print()
    print("Examples:")
    print("  wanda")
    print("  wanda -s earthview")
    print('  wanda -s un -t eiffel tower')
    print("  wanda -s lo -t folder/path")


def is_connected():
    return requests.get("https://detectportal.firefox.com/success.txt") == "success"


def validate_url(url) -> bool:
    return requests.get(url).status_code == 200


def command(string: str) -> str:
    return subprocess.check_output(string.split(" ")).decode()


def config_set(param, url):
    pass


def set_wp_url(url: str):
    validate_url(url)
    if home:
        subprocess.call(f"termux-wallpaper -u {url}", shell=True)
    if lock:
        subprocess.call(f"termux-wallpaper -lu {url}", shell=True)
    config_set("last_wallpaper_path", url)
    config_set("last_wallpaper_time", datetime.now())


def set_wp_file(url: str):
    validate_url(url)
    if home:
        subprocess.call(f"termux-wallpaper -f {url}", shell=True)
    if lock:
        subprocess.call(f"termux-wallpaper -lf {url}", shell=True)
    config_set("last_wallpaper_time", datetime.now())


def size():
    if is_android():
        hxw = command("getprop 'persist.vendor.camera.display.umax'")
        if hxw is not None:
            return f"{hxw.split('x')[1]}x{hxw.split('x')[0]}"
        return "1440x2960"

    try:
        dimensions = filter(lambda l: "dimensions" in l, subprocess.check_output("xdpyinfo").decode().split("\n"))
        return list(dimensions)[0].split()[1]
    except Exception:
        return "2560x1440"


def is_android():
    return os.environ.get('TERMUX_VERSION') is not None


def contains(word: str, match_all: bool, desired: list) -> bool:
    return match_all in list(map(lambda w: w not in word if w.startswith("!") else w in word, desired))


def wallhaven(search=""):
    api = "https://wallhaven.cc/api/v1/search?sorting=random"
    ratios = "portrait" if is_android() else "landscape"
    response = requests.get(f"{api}&ratios={ratios}&q={search}").json()
    return response["data"][0]["path"]


def unsplash(search=""):
    api = f"https://source.unsplash.com/random/{size()}/?{search}"
    return requests.get(api).url


def fourchan_auto():
    catalog = "https://a.4cdn.org/wg/catalog.json"
    response: list = requests.get(catalog).json()
    pages = len(response)
    thread = f"https://boards.4chan.org/wg/thread/{response[0]['threads'][1]['no']}"
    for page in range(pages):
        for thread in response[page]["threads"]:
            semantic_url = thread["semantic_url"]
            if is_android() and contains(semantic_url, True, ["mobile", "phone", "!official-image-modification"]):
                thread = f"https://boards.4chan.org/wg/thread/{thread['no']}"
                break
            elif not is_android():
                page = randrange(pages)
                thread = random.choice(response[page]["threads"])
                semantic_url = thread["semantic_url"]
                if not contains(semantic_url, True, ["mobile", "phone", "official-image-modification"]):
                    thread = f"https://boards.4chan.org/wg/thread/{thread['no']}"
                    break
    return thread


def fourchan(thread=""):
    if not thread:
        thread = fourchan_auto()
    posts = requests.get(f"{thread}.json").json()["posts"]
    for _ in posts:
        post = random.choice(posts)
        if "ext" in post and contains(post["ext"], False, [".jpg", ".png"]):
            return f"https://i.4cdn.org/wg/{post['tim']}{post['ext']}"


def subreddit():
    if is_android():
        return "mobilewallpaper+amoledbackgrounds+verticalwallpapers"
    return "wallpaper+wallpapers+earthporn+spaceporn+skyporn+minimalwallpaper"


def reddit_search(subreddit, search=None):
    reddit = "https://old.reddit.com/r/"
    if search:
        common_param = "&restrict_sr=on&sort=relevance&t=all"
        search_api = "/search.json?q="
        return f"{reddit}{subreddit}{search_api}{search}{common_param}"
    else:
        return f"{reddit}{subreddit}.json"


def reddit(search=""):
    subreddits = subreddit()
    if search.startswith("r/"):
        subreddits = search
        search = ""
    api = f"{reddit_search(subreddits, search)}"
    posts = requests.get(api, headers=user_agent).json()["data"]["children"]
    return random.choice(posts)["data"]["url"]


def imgur(search=None):
    alt = "rimgo.pussthecat.org"
    if not search.islower():
        imgur_url = f"https://{alt}/gallery/{search}"
    else:
        api = reddit_search("wallpaperdump", search)
        if is_android():
            if not search:
                search = ""
            api = f"{reddit_search('wallpaperdump', '{0} {1}'.format(search, random.choice(['phone', 'mobile'])))}"
        imgur_url = ""
        while not contains(imgur_url, True, ["imgur.com"]):
            imgur_url = random.choice(requests.get(api, headers=user_agent).json()["data"]["children"])["data"]["url"]

    tree = etree.HTML(requests.get(imgur_url.replace("imgur.com", f"{alt}")).content)
    return f"https://{alt}" + random.choice(tree.xpath("//div[@class='center']//img/@src"))
