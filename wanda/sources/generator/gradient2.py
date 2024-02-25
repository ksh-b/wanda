from PIL import Image, ImageDraw

from wanda.sources.generator.scheme import generate_random_color


def bilinear_gradient(width, height):
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    start_color = generate_random_color(True)
    end_color = generate_random_color(True)

    for y in range(height):
        for x in range(width):
            r = int(start_color[0] * (1 - x / width) + end_color[0] * (x / width))
            g = int(start_color[1] * (1 - y / height) + end_color[1] * (y / height))
            b = int(start_color[2] * (1 - x / width) + end_color[2] * (x / width))
            draw.point((x, y), fill=(r, g, b))

    return image
