import json
import os
import random
import re
import time

import appdirs
import cloudscraper  # type: ignore
import filetype  # type: ignore

from wanda.utils.common_utils import blank, get, ok, contains, get_dl_path, download
from wanda.utils.image_utils import screen_orientation, good_size
from wanda.utils.os_utils import size

user_agent = {"User-Agent": "git.io/wanda"}


def no_results():
    print("No results found.")
    print("• Try another source or term")
    print("• Try again at a later time")
    exit(1)


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

    api = f"https://archive.palanq.win/_/api/chan/search/?boards={board}&subject={search.lower()}"
    response = get(api).json()
    no_results() if "error" in response else ok()
    posts = list(
        filter(lambda p: "media" in p and "nimages" in p, response["0"]["posts"])
    )
    ok() if posts else no_results()
    post = random.choice(posts)
    thread = post["thread_num"]
    board = post["board"]["shortname"]
    api = f"https://archive.palanq.win/_/api/chan/thread/?board={board}&num={thread}"
    posts = get(api).json()[thread]["posts"]
    ok() if posts else no_results()
    post = random.choice(list(filter(lambda p: "media" in posts[p], posts)))
    if posts[post]:
        return posts[post]["media"]["media_link"]
    return no_results()


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

def picsum(search=None):
    w, h = size()
    if blank(search):
        api = f"https://picsum.photos/{w}/{h}"
    else:
        api = f"https://picsum.photos/seed/{search}/{w}/{h}"
    return get(api).url


def imgur(search=None):
    if search:
        imgur_url = f"https://rimgo.pussthecat.org/a/{search}"
    else:
        no_results()
        return
    return get_imgur_image(imgur_url)


def get_imgur_image(imgur_url, alt="rimgo.pussthecat.org"):
    from lxml import html

    tree = html.fromstring(get(imgur_url.replace("imgur.com", f"{alt}")).content)
    images = tree.xpath("//div[contains(@class,'post__media')]//img/@src")
    return f"https://{alt}{random.choice(images)}" if images else no_results()



def artstation_prints(search=None):
    scraper = cloudscraper.create_scraper()
    orientation = "portrait" if screen_orientation() == "portrait" else "landscape"
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
        "Content-Type": "application/json",
    }
    assets = scraper.get(api, json=body, headers=headers).json()["data"]

    no_results() if isinstance(assets, str) else ok()
    # noinspection PyTypeChecker
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
    if blank(path):
        print("Please specify path to images")
        exit(1)
    if path and not path.endswith("/"):
        path = f"{path}/"
    if os.path.exists(path):
        return path + random.choice(
            list(
                filter(
                    lambda f: os.path.isfile(path + f) and filetype.guess(path + f).MIME.startswith("image"),
                    os.listdir(path),
                )
            )
        )
    return no_results()


def waifuim(search=None):
    orientation = "PORTRAIT" if screen_orientation() == "portrait" else "LANDSCAPE"
    accept = f"&included_tags={search}" if search else ""
    reject = ""
    if search and "-" in search:
        accept = f"&selected_tags={search.split('-')[0]}"
        reject = f"&excluded_tags={search.split('-')[1]}"
    api = (
        f"https://api.waifu.im/search/?gif=false&is_nsfw=false"
        f"&orientation={orientation}{accept}{reject}"
    )
    response = get(api).json()
    no_results() if "detail" in response else ok()
    return response["images"][0]["url"]


# experimental
def musicbrainz(search=None):
    print("[!] This source is experimental")
    import musicbrainzngs as mb  # type: ignore

    if blank(search):
        print("Please enter [artist]-[album]")
        exit(1)
    mb.set_useragent("wanda", "*", user_agent["User-Agent"])
    [artist, album] = search.split("-")
    try:
        albums = mb.search_releases(album, artist=artist)
        ok() if albums else no_results()
        if not albums["release-list"]:
            raise mb.MusicBrainzError
        album_id = albums["release-list"][0]["release-group"]["id"]
        cover = mb.get_release_group_image_front(album_id)
        path = get_dl_path()
        with open(path, "wb") as f:
            f.write(cover)
        ext = filetype.guess(path).EXTENSION
        os.rename(path, f"{path}.{ext}")
        return f"{path}.{ext}"
    except mb.MusicBrainzError:
        no_results()


def wallhaven(search=None):
    api = "https://wallhaven.cc/api/v1/search?sorting=random"
    ratios = "portrait" if screen_orientation() == "portrait" else "landscape"
    response = get(f"{api}&ratios={ratios}&q={search or ''}").json()["data"]
    return response[0]["path"] if response else no_results()


def unsplash(search=None):
    api = f"https://source.unsplash.com/random/{size()[0]}x{size()[1]}/?{search or 'wallpaper'}"
    response = get(api).url
    return response if "source-404" not in response else no_results()


def earthview(_):  # NOSONAR
    from lxml import html  # type: ignore
    folder = appdirs.user_cache_dir("wanda")
    tree = html.fromstring(get("https://earthview.withgoogle.com").content)
    url = json.loads(tree.xpath("//body/@data-photo")[0])["photoUrl"]
    ext = url.split(".")[-1]
    if screen_orientation() == "landscape":
        return url
    path = os.path.normpath(f"{folder}/wanda_{int(time.time())}.{ext}")
    path = download(path, url)
    from PIL import Image  # type: ignore

    image = Image.open(path)
    image.rotate(90)
    image.save(path)
    return path
