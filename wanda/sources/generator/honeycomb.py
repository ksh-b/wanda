import math
import random

from PIL import Image, ImageDraw

from wanda.sources.generator.scheme import get_color_scheme, invalid_number


def draw_hexagon(draw, center, size, color, rotation=0):
    corners = []
    for i in range(6):
        angle_deg = 60 * i + rotation
        angle_rad = math.pi / 180 * angle_deg
        x = center[0] + size * math.cos(angle_rad)
        y = center[1] + size * math.sin(angle_rad)
        corners.append((x, y))
    draw.polygon(corners, fill=color, outline=color)


def honeycomb(
        width,
        height,
        count=None,
        hex_size=None,
        horizontal_spacing=None,
        vertical_spacing=None,
):
    if invalid_number(count):
        count = 4
    if invalid_number(hex_size):
        hex_size = 30
    if invalid_number(horizontal_spacing):
        horizontal_spacing = 2 * hex_size
    if invalid_number(vertical_spacing):
        vertical_spacing = math.sqrt(3) * hex_size

    colors = get_color_scheme(count)
    background_color = colors[0]
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    rows = int(height / vertical_spacing) + 2
    cols = int(width / horizontal_spacing) + 1

    for row in range(rows):
        for col in range(cols):
            x = col * horizontal_spacing + (row % 2) * (horizontal_spacing / 2)
            y = row * vertical_spacing
            color = random.choice(colors[1:])
            draw_hexagon(draw, (x, y), hex_size, color, rotation=30)

    # Save the image
    return image
