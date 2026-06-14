import base64
import os
import random
from pathlib import Path

import cloudscraper  # type: ignore
import filetype  # type: ignore
from PIL import Image  # type: ignore

from wanda.sources.earthview_ids import earthview_ids
from wanda.sources.generator.gradient1 import linear_gradient
from wanda.sources.generator.gradient2 import bilinear_gradient
from wanda.sources.generator.tiles import tiles
from wanda.utils.common_utils import blank, get, ok, contains, get_dl_path
from wanda.utils.const import user_agent
from wanda.utils.image_utils import screen_orientation, good_size
from wanda.utils.os_utils import size

def no_results():
    print("No results found.")
    print("• Try another source or term")
    print("• Try again at a later time")
    exit(1)


def fourchan(search=None):
    scraper = cloudscraper.create_scraper()
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
    response = scraper.get(api, headers=user_agent).json()
    no_results() if "error" in response else ok()
    posts = list(
        filter(lambda p: "media" in p and "nimages" in p, response["0"]["posts"])
    )
    ok() if posts else no_results()
    post = random.choice(posts)
    thread = post["thread_num"]
    board = post["board"]["shortname"]
    api = f"https://archive.palanq.win/_/api/chan/thread/?board={board}&num={thread}"
    posts = scraper.get(api, headers=user_agent).json()[thread]["posts"]
    ok() if posts else no_results()
    post = random.choice(list(filter(lambda p: "media" in posts[p], posts)))
    if posts[post]:
        return posts[post]['media']['remote_media_link']
    return no_results()

def is_imgur_gallery(url):
    return contains(url, False, ["imgur.com/a", "imgur.com/gallery"])


def picsum(search=None):
    w, h = size()
    if blank(search):
        api = f"https://picsum.photos/{w}/{h}"
    else:
        api = f"https://picsum.photos/seed/{search}/{w}/{h}"
    return get(api).url


def imgur(alt="rmgur.com", search=None):
    if search:
        from lxml import html
        tree = html.fromstring(get(f"https://{alt}/a/{search}").content)
        images = tree.xpath("//main//img[@loading]")
        return f"https://{alt}{random.choice(images).attrib['src']}" if images else no_results()
    return no_results()


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
    scraper = cloudscraper.create_scraper()
    if blank(search):
        print("Please provide an artist id")
        exit(1)
    response = scraper.get(f"https://www.artstation.com/users/{search}/hovercard.json", headers=user_agent)
    no_results() if response.status_code != 200 else ok()
    projects = scraper.get(f"https://www.artstation.com/users/{search}/projects.json", headers=user_agent).json()
    artwork = random.choice(projects["data"])["permalink"].split("/")[-1]
    return scraper.get(
        f"https://www.artstation.com/projects/{artwork}.json", headers=user_agent
    ).json()["assets"][
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
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:151.0) Gecko/20100101 Firefox/151.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
    }
    assets = scraper.get(api, json=body, headers=headers).json()["data"]

    no_results() if isinstance(assets, str) else ok()
    # noinspection PyTypeChecker
    hash_id = random.choice(assets)["hash_id"] if assets else no_results()

    api = f"https://www.artstation.com/projects/{hash_id}.json"
    assets = scraper.get(api, headers=headers).json()["assets"]
    random.shuffle(assets) if assets else no_results()
    for asset in assets:
        h = asset["height"]
        w = asset["width"]
        if good_size(w, h):
            return asset["image_url"]
    return random.choice(assets)["image_url"]


def local(path: str):
    if blank(path):
        print("Please specify path to images")
        exit(1)
    if path and not path.endswith("/"):
        path = f"{path}/"
    p = Path(path)
    if not p.exists() or not p.is_dir():
        return None

    images = []
    for entry in p.iterdir():
        if not entry.is_file():
            continue
        kind = filetype.guess(entry)
        if kind is None:
            continue
        if getattr(kind, "MIME", "").startswith("image"):
            images.append(str(entry))

    if not images:
        return no_results()

    return random.choice(images)


def waifuim(search=None):
    orientation = "portrait" if screen_orientation() == "portrait" else "landscape"
    accept = f"&IncludedTags={search}" if search else ""
    api = (
        f"https://api.waifu.im/images?"
        f"OrderBy=Random"
        f"&Orientation={orientation}"
        f"{accept}"
    )
    response = get(api).json()
    no_results() if not response['items'] else ok()
    return response["items"][0]["url"]


def musicbrainz(search=None):
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


def earthview(_):
    # https://chromewebstore.google.com/detail/earth-view-from-google-ea/bhloflhklmhfpedakmangadcdofhnnoh
    # 3.1.0
    url = f"https://www.gstatic.com/prettyearth/assets/data/v3/{random.choice(earthview_ids)}.json"
    response = get(url)
    data = response.json()
    image_data = data.get("dataUri", "")

    if image_data:
        image_data = image_data.split(",")[-1]
        image_bytes = base64.b64decode(image_data)
        filename = get_dl_path("jpg")
        with open(filename, "wb") as f:
            f.write(image_bytes)

        if screen_orientation() == "portrait":
            image = Image.open(filename)
            rotated_image = image.rotate(90, expand=True)
            rotated_image.save(filename)

        return filename
    return no_results()


def generate(term):
    path = get_dl_path("png")
    w, h = size()
    if term == "linear" or term == "gl":
        image = linear_gradient(w, h)
    elif term == "bilinear" or term == "gb":
        image = bilinear_gradient(w, h)
    elif term == "tiles" or term == "t":
        image = tiles(w, h)
    else:
        term = random.choice(["gl", "gb", "t"])
        return generate(term)

    image.save(path)
    return path
