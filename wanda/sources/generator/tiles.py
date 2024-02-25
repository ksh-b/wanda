from PIL import Image, ImageDraw

from wanda.sources.generator.scheme import get_color_scheme, invalid_number


def tiles(width, height, tile_size=None, num_colors=None):
    if invalid_number(tile_size):
        tile_size = 50
    if invalid_number(num_colors):
        num_colors = 5

    colors = get_color_scheme(num_colors)
    texture = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(texture)

    for x in range(0, width, tile_size):
        for y in range(0, height, tile_size):
            color = colors[(x // tile_size + y // tile_size) % len(colors)]
            draw.rectangle((x, y, x + tile_size, y + tile_size), fill=color)

    # Save the generated texture
    return texture
