import argparse
import getopt
import glob
import os
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path
from random import randrange

import requests
from lxml import etree

version = 0.56
user_agent = {"User-Agent": "git.io/wanda"}
content_json = "application/json"
folder = f'{str(Path.home())}/wanda'


def __version__():
    return version


def parser():
    parser_ = argparse.ArgumentParser(description='Set wallpapers')

    parser_.add_argument(
        '-s',
        metavar='source',
        type=str,
        default="unsplash",
        help='Source for wallpaper. -u for all supported sources',
        required=False,
    )
    parser_.add_argument(
        '-t',
        metavar='term',
        type=str,
        default=None,
        help='Search term. -u for more help',
        required=False,
    )
    parser_.add_argument(
        '-d',
        metavar='download',
        type=str,
        default=Path.home(),
        help='Save current wallpaper to home directory or given path',
        required=False,
    )
    parser_.add_argument(
        '-u',
        metavar='usage',
        help='Supported sources and their usage',
        required=False,
        action="store_const",
        const=None
    )
    parser_.add_argument(
        '-v',
        metavar='version',
        help='Current version',
        action="store_const",
        const=None
    )
    if is_android():
        parser_.add_argument(
            '-o',
            help='Set wallpaper on homescreen.',
            required=False,
            action="store_true",
        )
        parser_.add_argument(
            '-l',
            help='Set wallpaper on lockscreen.',
            required=False,
            action="store_true",
        )
    return parser_


def is_connected():
    return requests.get("https://detectportal.firefox.com/success.txt") == "success"


def validate_url(url):
    response = requests.get(url)
    return response if response.status_code == 200 else no_results()


def no_results():
    print("No results found. Try another source/term.")
    exit(1)


def command(string: str) -> str:
    return subprocess.check_output(string.split(" ")).decode()


def short_url(url: str) -> str:
    response = requests.post("https://cleanuri.com/api/v1/shorten", data={"url": url}).json()
    return f"{response['result_url']}" if "result_url" in response else url


def set_wp(url: str, home=True, lock=True):
    if is_android():
        t = "u" if url.startswith("https://") else "f"
        if home:
            subprocess.call(f"termux-wallpaper -{t} {url}", shell=True)
        if lock:
            subprocess.call(f"termux-wallpaper -l{t} {url}", shell=True)
        return
    path = os.path.normpath(f'{folder}/wanda_{time.time()}')
    if not os.path.exists(folder):
        os.mkdir(folder)

    files = glob.glob(f'{folder}/*')
    for f in files:
        os.remove(f)
    with open(path, 'wb') as f:
        print(url)
        f.write(requests.get(url).content)
    import platform
    if platform.system() == "Linux":
        set_wp_linux(path)
    elif platform.system() == "Windows":
        set_wp_win(path)
    else:
        print("Platform not supported")
        exit(1)


def set_wp_win(path):
    import ctypes
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


def set_wp_linux(path):
    if os.environ.get("SWAYSOCK"):
        setter = "eval ogurictl output '*' --image"
    elif os.environ.get("DESKTOP_SESSION").lower == "mate":
        setter = "gsettings set org.mate.background picture-filename"
    elif contains(os.environ.get("DESKTOP_SESSION").lower(), False, ["xfce", "xubuntu"]):
        setter = "xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/workspace0/last-image " \
                 "--set "
    elif os.environ.get("DESKTOP_SESSION").lower() == "lxde":
        setter = "pcmanfm --set-wallpaper"
    elif contains(os.environ.get("DESKTOP_SESSION").lower(), False, ["plasma", "neon", "kde"]):
        return os.system(
            'qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "\n' +
            "var allDesktops = desktops();\n" +
            "print (allDesktops);\n" +
            "for (i=0;i<allDesktops.length;i++) {\n" +
            "d = allDesktops[i];\n" +
            "d.wallpaperPlugin = 'org.kde.image';\n" +
            "d.currentConfigGroup = Array('Wallpaper','org.kde.image','General');\n" +
            f"d.writeConfig('Image', 'file://{path}')\n" +
            '}"'
        )
    elif contains(os.environ.get("DESKTOP_SESSION").lower(), False, ["gnome", "pantheon", "ubuntu", "deepin", "pop"]):
        setter = "gsettings set org.gnome.desktop.background picture-uri"
    else:
        setter = "feh --bg-scale"

    command(f"{setter} {path}")


def size():
    if is_android():
        hxw = command("getprop 'persist.vendor.camera.display.umax'")
        return f"{hxw.split('x')[1]}x{hxw.split('x')[0]}" if hxw is not None else "1440x2960"
    try:
        dimensions = filter(lambda l: "dimensions" in l, subprocess.check_output("xdpyinfo").decode().split("\n"))
        return list(dimensions)[0].split()[1]
    except Exception:
        return "2560x1440"


def is_android():
    return os.environ.get('TERMUX_VERSION') is not None


def is_desktop():
    return not is_android()


def good_size(w, h):
    return (is_android() and w < h) or (is_desktop() and w > h)


def contains(word: str, match_all: bool, desired: list) -> bool:
    matches = list(map(lambda w: w not in word if w.startswith("!") else w in word, desired))
    if not match_all:
        return True in matches
    return set(matches) == {True}


def wallhaven(search=None):
    api = "https://wallhaven.cc/api/v1/search?sorting=random"
    ratios = "portrait" if is_android() else "landscape"
    response = requests.get(f"{api}&ratios={ratios}&q={search or ''}").json()["data"]
    return response[0]["path"] if response else no_results()


def unsplash(search=None):
    api = f"https://source.unsplash.com/random/{size()}/?{search or ''}"
    response = requests.get(api).url
    return response if "source-404" not in response else no_results()


def fourchan_auto(search=None):
    catalog = "https://a.4cdn.org/wg/catalog.json"
    response: list = requests.get(catalog).json()
    pages = len(response)
    for page in range(pages):
        threads = response[page]["threads"]
        if not search or search == "":
            return f"https://boards.4chan.org/wg/thread/{random.choice(threads)['no']}"
        for thread in response[page]["threads"]:
            semantic_url = thread["semantic_url"]
            if is_android() and contains(semantic_url, True,
                                         [search, "mobile", "phone", "!official-image-modification"]):
                return f"https://boards.4chan.org/wg/thread/{thread['no']}"
            elif is_desktop():
                page = randrange(pages)
                thread = random.choice(response[page]["threads"])
                semantic_url = thread["semantic_url"]
                if search in semantic_url and not contains(semantic_url, True,
                                                           ["mobile", "phone", "official-image-modification"]):
                    return f"https://boards.4chan.org/wg/thread/{thread['no']}"
    return no_results()


def fourchan(thread=None):
    thread = fourchan_auto(thread) if thread and not thread.startswith("http") else thread
    posts = requests.get(f"{thread or fourchan_auto()}.json").json()["posts"]
    for _ in posts:
        post = random.choice(posts)
        if "ext" in post and contains(post["ext"], False, [".jpg", ".png"]):
            return f"https://i.4cdn.org/wg/{post['tim']}{post['ext']}"
    no_results()


def subreddit():
    if is_android():
        return "mobilewallpaper+amoledbackgrounds+verticalwallpapers"
    return "wallpaper+wallpapers+earthporn+spaceporn+skyporn+minimalwallpaper"


def reddit_search(sub, search=None):
    base = "https://old.reddit.com/r/"
    if search:
        common_param = "&restrict_sr=on&sort=relevance&t=all"
        search_api = "/search.json?q="
        return f"{base}{sub}{search_api}{search}{common_param}"
    else:
        return f"{base}{sub}.json"


def reddit(subreddits=subreddit(), search=None):
    api = f"{reddit_search(subreddits, search)}"
    posts = requests.get(api, headers=user_agent).json()["data"]["children"]
    return random.choice(posts)["data"]["url"] if posts else no_results()


def imgur(search=None):
    alt = "rimgo.pussthecat.org"
    if search and not search.islower():
        imgur_url = f"https://{alt}/gallery/{search}"
    else:
        api = reddit_search("wallpaperdump", search)
        if is_android():
            search = f"{search or ''} {random.choice(['phone', 'mobile'])}"
            api = f"{reddit_search('wallpaperdump', search)}"
        imgur_url = ""
        while not contains(imgur_url, True, ["imgur.com"]):
            response = requests.get(api, headers=user_agent).json()["data"]["children"]
            imgur_url = random.choice(response)["data"]["url"] if response else no_results()

    tree = etree.HTML(requests.get(imgur_url.replace("imgur.com", f"{alt}")).content)
    images = tree.xpath("//div[@class='center']//img/@src")
    return f"https://{alt}{random.choice(images)}" if images else no_results()


def imsea(search=None):
    api = f"https://imsea.herokuapp.com/api/1?q={size}+{search or 'wallpaper'}"
    response = requests.get(api).json()["results"]
    return random.choice(response) if response else no_results()


def fivehundredpx(search=None):
    payload = {
        "operationName": "PhotoSearchQueryRendererQuery",
        "variables": {
            "sort": "RELEVANCE",
            "search": f"{search or ''}"
        },
        "query": "query PhotoSearchQueryRendererQuery($sort: PhotoSort, $search: String!) {"
                 "\n...PhotoSearchPaginationContainer_query_67nah\n}\n\nfragment "
                 "PhotoSearchPaginationContainer_query_67nah on Query {\nphotoSearch(sort: $sort, first: 20, "
                 "search: $search) { \nedges { \nnode {\n id\n legacyId\n canonicalPath\n name\n description\n "
                 "category\n uploadedAt\n location\n width\n height\n isLikedByMe\n notSafeForWork\n tags\n "
                 "photographer: uploader { \n id \n legacyId \n username \n displayName \n canonicalPath \n avatar { "
                 "\n images { \n url \n id \n } \n id \n } \n followedByUsers { \n totalCount \n isFollowedByMe \n "
                 "}\n }\n images(sizes: [33, 35]) { \n size \n url \n jpegUrl \n webpUrl \n id\n }\n __typename \n} "
                 "\ncursor \n} \ntotalCount \npageInfo { \nendCursor \nhasNextPage \n}\n}\n}\n"}
    headers = {
        "User-Agent": user_agent["User-Agent"],
        "Content-Type": content_json,
        "Host": "api.500px.com"
    }
    response = \
        requests.post("https://api.500px.com/graphql", json=payload, headers=headers).json()["data"]["photoSearch"][
            "edges"]
    random.shuffle(response)
    for edge in response:
        node = edge["node"]
        w = node["width"]
        h = node["height"]
        if good_size(w, h):
            return node["images"][1]["url"]
    return no_results()


def artstation_prints(search=None):
    orientation = "portrait" if is_android() else "landscape"
    search = search or ""
    api = f"https://www.artstation.com/api/v2/prints/public/printed_products.json?page=1&per_page=30" \
          f"&orientation={orientation}&sort=trending&visibility=profile&variant_filter=price_limits_per_type" \
          f"&q={search}"
    response = requests.get(api, headers=user_agent).json()["data"]
    return random.choice(response)["print_type_variants"][0]["image_urls"][0]["url"] if response else no_results()


def artstation_any(search=None):
    search = "nature" if not search or search == "" else search
    body = {"query": search, "page": 1, "per_page": 50, "sorting": "relevance", "pro_first": "1", "filters": "[]",
            "additional_fields": []}
    api = "https://www.artstation.com/api/v2/search/projects.json"
    headers = {
        "User-Agent": user_agent["User-Agent"],
        "Host": "www.artstation.com",
        "Content-Type": content_json
    }
    assets = requests.get(api, json=body, headers=headers).json()["data"]
    if type(assets) == str:
        no_results()
    hash_id = random.choice(assets)["hash_id"] if assets else no_results()

    api = f"https://www.artstation.com/projects/{hash_id}.json"
    assets = requests.get(api, json=body, headers=headers).json()["assets"]
    random.shuffle(assets)
    for asset in assets:
        h = asset["height"]
        w = asset["width"]
        if good_size(w, h):
            return asset["image_url"]
    return no_results()


def local(path):
    if os.path.exists(path):
        return random.choice(list(filter(lambda f: f.endswith(".png") or f.endswith(".jpg"), os.listdir(path))))
    return no_results()


def usage():
    cyan = "\033[36m"
    pink = "\033[35m"
    gray = "\033[37m"
    print("Supported sources:")
    print(f"{cyan}4c{pink}han {gray}[thread url. example: https://boards.4chan.org/wg/thread/1234567]")
    print(f"{cyan}5{pink}00{cyan}p{pink}x {gray}[search term]")
    print(f"{cyan}ar{pink}station {gray}[search term for prints page]")
    print(f"{cyan}ar{pink}station_{cyan}a{pink}rt {gray}[artist id. example: tohad]")
    print(f"{cyan}ar{pink}station_{cyan}g{pink}en {gray}[search term for main page]")
    print(f"{cyan}ca{pink}nvas {gray}[solid|linear|radial|twisted|bilinear|plasma|blurred|[1-7]]")
    print(f"{cyan}ea{pink}rthview {gray}(takes no search term)")
    print(f"{cyan}im{pink}gur {gray}[gallery id. example: qF259WO]")
    print(f"{cyan}lo{pink}cal {gray}[path relative to $HOME]")
    print(f"{cyan}re{pink}ddit {gray}[search term]")
    print(f"{cyan}un{pink}splash {gray}[search term]")
    print(f"{cyan}wa{pink}llhaven {gray}[search term]")


def run():
    home = True
    lock = True
    source = "unsplash"
    term = None
    args = parser().parse_args()
    options, remainder = getopt.getopt(
        sys.argv[1:],
        'vus:t:d:ho',
    )
    for opt, arg in options:
        if opt in "-v":
            print(__version__())
            exit(0)
        elif opt in "-u":
            usage()
            exit(0)
        elif opt in "-d":
            if os.path.exists(args.d):
                shutil.move(folder, args.d.strip())
            print(args.d)
            exit(0)
        if opt in "-s":
            source = args.s.strip()
        if opt in "-t":
            term = args.t.strip()
        if opt in "-l":
            lock = True
            home = False
        if opt in "-h":
            lock = False
            home = True

    if contains(source, False, ["4c", "4chan"]):
        set_wp(fourchan(term), home, lock)
    elif contains(source, False, ["5p", "500px"]):
        set_wp(fivehundredpx(term), home, lock)
    elif contains(source, False, ["un", "unsplash"]):
        set_wp(unsplash(term), home, lock)
    elif contains(source, False, ["wa", "wallhaven"]):
        set_wp(wallhaven(term), home, lock)
    elif contains(source, False, ["im", "imgur"]):
        set_wp(imgur(term), home, lock)
    elif contains(source, False, ["is", "imsea"]):
        set_wp(imsea(term), home, lock)
    elif contains(source, False, ["ar", "artstation"]):
        set_wp(artstation_any(term), home, lock)
    elif contains(source, False, ["arp", "artstation_prints"]):
        set_wp(artstation_any(term), home, lock)
    elif contains(source, False, ["re", "reddit"]):
        if term.contains("@"):
            set_wp(reddit(term.split("@")[1], reddit(term.split("@")[0])))
        set_wp(reddit(search=term), home, lock)
    else:
        print("Unknown source")


if __name__ == "__main__":
    sys.exit(run())
