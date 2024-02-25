import random

import requests

from wanda.utils.common_utils import coin_toss


def generate_random_color(as_rgb=False):
    while True:
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        if r > 200 and g < 150 < b:
            continue
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        if max_val == 0:
            saturation = 0
        else:
            saturation = 1 - min_val / max_val
        if saturation < 1.0:
            if as_rgb:
                return r, g, b
            return "#{:02x}{:02x}{:02x}".format(r, g, b)


def rearrange_colors(colors_list):
    sorted_colors = sorted(colors_list, key=lambda color: sum(color))
    if coin_toss:
        sorted_colors.reverse()
    return sorted_colors


def get_color_scheme(count=5):
    modes = ["monochrome", "monochrome-dark", "monochrome-light"]

    random_mode = random.choice(modes)
    random_hex = generate_random_color()
    url = "https://www.thecolorapi.com/scheme"
    params = {"hex": random_hex, "mode": random_mode, "count": count}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            response_data = response.json()
            colors_list = [
                (color["rgb"]["r"], color["rgb"]["g"], color["rgb"]["b"])
                for color in response_data["colors"]
            ]
            return rearrange_colors(colors_list)
        else:
            colors_list = [(generate_random_color(True)) for _ in range(count)]
            return rearrange_colors(colors_list)
    except:
        colors_list = [(generate_random_color(True)) for _ in range(count)]
        return rearrange_colors(colors_list)


def invalid_number(maybe_number):
    return not maybe_number or not (isinstance(maybe_number, int))
