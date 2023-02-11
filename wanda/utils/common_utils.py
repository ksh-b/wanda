import os
import subprocess
import time

import appdirs
import cloudscraper  # type: ignore
import filetype  # type: ignore

folder = appdirs.user_cache_dir("wanda")


def command(string: str) -> str:
    return subprocess.check_output(string.split(" ")).decode().strip()


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
    ext = filetype.guess(path).EXTENSION
    os.rename(path, f"{path}.{ext}")
    return f"{path}.{ext}"


def get(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url, headers={"User-Agent": "git.io/wanda"}, timeout=10)
    if response.status_code != 200:
        from http.client import responses
        print(f"Got status code [{responses[response.status_code]}] from {url}")
        exit(1)
    return response


def blank(search):
    return not search or search == ""


def contains(word: str, match_all: bool, desired: list) -> bool:
    matches = list(
        map(lambda w: w not in word if w.startswith("!") else w in word, desired)
    )
    if not match_all:
        return True in matches
    return set(matches) == {True}


def is_connected():
    # noinspection PyBroadException
    try:
        result = get("https://detectportal.firefox.com/success.txt")
        return result.text.strip() == "success"
    except Exception:
        return False


# do nothing
def ok():
    pass
