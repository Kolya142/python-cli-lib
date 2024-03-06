from random import randint
import time
from typing import List
import vnoise

import keyboard

import cli

cli.init()
noise = vnoise.Noise()
door = cli.Sprite.from_img(15, 5, 'door')
doors_count = 100
doors = [randint(0, 4) for _ in range(doors_count)]


def gen_sprite():
    global level
    frame = {}
    for i in range(cli.size[0]):
        for j in range(cli.size[1]):
            col = [int(noise.noise3(i / cli.size[0], j / cli.size[1], level + 0.1) * 255) % 255,
                   int(noise.noise3(i / cli.size[0], j / cli.size[1], level + 0.3) * 255) % 255,
                   int(noise.noise3(i / cli.size[0], j / cli.size[1], level + .01) * 255) % 255
                   ]
            col[0] = max(0, col[0])
            col[1] = max(0, col[1])
            col[2] = max(0, col[2])
            frame[(i, j)] = ((0, 0, 0), col, '█')
    return cli.Sprite(0, 0, frame)


idkfa_active = False
cheat_last = ''
cheat_active = False
i_lt = 0
d_lt = 0
k_lt = 0
f_lt = 0
a_lt = 0
level = 0
doors_image: List[cli.Sprite] = [gen_sprite()]
errors = 0
lt = 0

while True:
    if level == len(doors_image):
        doors_image.append(gen_sprite())
    doors_image[level].update(0, 0)
    cli.blit_text(cli.size[0] - 20, cli.size[1] - 2, f'return to start: o')
    cli.blit_text(1, cli.size[1] - 2, f'errors: {errors}')
    cli.blit_text(1, cli.size[1] - 3, f'level: {level}')
    if cheat_active:
        cli.blit_text(1, 0, f'{doors[level] + 1}')
    cli.blit_text(9, 2, 'key: 1')
    door.update(5, 4)
    cli.blit_text(door.width + 14, 2, 'key: 2')
    door.update(door.width + 10, 4)
    cli.blit_text(door.width * 2 + 18, 2, 'key: 3')
    door.update(door.width * 2 + 15, 4)
    cli.blit_text(door.width * 3 + 24, 2, 'key: 4')
    door.update(door.width * 3 + 20, 4)
    cli.blit_text(door.width * 4 + 28, 2, 'key: 5')
    door.update(door.width * 4 + 25, 4)
    if keyboard.is_pressed('o'):
        level = 0
        errors = 0
    if time.time() - lt > 0.5:
        if keyboard.is_pressed('1'):
            lt = time.time()
            if doors[level] == 0:
                level += 1
            else:
                errors += 1
        if keyboard.is_pressed('2'):
            lt = time.time()
            if doors[level] == 1:
                level += 1
            else:
                errors += 1
        if keyboard.is_pressed('3'):
            lt = time.time()
            if doors[level] == 2:
                level += 1
            else:
                errors += 1
        if keyboard.is_pressed('4'):
            lt = time.time()
            if doors[level] == 3:
                level += 1
            else:
                errors += 1
        if keyboard.is_pressed('5'):
            lt = time.time()
            if doors[level] == 4:
                level += 1
            else:
                errors += 1
    if cheat_last:
        if keyboard.read_key() not in 'idkfa':
            cheat_last = ''
    if keyboard.is_pressed('i') and time.time() - i_lt > 0.1:
        cheat_last = 'i'
    if keyboard.is_pressed('d') and time.time() - d_lt > 0.1 and cheat_last == 'i':
        cheat_last = 'd'
    if keyboard.is_pressed('k') and time.time() - k_lt > 0.1 and cheat_last == 'd':
        cheat_last = 'k'
    if keyboard.is_pressed('f') and time.time() - f_lt > 0.1 and cheat_last == 'k':
        cheat_last = 'f'
    if keyboard.is_pressed('a') and time.time() - a_lt > 0.1 and cheat_last == 'f':
        cheat_last = ''
        cheat_active = not cheat_active

    cli.update()
    cli.draw()
