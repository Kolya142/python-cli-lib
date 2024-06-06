import time

import cli
import shaderlib
from vec import Vec2d, Vec3d


cli.init()


class Shader1(shaderlib.Shader):
    def draw(self, pos: Vec2d) -> shaderlib.Pixel:
        uv = pos / self.resolution
        uv += time.time()
        uv.x = uv.x % 1
        uv.y = uv.y % 1
        col = Vec3d(uv.x, uv.y)
        return shaderlib.Pixel(" ", Vec3d(0), col)


class Shader2(shaderlib.Shader):
    def draw(self, pos: Vec2d) -> shaderlib.Pixel:
        uv = pos / self.resolution * 2 - 1
        uv.x *= self.resolution.x / self.resolution.y
        uv.x *= self.pixel_aspect
        col = Vec3d(1) if uv.mag() < 0.5 else Vec3d(0)
        return shaderlib.Pixel(" ", Vec3d(0), col)


shader = Shader2()
cli.update()
shader.set_resolution(Vec2d.from_list(cli.size))

while True:
    cli.clear()
    # shader.set_uniform({"time", time.time()})
    image = shaderlib.update_shader(shader)
    # shaderlib.blit_image(image)
    cli.screen = image.image
    cli.screen_color_fg = image.color_fg
    cli.screen_color_bg = image.color_bg
    cli.update()
    shader.set_resolution(Vec2d.from_list(cli.size))
    cli.draw()
