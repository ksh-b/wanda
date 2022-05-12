import argparse
import glob
import json
import os
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import requests
from lxml import html
from wand.image import Image

version = '0.58.5'

user_agent = {"User-Agent": "git.io/wanda"}
content_json = "application/json"
folder = f'{str(Path.home())}/wanda'


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
        default=None,
        required=False,
        help='Save current wallpaper to home directory or given path',
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
        required=False,
        action="store_const",
        const=version
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
    return requests.get("https://detectportal.firefox.com/success.txt").text.strip() == "success"


def validate_url(url):
    response = requests.get(url, headers=user_agent)
    return response if response.status_code == 200 else no_results()


def no_results():
    print("No results found. Try another source/term.")
    exit(1)


def command(string: str) -> str:
    return subprocess.check_output(string.split(" ")).decode()


def short_url(url: str) -> str:
    response = requests.post("https://cleanuri.com/api/v1/shorten", data={"url": url}).json()
    return f"{response['result_url']}" if "result_url" in response else url


def is_web_url(url):
    return url.startswith("https://")


def set_wp(url: str, home=True, lock=True):
    if is_android():
        t = "u" if is_web_url(url) else "f"
        if home:
            command(f"termux-wallpaper -{t} {url}")
        if lock:
            command(f"termux-wallpaper -l{t} {url}")
        return
    path = os.path.normpath(f'{folder}/wanda_{time.time()}')
    if not os.path.exists(folder):
        os.mkdir(folder)

    files = glob.glob(f'{folder}/*')
    for f in files:
        os.remove(f)
    if url.startswith("https://"):
        with open(path, 'wb') as f:
            print(url)
            f.write(requests.get(url, headers=user_agent).content)
    elif os.path.exists(url):
        path = url
    else:
        print("Invalid url/path")
        return 1
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
        hxw = command("getprop persist.vendor.camera.display.umax").strip()
        return f"{hxw.split('x')[1]}x{hxw.split('x')[0]}" if hxw is not None else "1440x2960"
    try:
        dimensions = filter(lambda l: "dimensions" in l, subprocess.check_output("xdpyinfo").decode().split("\n"))
        return list(dimensions)[0].split()[1]
    except NameError:
        return "2560x1440"


def is_landscape():
    return int(size().split("x")[0]) > int(size().split("x")[1])


def is_portrait():
    return not is_landscape()


def is_android():
    return os.environ.get('TERMUX_VERSION') is not None


def is_desktop():
    return not is_android()


def good_size(w, h):
    return (is_portrait() and w < h) or (is_landscape() and w > h)


def contains(word: str, match_all: bool, desired: list) -> bool:
    matches = list(map(lambda w: w not in word if w.startswith("!") else w in word, desired))
    if not match_all:
        return True in matches
    return set(matches) == {True}


def wallhaven(search=None):
    api = "https://wallhaven.cc/api/v1/search?sorting=random"
    ratios = "portrait" if is_portrait() else "landscape"
    response = requests.get(f"{api}&ratios={ratios}&q={search or ''}").json()["data"]
    return response[0]["path"] if response else no_results()


def unsplash(search=None):
    api = f"https://source.unsplash.com/random/{size()}/?{search or ''}"
    response = requests.get(api).url
    return response if "source-404" not in response else no_results()


def earthview(_):  # NOSONAR
    tree = html.fromstring(requests.get("https://earthview.withgoogle.com").content)
    url = json.loads(tree.xpath("//body/@data-photo")[0])["photoUrl"]
    if is_landscape():
        return url
    path = os.path.normpath(f'{folder}/wanda_{time.time()}')
    with open(path, 'wb') as f:
        f.write(requests.get(url, headers=user_agent).content)
    with Image(filename=path) as i:
        i.rotate(90)
        i.save(filename=path)
    return path


def blank(search):
    return not search or search == ""


def fourchan(search=None):
    if not search:
        search = ""
        board = "wg"
    elif "@" not in search:
        search = f"{search}" if search else ""
        board = "wg"
    else:
        board = search.split("@")[1]
        search = search.split("@")[0]

    api = f"https://archive.alice.al/_/api/chan/search/?boards={board}&subject={search}"
    response = requests.get(api).json()
    if "error" in response:
        no_results()
    posts = list(filter(lambda p: "media" in p and "nimages" in p, response["0"]["posts"]))
    if not posts:
        no_results()
    post = random.choice(posts)
    thread = post["thread_num"]
    board = post["board"]["shortname"]
    api = f"https://archive.alice.al/_/api/chan/thread/?board={board}&num={thread}"
    posts = requests.get(api).json()[thread]["posts"]
    if not posts:
        no_results()
    post = random.choice(list(filter(lambda p: "media" not in p, posts)))
    return posts[post]["media"]["media_link"]


def subreddit():
    if is_portrait():
        return "mobilewallpaper+amoledbackgrounds+verticalwallpapers"
    return "wallpaper+wallpapers+minimalwallpaper"


def reddit_gallery(url):
    if "/gallery/" not in url:
        return
    else:
        url = url.replace("/gallery/", "/comments/")

    images = requests.get(f"{url}.json", headers=user_agent).json()[0]["data"]["children"][0]["data"]["media_metadata"]
    ids = images.keys()
    return list(map(lambda i: f'https://i.redd.it/{i}.{images[i]["m"].split("/")[1]}', ids))


def is_imgur_gallery(url):
    return contains(url, False, ["imgur.com/a", "imgur.com/gallery"])


def reddit_search(sub, search=None, extra=""):
    base = "https://old.reddit.com/r/"
    if not search:
        return f"{base}{sub}.json?{extra}"
    common_param = f"&restrict_sr=on&sort=relevance&t=all&sort=top&limit=100&type=link{extra}"
    search_api = "/search.json?q="
    return f"{base}{sub}{search_api}{search}{common_param}"


def reddit_compare_image_size(title):
    if sr := re.search("[0-9]+x[0-9]+", title):
        w = int(sr.group().split("x")[0]) >= int(size().split("x")[0])
        h = int(sr.group().split("x")[1]) >= int(size().split("x")[1])
        return w and h
    return is_portrait() or False


def reddit(search=None, subreddits=subreddit()):
    if search and "@" in search:
        subreddits = search.split("@")[1]
        search = search.split("@")[0]
    api = reddit_search(subreddits, search)
    posts = requests.get(api, headers=user_agent).json()["data"]["children"]
    image_urls = ["reddit.com/gallery", "imgur.com/a", "imgur.com/gallery", "i.redd.it", "i.imgur", ]
    posts = list(filter(lambda p:
                        contains(p["data"]["url"], False, image_urls) and
                        reddit_compare_image_size(p["data"]["title"]), posts))
    if not posts:
        no_results()
    url = random.choice(posts)["data"]["url"]
    if "reddit.com/gallery" in url:
        return random.choice(reddit_gallery(url))
    elif is_imgur_gallery(url):
        return get_imgur_image(url)
    elif contains(url, False, ["i.redd.it", "i.imgur", ".png", ".jpg"]):
        return url
    else:
        no_results()


def imgur(search=None):
    if search:
        imgur_url = f"https://rimgo.pussthecat.org/gallery/{search}"
    else:
        search = ""
        if is_portrait():
            search = f"&q={search or ''} {random.choice(['phone', 'mobile'])}"
        api = f"https://old.reddit.com/r/wallpaperdump/search.json?q=site:imgur.com&restrict_sr=on{search}"
        response = requests.get(api, headers=user_agent).json()["data"]["children"]
        imgur_url = random.choice(response)["data"]["url"] if response else no_results()

    return get_imgur_image(imgur_url)


def get_imgur_image(imgur_url, alt="rimgo.pussthecat.org"):
    tree = html.fromstring(
        requests.get(imgur_url.replace("imgur.com", f"{alt}"), headers=user_agent).content)
    images = tree.xpath("//div[@class='center']//img/@src")
    return f"https://{alt}{random.choice(images)}" if images else no_results()


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
    import cloudscraper

    scraper = cloudscraper.create_scraper()
    orientation = "portrait" if is_portrait() else "landscape"
    search = search or ""
    api = f"https://www.artstation.com/api/v2/prints/public/printed_products.json?page=1&per_page=30" \
          f"&orientation={orientation}&sort=trending&visibility=profile&variant_filter=price_limits_per_type" \
          f"&q={search}"
    response = scraper.get(api, headers=user_agent).json()["data"]
    return random.choice(response)["print_type_variants"][0]["image_urls"][0]["url"] if response else no_results()


def artstation_artist(search=None):
    import cloudscraper
    if blank(search):
        search = random.choice(["tohad"])
    scraper = cloudscraper.create_scraper()
    response = scraper.get(f"https://www.artstation.com/users/{search}/hovercard.json", headers=user_agent)
    if response.status_code != 200:
        no_results()
    projects = scraper.get(f"https://www.artstation.com/users/{search}/projects.json", headers=user_agent).json()
    artwork = random.choice(projects["data"])["permalink"].split("/")[-1]
    return scraper.get(f"https://www.artstation.com/projects/{artwork}.json", headers=user_agent).json()["assets"][0][
        "image_url"]


def artstation_any(search=None):
    import cloudscraper

    scraper = cloudscraper.create_scraper()
    search = "nature" if blank(search) else search
    body = {"query": search, "page": 1, "per_page": 50, "sorting": "relevance", "pro_first": "1", "filters": "[]",
            "additional_fields": []}
    api = "https://www.artstation.com/api/v2/search/projects.json"
    headers = {
        "User-Agent": user_agent["User-Agent"],
        "Host": "www.artstation.com",
        "Content-Type": content_json
    }
    assets = scraper.get(api, json=body, headers=headers).json()["data"]
    if isinstance(assets, str):
        no_results()
    hash_id = random.choice(assets)["hash_id"] if assets else no_results()

    api = f"https://www.artstation.com/projects/{hash_id}.json"
    assets = scraper.get(api, json=body, headers=headers).json()["assets"]
    random.shuffle(assets)
    for asset in assets:
        h = asset["height"]
        w = asset["width"]
        if good_size(w, h):
            return asset["image_url"]
    return no_results()


def local(path):
    if blank(path):
        print("Please specify path to images")
        exit(1)
    if path and not path.endswith("/"):
        path = f'{path}/'
    if os.path.exists(path):
        return path + random.choice(list(filter(lambda f: f.endswith(".png") or f.endswith(".jpg"), os.listdir(path))))
    return no_results()


def waifuim(search=None):
    orientation = "PORTRAIT" if is_portrait() else "LANDSCAPE"
    accept = f"&selected_tags={search}" if search else ""
    reject = ""
    if search and "-" in search:
        accept = f"&selected_tags={search.split('-')[0]}"
        reject = f"&excluded_tags={search.split('-')[1]}"
    api = f"https://api.waifu.im/random/?gif=false&is_nsfw=false" \
          f"&orientation={orientation}{accept}{reject}"
    response = requests.get(api).json()
    if "detail" in response:
        no_results()
    return response["images"][0]["url"]


def usage():
    cyan = "\033[36m"
    pink = "\033[35m"
    print("Use double quotes if your keyword or path has spaces")
    print("Supported sources:")
    print(f"{cyan}4chan {pink}[keyword]|[keyword@board]")
    print(f"{cyan}500{cyan}px {pink}[keyword]")
    print(f"{cyan}arstation {pink}[keyword]")
    print(f"{cyan}arstation_{cyan}artist {pink}[id of artist. example: aenamiart]")
    print(f"{cyan}arstation_{cyan}prints {pink}[keyword for prints]")
    print(f"{cyan}imgur {pink}[gallery id. example: qF259WO]")
    print(f"{cyan}earthview")
    print(f"{cyan}local {pink}[full path to folder]")
    print(f"{cyan}reddit {pink}[keyword]|[keyword@subreddit]")
    print(f"{cyan}unsplash {pink}[keyword]")
    print(f"{cyan}wallhaven {pink}[keyword(,keyword2,keyword3...&)]")
    print(f"{cyan}waifu.im {pink}[selected_tag-(excluded_tag)]")
    print("")
    print("Wallhaven advanced usage:")
    print("For full list of parameters, go to https://wallhaven.cc/help/api#search")
    print("example: wanda -sw -tcar,lamborghini&colors=cc3333&categories=111&purity=100")
    print("")
    print("\033[33mShort codes:")
    print(json.dumps(shortcodes(), indent=2).strip("{}").replace("\"", ""))


def run():
    args = parser().parse_args()
    if '-u' in sys.argv:
        usage()
        exit(0)
    if '-v' in sys.argv:
        print(args.v)
        exit(0)
    if '-d' in sys.argv:
        for src_file in Path(folder).glob('wanda_*.*'):
            shutil.copy(src_file, args.d)
            print(f"Copied to {src_file}")
        exit(0)
    source = args.s
    term = args.t
    home = True
    lock = True
    if '-l' in sys.argv and args.l:
        lock = True
        home = False
    if '-h' in sys.argv and args.h:
        lock = False
        home = True

    try:
        if source != 'local' and not is_connected():
            print("Please check your internet connection and try again")
            exit(1)
        set_wp(eval(source_map(source))(term), home, lock)
    except NameError:
        print(f"Unknown source: '{source}'. Available sources:")
        usage()
    return 0


def shortcodes():
    return {
        "4": "4chan",
        "5": "500px",
        "aa": "artstation_artist",
        "ap": "artstation_prints",
        "a": "artstation",
        "e": "earthview",
        "i": "imgur",
        "l": "local",
        "r": "reddit",
        "u": "unsplash",
        "wi": "waifuim",
        "w": "wallhaven",
    }


def source_map(shortcode):
    return shortcodes().get(shortcode, shortcode)


if __name__ == "__main__":
    sys.exit(run())
