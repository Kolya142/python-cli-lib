import time
from random import randint
from math import sqrt
from typing import List

import keyboard

# Import your cli library
import cli

cli.init()
bx = 30
by = 5
# blocks = list(cli.Sprite.from_img(0, 0, 'boid-level1').frame.keys())
# blocks = [(b[0]-bx, b[1]-by) for b in blocks]
blocks = []
xtree = list(cli.Sprite.from_img(0, 0, 'xtree').frame.keys())
xtree_not = []

# Constants
SOME_THRESHOLD = 5  # Boids start avoiding the block when closer than 30 units
COLLISION_AVOIDANCE_FACTOR = 0.1  # Boids adjust their velocity by 5% to avoid the block
BOID_VISION_RANGE = 20
BOID_PROTECTED_RANGE_SQUARED = 4
BOID_CENTERING_FACTOR = 0.01
BOID_MATCHING_FACTOR = 0.05
BOID_MATCHING_MOUSE_FACTOR = 0.05
BOID_AVOID_FACTOR = 0.01
BOID_MIN_SPEED = 0.5
BOID_MAX_SPEED = 3
BOID_TURN_FACTOR = 0.1


def clamp(v, a, b):
    return min(max(v, a), b)


def get_char_and_color(speed):
    # Character set for the gradient
    cset = '.,-+=oxmg%#@'
    # Windows CMD color set (foreground colors)
    colors = [
        (0, 0, 0),  # Black
        (0, 0, 128),  # Dark Blue
        (0, 128, 0),  # Dark Green
        (0, 128, 128),  # Dark Cyan
        (128, 0, 0),  # Dark Red
        (128, 0, 128),  # Dark Magenta
        (128, 128, 0),  # Dark Yellow
        (192, 192, 192),  # Light Gray
        (128, 128, 128),  # Dark Gray
        (0, 0, 255),  # Blue
        (0, 255, 0),  # Green
        (0, 255, 255),  # Cyan
        (255, 0, 0),  # Red
        (255, 0, 255),  # Magenta
        (255, 255, 0),  # Yellow
        (255, 255, 255)  # White
    ]

    # Normalize speed to range [0, 1]
    normalized_speed = (speed - BOID_MIN_SPEED) / (BOID_MAX_SPEED - BOID_MIN_SPEED)

    # Get index for character and color
    char_index = int(normalized_speed * (len(cset) - 1))
    color_index = int(normalized_speed * (len(colors) - 1))

    # Clamp indices to valid range
    char_index = clamp(char_index, 0, len(cset) - 1)
    color_index = clamp(color_index, 0, len(colors) - 1)

    # Get character and color
    char = cset[char_index]
    color = colors[color_index]

    return char, color


class Boid:
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y
        self._stop = False
        self.vx, self.vy = randint(-100, 100) / 100, randint(-100, 100) / 100
        while (self.x, self.y) in blocks:
            self.x, self.y = randint(0, cli.size[0]), randint(0, cli.size[1])

    def stop(self, a=None):
        if a is None:
            self._stop = not self._stop
            return
        self._stop = not not a

    def is_stopped(self):
        return self._stop

    def update(self, boids: List['Boid']):
        if self._stop:
            speed = sqrt(self.vx ** 2 + self.vy ** 2)
            c, f = get_char_and_color(speed)
            cli.rect(int(self.x), int(self.y), 0, 0, c, f, (0, 0, 0))
            return
        xpos_avg, ypos_avg, xvel_avg, yvel_avg = 0, 0, 0, 0
        neighboring_boids = 0
        close_dx, close_dy = 0, 0

        if keyboard.is_pressed('space'):
            mouse_pos = cli.getRelativePos()
            if mouse_pos != (-1, -1):
                # Calculate direction towards the mouse
                towards_mouse_dx = mouse_pos[0] - self.x
                towards_mouse_dy = mouse_pos[1] - self.y
                dist = ((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) ** 0.5
                dist /= 10

                # Adjust velocity slightly towards the mouse
                self.vx += towards_mouse_dx * BOID_MATCHING_MOUSE_FACTOR / dist
                self.vy += towards_mouse_dy * BOID_MATCHING_MOUSE_FACTOR / dist

        if keyboard.is_pressed('z'):
            mouse_pos = cli.getRelativePos()
            if mouse_pos != (-1, -1):
                # Calculate direction towards the mouse
                towards_mouse_dx = mouse_pos[0] - self.x
                towards_mouse_dy = mouse_pos[1] - self.y
                dist = ((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) ** 0.5
                dist /= 5

                # Adjust velocity slightly towards the mouse
                self.vx -= towards_mouse_dx * BOID_MATCHING_MOUSE_FACTOR / dist
                self.vy -= towards_mouse_dy * BOID_MATCHING_MOUSE_FACTOR / dist

        for otherboid in boids:
            if otherboid is self:
                continue

            dx, dy = self.x - otherboid.x, self.y - otherboid.y
            squared_distance = dx ** 2 + dy ** 2

            if squared_distance < BOID_PROTECTED_RANGE_SQUARED:
                close_dx += dx
                close_dy += dy
            elif squared_distance < BOID_VISION_RANGE ** 2:
                if not otherboid.is_stopped():
                    xpos_avg += otherboid.x
                    ypos_avg += otherboid.y
                    xvel_avg += otherboid.vx
                    yvel_avg += otherboid.vy
                    neighboring_boids += 1

        for block in blocks:
            block_dx, block_dy = self.x - block[0], self.y - block[1]
            distance_to_block = sqrt(block_dx ** 2 + block_dy ** 2)

            if distance_to_block < SOME_THRESHOLD:  # Define a suitable threshold
                # Adjust velocity to steer away from the block
                self.vx -= block_dx * COLLISION_AVOIDANCE_FACTOR
                self.vy -= block_dy * COLLISION_AVOIDANCE_FACTOR

        if neighboring_boids > 0:
            xpos_avg /= neighboring_boids
            ypos_avg /= neighboring_boids
            xvel_avg /= neighboring_boids
            yvel_avg /= neighboring_boids

            self.vx += (xpos_avg - self.x) * BOID_CENTERING_FACTOR + (xvel_avg - self.vx) * BOID_MATCHING_FACTOR
            self.vy += (ypos_avg - self.y) * BOID_CENTERING_FACTOR + (yvel_avg - self.vy) * BOID_MATCHING_FACTOR

        self.vx += close_dx * BOID_AVOID_FACTOR
        self.vy += close_dy * BOID_AVOID_FACTOR

        # Handle boundaries (assuming wrap-around logic)
        if self.x < 0:
            self.x = cli.size[0]
        if self.x > cli.size[0]:
            self.x = 0
        if self.y > cli.size[1]:
            self.y = 0
        if self.y < 0:
            self.y = cli.size[1]

        # Enforce min and max speed
        speed = sqrt(self.vx ** 2 + self.vy ** 2)
        if speed < BOID_MIN_SPEED:
            self.vx = (self.vx / speed) * BOID_MIN_SPEED
            self.vy = (self.vy / speed) * BOID_MIN_SPEED
        elif speed > BOID_MAX_SPEED:
            self.vx = (self.vx / speed) * BOID_MAX_SPEED
            self.vy = (self.vy / speed) * BOID_MAX_SPEED

        self.x += self.vx
        self.y += self.vy
        c, f = get_char_and_color(speed)

        # Draw the boid
        cli.rect(int(self.x), int(self.y), 0, 0, c, f, (0, 0, 0))


# Initialize boids
boids = [Boid(randint(0, cli.size[0]), randint(0, cli.size[1])) for _ in range(200)]
t = time.time()
tree_show = False

# Main loop
while True:
    # time.sleep(1/10)
    # if time.time()-t > 2:
    #     t = time.time()
    #     for boid in boids:
    #         boid.stop()
    cli.clear()
    for boid in boids:
        boid.update(boids)
        if tree_show:
            if (int(boid.x), int(boid.y)) in xtree and (int(boid.x), int(boid.y)) not in xtree_not:
                boid.stop(1)
                xtree_not.append((int(boid.x), int(boid.y)))
        else:
            boid.stop(0)
    if keyboard.is_pressed('q'):
        tree_show = True
    if keyboard.is_pressed('w'):
        xtree_not = []
        tree_show = False
    for block in blocks:
        cli.rect(block[0], block[1], 0, 0, 'B', (255, 255, 255), (0, 0, 0))
    cli.update()
    cli.draw()
