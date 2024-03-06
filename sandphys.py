import math
import random
import time
from math import sin, cos
from typing import Dict, Tuple

import cli
cli.init()
ANGLE_STEP_SIZE = 360/8
gravity = 0.1


class Obj:
    x: int = 0
    y: int = 0
    static: bool = False

    def __init__(self, x, y, vx, vy, static=False):
        self.x = x
        self.y = y
        self.space = space
        self.static = static
        self.vx = vx
        self.vy = vy

    def update(self, objects):
        # If the object is static, it should not be updated.
        if self.static:
            return

        # Apply gravity to the vertical velocity.
        self.vy += gravity

        # Store the original velocities to reset after collision detection.
        orig_vx, orig_vy = self.vx, self.vy

        # Define potential adjustments for collision resolution.
        # These seem intended to slightly adjust the object's position to avoid collision.
        putsx = [-1, 1, -1, 1]
        putsy = [1, 1, 0, 0]

        i = 0
        # Check for collision only if the object is moving.
        if int(self.vx) != 0 or int(self.vy) != 0:  # Use `or` instead of `and` to handle any movement.
            while (int(self.x + self.vx), int(self.y + self.vy)) in objects:
                # Adjust velocity based on the collision resolution arrays.
                # Reset to original velocities before applying adjustment to avoid compounding changes.
                self.vx = orig_vx + putsx[i]
                self.vy = orig_vy + putsy[i]
                i += 1
                # If all adjustments have been tried, stop the object.
                if i == len(putsx):
                    self.vx, self.vy = 0, 0
                    break

        # Normalize velocity to maintain constant speed in the direction of movement.
        magn = (self.vx ** 2 + self.vy ** 2) ** 0.5
        if magn != 0:
            self.vx /= magn
            self.vy /= magn

        # Update position based on the adjusted velocity.
        self.x += self.vx
        self.y += self.vy

        # Uncomment if positions should be integers.
        self.x = int(self.x)
        self.y = int(self.y)

    def draw(self):
        cli.rect(int(self.x), int(self.y), 0, 0, '@' if not self.static else '#', (255, 255, 255), (0, 0, 0))
        cli.rect(int(self.x+self.vx), int(self.y+self.vy), 0, 0, '0', (255, 255, 255), (0, 0, 0))


class Space:
    objects: Dict[Tuple[int, int], Obj] = {}
    fps: float = 10000
    _t = 0

    def __init__(self):
        self.size: Tuple[int, int] = cli.size

    def add_object(self, x, y, static=False):
        self.objects[(x, y)] = Obj(x, y, 0, 0, static)

    def update(self):
        update = False

        if time.time() - self._t > 1 / self.fps:
            self._t = time.time()
            update = True
        for j in range(self.size[1]):
            for i in range(self.size[0]):
                if (i, j) not in self.objects:
                    continue
                obj = self.objects[(i, j)]
                if update:
                    obj.update(self.objects)
                obj.draw()

        for j in range(self.size[1]):
            for i in range(self.size[0]):
                if (i, j) not in self.objects or self.objects[(i, j)].static:
                    continue
                obj = self.objects[(i, j)]
                self.objects[(int(obj.x), int(obj.y))] = self.objects.pop((i, j))


space = Space()
space.fps = 0.5
# space.add_object(5, 6)
# space.add_object(6, 6)
# space.add_object(7, 6)
# space.add_object(8, 6)
# space.add_object(5, 8)
# space.add_object(6, 9)
# space.add_object(7, 7)
# space.add_object(8, 10)
#
# space.add_object(5, 20, True)
# space.add_object(6, 20, True)
# space.add_object(7, 20, True)
# space.add_object(8, 20, True)
sprite = cli.Sprite.from_img(0, 0, 'phys-level')
level = sprite.frame
for pos in level:
    fg, bg, c = level[pos]
    x, y = pos
    if bg == (255, 0, 0):
        space.add_object(x, y)
    if bg == (0, 0, 255):
        space.add_object(x, y, True)


while True:
    cli.clear()
    space.update()
    # sprite.update(0, 0)
    cli.update()
    cli.draw()
