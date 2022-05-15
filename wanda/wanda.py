import argparse
import json
import os
import random
import re
import subprocess
import sys
import time
from pathlib import Path

import cloudscraper  # type: ignore

version = "0.59.5"

user_agent = {"User-Agent": "git.io/wanda"}
content_json = "application/json"
folder = f"{str(Path.home())}/wanda"

landscape = "landscape"
portrait = "portrait"


def is_connected():
    try:
        result = get("https://detectportal.firefox.com/success.txt")
        return result.text.strip() == "success"
    except Exception:
        return False


def no_results():
    print("No results found. Try another source/term.")
    exit(1)


def command(string: str) -> str:
    return subprocess.check_output(string.split(" ")).decode().strip()


def set_wp(url: str, home=True, lock=True):
    # print selected wallpaper url
    print(url)

    # setup directory
    path = get_dl_path()

    # download wallpaper
    if url.startswith("https://"):
        download(path, url)
    elif os.path.exists(url):
        path = url
    else:
        print("Invalid url/path")
        return 1

    # fit wallpaper to screen if orientation mismatch
    # path = fit(path)

    # set wallpaper
    import platform

    if is_android():
        set_wp_android(path, home, lock)
    elif platform.system() == "Linux":
        set_wp_linux(path)
    elif platform.system() == "Windows":
        set_wp_win(path)
    else:
        print("Platform not supported")
        exit(1)


def get_dl_path():
    path = os.path.normpath(f"{folder}/wanda_{int(time.time())}")
    if not os.path.exists(folder):
        os.mkdir(folder)
    empty_download_folder()
    return path


def empty_download_folder():
    import glob

    files = glob.glob(f"{folder}/*")
    for f in files:
        os.remove(f)


def download(path, url):
    with open(path, "wb") as f:
        f.write(get(url).content)


def set_wp_android(path, home, lock):
    if home:
        command(f"termux-wallpaper -f {path}")
    if lock:
        command(f"termux-wallpaper -lf {path}")


def get(url):
    scraper = cloudscraper.create_scraper()
    return scraper.get(url, headers=user_agent)


def set_wp_win(path):
    import ctypes

    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


def set_wp_linux(path):
    if os.environ.get("SWAYSOCK"):
        setter = "eval ogurictl output '*' --image"
    elif os.environ.get("DESKTOP_SESSION").lower == "mate":
        setter = "gsettings set org.mate.background picture-filename"
    elif contains(
            os.environ.get("DESKTOP_SESSION").lower(), False, ["xfce", "xubuntu"]
    ):
        setter = (
            "xfconf-query --channel xfce4-desktop --property /backdrop/screen0/monitor0/workspace0/last-image "
            "--set "
        )
    elif os.environ.get("DESKTOP_SESSION").lower() == "lxde":
        setter = "pcmanfm --set-wallpaper"
    elif contains(
            os.environ.get("DESKTOP_SESSION").lower(), False, ["plasma", "neon", "kde"]
    ):
        return os.system(
            'qdbus org.kde.plasmashell /PlasmaShell org.kde.PlasmaShell.evaluateScript "\n'
            + "var allDesktops = desktops();\n"
            + "print (allDesktops);\n"
            + "for (i=0;i<allDesktops.length;i++) {\n"
            + "d = allDesktops[i];\n"
            + "d.wallpaperPlugin = 'org.kde.image';\n"
            + "d.currentConfigGroup = Array('Wallpaper','org.kde.image','General');\n"
            + f"d.writeConfig('Image', 'file://{path}')\n"
            + '}"'
        )
    elif contains(
            os.environ.get("DESKTOP_SESSION").lower(),
            False,
            ["gnome", "pantheon", "ubuntu", "deepin", "pop"],
    ):
        setter = "gsettings set org.gnome.desktop.background picture-uri"
    else:
        setter = "feh --bg-scale"

    command(f"{setter} {path}")


def size():
    import screeninfo  # type: ignore
    if is_android():
        hxw = command("getprop persist.vendor.camera.display.umax")
        if hxw is not None:
            int(hxw.split("x")[1]), int(hxw.split("x")[0])
        else:
            return 1440, 2960
    try:
        dimensions = screeninfo.get_monitors()[0]  # type: ignore
        return int(dimensions.width), int(dimensions.height)
    except screeninfo.ScreenInfoError:
        return 2560, 1440


def screen_orientation():
    return landscape if size()[0] > size()[1] else portrait


def image_orientation(image):
    return landscape if image.width > image.height else portrait


def is_android():
    return os.environ.get("TERMUX_VERSION") is not None


def is_desktop():
    return not is_android()


def blank(search):
    return not search or search == ""


def good_size(w, h):
    return (screen_orientation() is portrait and w < h) or (
            screen_orientation() is landscape and w > h
    )


def contains(word: str, match_all: bool, desired: list) -> bool:
    matches = list(
        map(lambda w: w not in word if w.startswith("!") else w in word, desired)
    )
    if not match_all:
        return True in matches
    return set(matches) == {True}


def wallhaven(search=None):
    api = "https://wallhaven.cc/api/v1/search?sorting=random"
    ratios = "portrait" if screen_orientation() is portrait else "landscape"
    response = get(f"{api}&ratios={ratios}&q={search or ''}").json()["data"]
    return response[0]["path"] if response else no_results()


def unsplash(search=None):
    api = f"https://source.unsplash.com/random/{size()[0]}x{size()[1]}/?{search or ''}"
    response = get(api).url
    return response if "source-404" not in response else no_results()


def earthview(_):  # NOSONAR
    from lxml import html  # type: ignore

    tree = html.fromstring(get("https://earthview.withgoogle.com").content)
    url = json.loads(tree.xpath("//body/@data-photo")[0])["photoUrl"]
    ext = url.split(".")[-1]
    if screen_orientation() is landscape:
        return url
    path = os.path.normpath(f"{folder}/wanda_{int(time.time())}.{ext}")
    download(path, url)
    from PIL import Image  # type: ignore

    image = Image.open(path)
    image.rotate(90)
    image.save(path)
    return path


# do nothing
def ok():
    pass


def fourchan(search=None):
    if blank(search):
        search = ""
        board = "wg"
    elif "@" not in search:
        search = f"{search.lower()}" if search else ""
        board = "wg"
    else:
        board = search.split("@")[1]
        search = search.split("@")[0].lower()

    api = f"https://archive.alice.al/_/api/chan/search/?boards={board}&subject={search.lower()}"
    response = get(api).json()
    no_results() if "error" in response else ok()
    posts = list(
        filter(lambda p: "media" in p and "nimages" in p, response["0"]["posts"])
    )
    ok() if posts else no_results()
    post = random.choice(posts)
    thread = post["thread_num"]
    board = post["board"]["shortname"]
    api = f"https://archive.alice.al/_/api/chan/thread/?board={board}&num={thread}"
    posts = get(api).json()[thread]["posts"]
    ok() if posts else no_results()
    post = random.choice(list(filter(lambda p: "media" not in p, posts)))
    return posts[post]["media"]["media_link"]


def suggested_subreddits():
    if screen_orientation() is portrait:
        return "mobilewallpaper+amoledbackgrounds+verticalwallpapers"
    return "wallpaper+wallpapers+minimalwallpaper"


def reddit_gallery(url):
    if "/gallery/" not in url:
        return
    else:
        url = url.replace("/gallery/", "/comments/")
    images = get(f"{url}.json").json()[0]["data"]["children"][0]["data"][
        "media_metadata"
    ]
    ids = images.keys()
    return list(
        map(lambda i: f'https://i.redd.it/{i}.{images[i]["m"].split("/")[1]}', ids)
    )


def is_imgur_gallery(url):
    return contains(url, False, ["imgur.com/a", "imgur.com/gallery"])


def reddit_search(sub, search=None, extra=""):
    base = "https://old.reddit.com/r/"
    if not search:
        return f"{base}{sub}.json?{extra}"
    common_param = (
        f"&restrict_sr=on&sort=relevance&t=all&sort=top&limit=100&type=link{extra}"
    )
    search_api = "/search.json?q="
    return f"{base}{sub}{search_api}{search}{common_param}"


def reddit_compare_image_size(title):
    if sr := re.search(r"[\d]+x[\d]+", title):
        w = int(sr.group().split("x")[0]) >= int(size()[0])
        h = int(sr.group().split("x")[1]) >= int(size()[1])
        return w and h
    return screen_orientation() is portrait or False


def reddit(search=None, subreddits=suggested_subreddits()):
    if search and "@" in search:
        subreddits = search.split("@")[1]
        search = search.split("@")[0]
    api = reddit_search(subreddits, search)
    posts = get(api).json()["data"]["children"]
    image_urls = [
        "reddit.com/gallery",
        "imgur.com/a",
        "imgur.com/gallery",
        "i.redd.it",
        "i.imgur",
    ]
    posts = list(
        filter(
            lambda p: contains(p["data"]["url"], False, image_urls)
                      and reddit_compare_image_size(p["data"]["title"]),
            posts,
        )
    )
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


def picsum(search=None):
    if blank(search):
        api = f"https://picsum.photos/{size()[0]}/{size()[1]}"
    else:
        api = f"https://picsum.photos/seed/{search}/{size()[0]}/{size()[1]}"
    return get(api).url


def imgur(search=None):
    if search:
        imgur_url = f"https://rimgo.pussthecat.org/gallery/{search}"
    else:
        search = ""
        if screen_orientation() is portrait:
            search = f"&q={search or ''} {random.choice(['phone', 'mobile'])}"
        api = f"https://old.reddit.com/r/wallpaperdump/search.json?q=site:imgur.com&restrict_sr=on{search}"
        response = get(api).json()["data"]["children"]
        imgur_url = random.choice(response)["data"]["url"] if response else no_results()
    return get_imgur_image(imgur_url)


def get_imgur_image(imgur_url, alt="rimgo.pussthecat.org"):
    from lxml import html

    tree = html.fromstring(get(imgur_url.replace("imgur.com", f"{alt}")).content)
    images = tree.xpath("//div[@class='center']//img/@src")
    return f"https://{alt}{random.choice(images)}" if images else no_results()


def fivehundredpx(search=None):
    payload = {
        "operationName": "PhotoSearchQueryRendererQuery",
        "variables": {"sort": "RELEVANCE", "search": f"{search or ''}"},
        "query": "query PhotoSearchQueryRendererQuery($sort: PhotoSort, $search: String!) {"
                 "\n...PhotoSearchPaginationContainer_query_67nah\n}\n\nfragment "
                 "PhotoSearchPaginationContainer_query_67nah on Query {\nphotoSearch(sort: $sort, first: 20, "
                 "search: $search) { \nedges { \nnode {\n id\n legacyId\n canonicalPath\n name\n description\n "
                 "category\n uploadedAt\n location\n width\n height\n isLikedByMe\n notSafeForWork\n tags\n "
                 "photographer: uploader { \n id \n legacyId \n username \n displayName \n canonicalPath \n avatar { "
                 "\n images { \n url \n id \n } \n id \n } \n followedByUsers { \n totalCount \n isFollowedByMe \n "
                 "}\n }\n images(sizes: [33, 35]) { \n size \n url \n jpegUrl \n webpUrl \n id\n }\n __typename \n} "
                 "\ncursor \n} \ntotalCount \npageInfo { \nendCursor \nhasNextPage \n}\n}\n}\n",
    }
    headers = {
        "User-Agent": user_agent["User-Agent"],
        "Content-Type": content_json,
        "Host": "api.500px.com",
    }
    scraper = cloudscraper.create_scraper()
    response = scraper.post(
        "https://api.500px.com/graphql", json=payload, headers=headers
    ).json()["data"]["photoSearch"]["edges"]
    random.shuffle(response)
    for edge in response:
        node = edge["node"]
        w = node["width"]
        h = node["height"]
        if good_size(w, h):
            return node["images"][1]["url"]
    return no_results()


def artstation_prints(search=None):
    scraper = cloudscraper.create_scraper()
    orientation = "portrait" if screen_orientation() == portrait else "landscape"
    search = search or ""
    api = (
        f"https://www.artstation.com/api/v2/prints/public/printed_products.json?page=1&per_page=30"
        f"&orientation={orientation}&sort=trending&visibility=profile&variant_filter=price_limits_per_type"
        f"&q={search}"
    )
    response = scraper.get(api, headers=user_agent).json()["data"]
    return (
        random.choice(response)["print_type_variants"][0]["image_urls"][0]["url"]
        if response
        else no_results()
    )


def artstation_artist(search=None):
    if blank(search):
        print("Please provide an artist id")
        exit(1)
    response = get(f"https://www.artstation.com/users/{search}/hovercard.json")
    no_results() if response.status_code != 200 else ok()
    projects = get(f"https://www.artstation.com/users/{search}/projects.json").json()
    artwork = random.choice(projects["data"])["permalink"].split("/")[-1]
    return get(f"https://www.artstation.com/projects/{artwork}.json").json()["assets"][
        0
    ]["image_url"]


def artstation_any(search=None):
    scraper = cloudscraper.create_scraper()
    search = "nature" if blank(search) else search
    body = {
        "query": search,
        "page": 1,
        "per_page": 50,
        "sorting": "relevance",
        "pro_first": "1",
        "filters": "[]",
        "additional_fields": [],
    }
    api = "https://www.artstation.com/api/v2/search/projects.json"
    headers = {
        "User-Agent": user_agent["User-Agent"],
        "Host": "www.artstation.com",
        "Content-Type": content_json,
    }
    assets = scraper.get(api, json=body, headers=headers).json()["data"]

    no_results() if isinstance(assets, str) else ok()
    hash_id = random.choice(assets)["hash_id"] if assets else no_results()

    api = f"https://www.artstation.com/projects/{hash_id}.json"
    assets = scraper.get(api, json=body, headers=headers).json()["assets"]
    random.shuffle(assets) if assets else no_results()
    for asset in assets:
        h = asset["height"]
        w = asset["width"]
        if good_size(w, h):
            return asset["image_url"]
    return random.choice(assets)["image_url"]


def local(path):
    import filetype  # type: ignore

    if blank(path):
        print("Please specify path to images")
        exit(1)
    if path and not path.endswith("/"):
        path = f"{path}/"
    if os.path.exists(path):
        return path + random.choice(
            list(
                filter(
                    lambda f: filetype.guess(path + f).MIME.startswith("image"),
                    os.listdir(path),
                )
            )
        )
    return no_results()


def waifuim(search=None):
    orientation = "PORTRAIT" if screen_orientation() is portrait else "LANDSCAPE"
    accept = f"&selected_tags={search}" if search else ""
    reject = ""
    if search and "-" in search:
        accept = f"&selected_tags={search.split('-')[0]}"
        reject = f"&excluded_tags={search.split('-')[1]}"
    api = (
        f"https://api.waifu.im/random/?gif=false&is_nsfw=false"
        f"&orientation={orientation}{accept}{reject}"
    )
    response = get(api).json()
    no_results() if "detail" in response else ok()
    return response["images"][0]["url"]


# experimental
def musicbrainz(search=None):
    print("[!] This source is experimental")
    import musicbrainzngs as mb  # type: ignore
    if blank(search) and is_android():
        music_players = ["com.spotify.music"]
        notifications = json.loads(command("termux-notification-list"))
        music_notification = list(filter(
            lambda n: n["packageName"] in music_players,
            notifications
        ))[0]
        title = music_notification["title"]
        artist = music_notification["content"]
        search = f"{artist} {title}"
    if blank(search) and not is_android():
        print("Please enter [artist] [track title]")
        exit(1)
    mb.set_useragent("wanda", version, user_agent["User-Agent"])
    albums = mb.search_release_groups(search)
    ok() if albums else no_results()
    album_id = albums["release-group-list"][0]["id"]
    cover = mb.get_release_group_image_front(album_id)
    with open(get_dl_path(), "wb") as f:
        f.write(cover)


def fit(wallpaper_path):
    from colorthief import ColorThief  # type: ignore
    from PIL import Image

    wp = Image.open(wallpaper_path)
    color_thief = ColorThief(wallpaper_path)
    dominant_color = color_thief.get_color(quality=1)
    bg = Image.new("RGB", (size()), dominant_color)

    # image smaller than screen
    if wp.height < bg.height and wp.width < bg.width:
        x1 = int(bg.width / 2) - int(wp.width / 2)
        y1 = int(bg.height / 2) - int(wp.height / 2)
        bg.paste(wp, (x1, y1))
        bg.save(wallpaper_path)

    # image is portrait but screen is landscape
    if image_orientation(wp) is portrait and screen_orientation() is landscape:
        percentage = wp.height / bg.height
        resized_dimensions = (
            int(wp.width * (1 / percentage)),
            int(wp.height * (1 / percentage)),
        )
        resized = wp.resize(resized_dimensions)
        x1 = int(bg.width / 2) - int(resized.width / 2)
        y1 = 0
        bg.paste(resized, (x1, y1))
        bg.save(wallpaper_path)

    # image is landscape but screen is portrait
    if image_orientation(wp) is landscape and screen_orientation() is portrait:
        percentage = wp.width / bg.width
        resized_dimensions = (
            int(wp.width * (1 / percentage)),
            int(wp.height * (1 / percentage)),
        )
        resized = wp.resize(resized_dimensions)
        x1 = 0
        y1 = int(bg.height / 2) - int(resized.height / 2)
        bg.paste(resized, (x1, y1))
        bg.save(wallpaper_path)
    return wallpaper_path


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
    print(f"{cyan}musicbrainz {pink}[artist title]")
    print(f"{cyan}reddit {pink}[keyword]|[keyword@subreddit]")
    print(f"{cyan}unsplash {pink}[keyword]")
    print(f"{cyan}wallhaven {pink}[keyword(,keyword2,keyword3...&)]")
    print(f"{cyan}waifu.im {pink}[selected_tag-(excluded_tag)]")
    print("")
    print("Wallhaven advanced usage:")
    print("For full list of parameters, go to https://wallhaven.cc/help/api#search")
    print(
        "example: wanda -sw -tcar,lamborghini&colors=cc3333&categories=111&purity=100"
    )
    print("")
    print("\033[33mShort codes:")
    print(json.dumps(shortcodes(), indent=2).strip("{}").replace('"', ""))


def parser():
    parser_ = argparse.ArgumentParser(description="Set wallpapers")

    parser_.add_argument(
        "-s",
        metavar="source",
        type=str,
        default="unsplash",
        help="Source for wallpaper. -u for all supported sources",
        required=False,
    )
    parser_.add_argument(
        "-t",
        metavar="term",
        type=str,
        default=None,
        help="Search term. -u for more help",
        required=False,
    )
    parser_.add_argument(
        "-d",
        metavar="download",
        type=str,
        default=None,
        required=False,
        help="Save current wallpaper to home directory or given path",
    )
    parser_.add_argument(
        "-u",
        metavar="usage",
        help="Supported sources and their usage",
        required=False,
        action="store_const",
        const=None,
    )
    parser_.add_argument(
        "-v",
        metavar="version",
        help="Current version",
        required=False,
        action="store_const",
        const=version,
    )
    if is_android():
        parser_.add_argument(
            "-o",
            help="Set wallpaper on homescreen.",
            required=False,
            action="store_true",
        )
        parser_.add_argument(
            "-l",
            help="Set wallpaper on lockscreen.",
            required=False,
            action="store_true",
        )
    return parser_


def run():
    args = parser().parse_args()
    if "-u" in sys.argv:
        usage()
        exit(0)
    if "-v" in sys.argv:
        print(args.v)
        exit(0)
    if "-d" in sys.argv:
        for src_file in Path(folder).glob("wanda_*.*"):
            import shutil

            shutil.copy(src_file, args.d)
            print(f"Copied to {src_file}")
        exit(0)
    source = args.s
    term = args.t
    home = True
    lock = True
    if "-l" in sys.argv and args.l:
        lock = True
        home = False
    if "-h" in sys.argv and args.h:
        lock = False
        home = True

    try:
        if source != "local" and not is_connected():
            print("Please check your internet connection and try again")
            exit(1)
        set_wp(eval(source_map(source))(term), home, lock)
    except NameError:
        print(f"Unknown source: '{source}'. Available sources:")
        usage()
    return 0


def shortcodes():
    return {
        "4": "fourchan",
        "5": "fivehundredpx",
        "aa": "artstation_artist",
        "ap": "artstation_prints",
        "a": "artstation",
        "e": "earthview",
        "i": "imgur",
        "l": "local",
        "p": "picsum",
        "r": "reddit",
        "u": "unsplash",
        "wi": "waifuim",
        "w": "wallhaven",
    }


def source_map(shortcode):
    return shortcodes().get(shortcode, shortcode)


if __name__ == "__main__":
    sys.exit(run())
