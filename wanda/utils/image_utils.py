import os

from wanda.utils.common_utils import get_dl_path, download
from wanda.utils.os_utils import size, set_wp_android, set_wp_linux, set_wp_win, is_android


def screen_orientation():
    return "landscape" if size()[0] > size()[1] else "portrait"


def image_orientation(image):
    return "landscape" if image.width > image.height else "portrait"


def good_size(w, h):
    return (screen_orientation() == "portrait" and w < h) or (
            screen_orientation() == "landscape" and w > h
    )


# get dominant color from image
def dominant_color(wallpaper_path):
    from colorthief import ColorThief  # type: ignore

    color_thief = ColorThief(wallpaper_path)
    return color_thief.get_color(quality=1)


def fit(wallpaper_path):
    from PIL import Image

    wp = Image.open(wallpaper_path)
    scr_width, scr_height = size()

    # if image is squarish (like album art)
    if 95 < int(wp.width / wp.height) * 100 < 105:
        bg = Image.new("RGB", (size()), dominant_color(wallpaper_path))
        percentage = 0
        if screen_orientation() == "portrait" and wp.width > scr_width:
            percentage = wp.width / scr_width
        elif screen_orientation() == "landscape" and wp.height > scr_height:
            percentage = wp.height / scr_height
        if percentage != 0:
            print("Fitting // squarish image")
            resized_dimensions = (
                int(wp.width / percentage),
                int(wp.height / percentage),
            )
            resized = wp.resize(resized_dimensions)
            x1 = int(scr_width / 2) - int(resized.width / 2)
            y1 = int(scr_height / 2) - int(resized.height / 2)
            bg.paste(resized, (x1, y1))
            bg.save(wallpaper_path)

    # image smaller than screen
    elif wp.height < scr_height and wp.width < scr_width:
        print("Fitting // image smaller than screen")
        bg = Image.new("RGB", (size()), dominant_color(wallpaper_path))
        x1 = int(scr_width / 2) - int(wp.width / 2)
        y1 = int(scr_height / 2) - int(wp.height / 2)
        bg.paste(wp, (x1, y1))
        bg.save(wallpaper_path)

    # image == portrait but screen == landscape
    elif image_orientation(wp) == "portrait" and screen_orientation() == "landscape":
        print("Fitting // image is portrait but screen is landscape")
        bg = Image.new("RGB", (size()), dominant_color(wallpaper_path))
        percentage = wp.height / scr_height
        resized_dimensions = (
            int(wp.width / percentage),
            int(wp.height / percentage),
        )
        resized = wp.resize(resized_dimensions)
        x1 = int(scr_width / 2) - int(resized.width / 2)
        y1 = 0
        bg.paste(resized, (x1, y1))
        bg.save(wallpaper_path)

    # image == landscape but screen == portrait
    elif image_orientation(wp) == "landscape" and screen_orientation() == "portrait":
        print("Fitting // image is landscape but screen is portrait")
        bg = Image.new("RGB", (size()), dominant_color(wallpaper_path))
        percentage = wp.width / scr_width
        resized_dimensions = (
            int(wp.width / percentage),
            int(wp.height / percentage),
        )
        resized = wp.resize(resized_dimensions)
        x1 = 0
        y1 = int(scr_height / 2) - int(resized.height / 2)
        bg.paste(resized, (x1, y1))
        bg.save(wallpaper_path)

    return wallpaper_path


def set_wp(url: str, home=True, lock=True, fitwp=False):
    # print selected wallpaper url
    print(url)

    # download wallpaper
    if url.replace("http://", "https://").startswith("https://"):
        path = get_dl_path()
        path = download(path, url)
    elif os.path.exists(url):
        path = url
    else:
        print("Invalid url/path")
        return 1

    # fit wallpaper to screen if orientation mismatch
    if fitwp:
        path = fit(path)

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
