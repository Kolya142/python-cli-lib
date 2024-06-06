import vnoise

import cli
from vec import Vec2d

cli.init()
noise = vnoise.Noise()
camera_offset = Vec2d(0, 0)
colors = [
    (255, 255, 0),
    (0, 255, 0)
]


def color_mix(value):
    r = colors[0][0] * value + colors[1][0] * (1 - value)
    g = colors[0][1] * value + colors[1][1] * (1 - value)
    b = colors[0][2] * value + colors[1][2] * (1 - value)
    return r, g, b


def make_sprite():
    frame = {}
    for i in range(0, cli.size[0], 2):
        for j in range(0, cli.size[1], 2):
            # Generate noise-based value
            value = noise.noise2((i + camera_offset.x) * 0.1, (j + camera_offset.y) * 0.1)
            # Calculate grayscale color based on noise value
            color = (abs(value) * 255, abs(value) * 255, abs(value) * 255)
            color = color, (0, 0, 0), "."
            frame[(i, j)] = color
            frame[(i + 1, j)] = color
            frame[(i, j + 1)] = color
            frame[(i + 1, j + 1)] = color
    return cli.Sprite(0, 0, frame)


while True:
    sprite = make_sprite()
    sprite.update(0, 0)
    cli.update()
    cli.draw()
