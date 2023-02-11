import argparse
import json
import sys
from pathlib import Path

import appdirs

import wanda.utils.common_utils as common
import wanda.utils.image_utils as image
import wanda.utils.os_utils as osu
import wanda.sources as sources

folder = appdirs.user_cache_dir("wanda")
version = "0.61.1"


def usage(level=0):
    cyan = "\033[36m"
    pink = "\033[35m"
    print("Sources:")
    print(f"{cyan}4chan {pink}[keyword]|[keyword@board]")
    print(f"{cyan}500{cyan}px {pink}[keyword]")
    print(f"{cyan}arstation {pink}[keyword]")
    print(f"{cyan}arstation_{cyan}artist {pink}[id of artist]")
    print(f"{cyan}arstation_{cyan}prints {pink}[keyword for prints]")
    print(f"{cyan}imgur {pink}[gallery id. example: qF259WO]")
    print(f"{cyan}earthview")
    print(f"{cyan}local {pink}[full path to folder]")
    print(f"{cyan}musicbrainz {pink}[artist-album]")
    print(f"{cyan}picsum")
    print(f"{cyan}reddit {pink}[keyword]|[keyword@subreddit]")
    print(f"{cyan}unsplash {pink}[keyword]")
    print(f"{cyan}wallhaven {pink}[keyword(,keyword2,keyword3...&)]")
    print(f"{cyan}waifu.im {pink}[selected_tag-(excluded_tag)]")
    print()
    print("Use double quotes around your keyword or path if it has spaces")

    if level >= 1:
        print("Wallhaven advanced usage:")
        print("For full list of parameters, go to https://wallhaven.cc/help/api#search")
        print(
            "example: wanda -sw -tcar,lamborghini&colors=cc3333&categories=111&purity=100"
        )

    if level >= 2:
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
        nargs="?",
        const=str(Path.home()),
        help="Copy last downloaded wallpaper to home directory or given path",
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
    parser_.add_argument(
        "-f",
        help="Fit wallpaper to screen if screen and wallpaper orientation mismatch",
        required=False,
        action="store_true",
    )
    if osu.is_android():
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
        usage(2)
        exit(0)
    if "-v" in sys.argv:
        print(args.v)
        exit(0)
    if "-d" in sys.argv:
        for src_file in Path(folder).glob("wanda_*.*"):
            import shutil
            shutil.copy(src_file, args.d)
            print(f"Copied wallpaper to {args.d}")
        exit(0)

    source = args.s
    term = args.t
    home = True
    lock = True
    fitwp = False
    if "-l" in sys.argv and args.l:
        home = False
    if "-h" in sys.argv and args.h:
        lock = False
    if "-f" in sys.argv and source not in ('e', 'earthview'):
        fitwp = True
    try:
        if source != "local" and not common.is_connected():
            print("Please check your internet connection and try again")
            exit(1)
        image.set_wp(eval(f"sources.{source_map(source)}")(term), home, lock, fitwp)
    except NameError:
        print(f"Unknown source: '{source}'")
        usage()

    return 0


def shortcodes():
    return {
        "4": "fourchan",
        "5": "fivehundredpx",
        "a": "artstation_any",
        "aa": "artstation_artist",
        "ap": "artstation_prints",
        "e": "earthview",
        "i": "imgur",
        "l": "local",
        "m": "musicbrainz",
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
