import math
import random
import time
from typing import List, Tuple

import cli
import keyboard
import pymunk
cli.init()


space = pymunk.Space()
space.gravity = 0, -1000
space.damping = 0.5

floor_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
floor_shape = pymunk.Segment(floor_body, (0, 0), (cli.size[0], 0), 1)
floor_shape.elasticity = 0.4
floor_shape.friction = 1.0
space.add(floor_body, floor_shape)

wall_left_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
wall_left_shape = pymunk.Segment(wall_left_body, (0, 0), (0, cli.size[1]), 1)
wall_left_shape.elasticity = 0.4
wall_left_shape.friction = 1.0
space.add(wall_left_body, wall_left_shape)

wall_right_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
wall_right_shape = pymunk.Segment(wall_right_body, (cli.size[0], 0), (cli.size[0], cli.size[1]), 1)
wall_right_shape.elasticity = 0.4
wall_right_shape.friction = 1.0
space.add(wall_right_body, wall_right_shape)

circles: List[Tuple[pymunk.Body, float]] = []
t = time.time()-10
while True:
    pos = cli.getRelativePos()
    cli.clear()
    cli.blit_text(0, 0, str(circles))
    for i in range(0, cli.size[0]):
        cli.set_color_bg(i, cli.size[1]-1, 200, 200, 200)
    for j in range(0, cli.size[1]):
        cli.set_color_bg(0, cli.size[1], 200, 200, 200)
    for body, r in circles:
        if str(body.position.x) != "nan" and str(cli.size[1]-body.position.y) != "nan":
            # print(body.position)
            if r == 2:
                for x in range(int(body.position.x)-1, int(body.position.x)+1):
                    for y in range(int(cli.size[1] - body.position.y) - 1, int(cli.size[1] - body.position.y) + 1):
                        cli.set_color_bg(x, y, 255, 0, 0)
            elif r == 3:
                for x in range(int(body.position.x)-1, int(body.position.x)+2):
                    for y in range(int(cli.size[1] - body.position.y) - 1, int(cli.size[1] - body.position.y) + 2):
                        cli.set_color_bg(x, y, 255, 0, 0)
            else:
                cli.set_color_bg(int(body.position.x), int(cli.size[1]-body.position.y), 255, 0, 0)
    if pos != (-1, -1):
        if keyboard.is_pressed("space"):
            body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
            body.position = pymunk.Vec2d(pos[0], cli.size[1]-pos[1])
            shape = pymunk.Circle(body, random.randint(1, 3))
            shape.density = 0.1
            shape.elasticity = 0.9
            shape.friction = 0.7
            space.add(body, shape)
            circles.append((body, shape.radius))
    space.step(1/60)
    t = time.time()
    cli.update()
    cli.draw()

