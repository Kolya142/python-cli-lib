import dataclasses
from typing import Dict, Callable, final, Final

import cli
from cli import Image
from vec import Vec2d, Vec3d


@dataclasses.dataclass
class Pixel:
    char: str
    fg: Vec3d
    bg: Vec3d


uniform_type = str | int | float | Vec2d | Image


def save_image() -> Image:
    return Image(cli.screen, cli.screen_color_fg, cli.screen_color_bg)


def blit_image(image: Image):
    cli.screen = image.image
    cli.screen_color_fg = image.color_fg
    cli.screen_color_bg = image.color_bg


class Shader:
    resolution: Vec2d = None
    uniforms: Dict[str, uniform_type] = None
    pixel_aspect: Final[float] = 11/24

    @final
    def set_uniform(self, name: str, data: uniform_type) -> None:
        self.uniforms[name] = data

    @final
    def set_resolution(self, resolution: Vec2d):
        self.resolution = resolution

    @final
    def texture(self, texture: Image, uv: Vec2d):
        c = texture.image[int(uv.y)][int(uv.x)]
        f = texture.color_fg[int(uv.y)][int(uv.x)]
        b = texture.color_bg[int(uv.y)][int(uv.x)]
        return Pixel(c, f, b)

    @final
    def __init__(self):
        self.uniforms = {}

    def draw(self, pos: Vec2d) -> Pixel:
        raise NotImplementedError()


def update_shader(shader: Shader) -> Image:
    screen_width, screen_height = shader.resolution.to_list()
    shader.set_resolution(Vec2d(screen_width, screen_height))

    new_image = [[None for _ in range(screen_width)] for _ in range(screen_height)]
    new_color_fg = [[None for _ in range(screen_width)] for _ in range(screen_height)]
    new_color_bg = [[None for _ in range(screen_width)] for _ in range(screen_height)]

    for y in range(screen_height):
        for x in range(screen_width):
            pos = Vec2d(x, y)
            pixel = shader.draw(pos)
            new_image[y][x] = pixel.char
            new_color_fg[y][x] = (pixel.fg * 255).int().to_list()
            new_color_bg[y][x] = (pixel.bg * 255).int().to_list()
    return Image(new_image, new_color_fg, new_color_bg)
