from PIL import Image, ImageDraw

from wanda.sources.generator.scheme import generate_random_color
from wanda.utils.common_utils import coin_toss


def linear_gradient(width, height):
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    start_color = generate_random_color(True)
    end_color = generate_random_color(True)

    if coin_toss():
        for x in range(width):
            r = int(start_color[0] * (1 - x / width) + end_color[0] * (x / width))
            g = int(start_color[1] * (1 - x / width) + end_color[1] * (x / width))
            b = int(start_color[2] * (1 - x / width) + end_color[2] * (x / width))
            for y in range(height):
                draw.point((x, y), fill=(r, g, b))
    else:
        for y in range(height):
            r = int(start_color[0] * (1 - y / height) + end_color[0] * (y / height))
            g = int(start_color[1] * (1 - y / height) + end_color[1] * (y / height))
            b = int(start_color[2] * (1 - y / height) + end_color[2] * (y / height))
            for x in range(width):
                draw.point((x, y), fill=(r, g, b))

    return image
