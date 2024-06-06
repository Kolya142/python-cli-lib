import time

import cli
import shaderlib
from vec import Vec2d, Vec3d


cli.init()


class Shader1(shaderlib.Shader):
    def draw(self, pos: Vec2d) -> shaderlib.Pixel:
        uv = pos + self.uniforms["time"]
        if uv.x > self.resolution.x:
            uv.x = 0
        if uv.y > self.resolution.y:
            uv.y = 0

        col = self.texture(self.uniforms["img"], uv)
        return col


shader = Shader1()
cli.update()
shader.set_resolution(Vec2d.from_list(cli.size))
cli.rect(5, 5, 4, 4, "*", (255, 255, 255), (0, 0, 0))
cli.draw()

while True:
    shader.set_uniform("img", cli.grab_image())
    shader.set_uniform("time", time.time())
    cli.clear()
    image = shaderlib.update_shader(shader)
    # shaderlib.blit_image(image)
    cli.screen = image.image
    cli.screen_color_fg = image.color_fg
    cli.screen_color_bg = image.color_bg
    cli.update()
    shader.set_resolution(Vec2d.from_list(cli.size))
    cli.draw()
