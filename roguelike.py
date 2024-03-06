import datetime
import os
import time

import keyboard

import cli

cli.init()
w, h = 30, 15


class Level:
    mapa = \
        "                              "\
        "                              "\
        "                              "\
        "                              "\
        "                              "\
        "                              "\
        "                              "\
        "                              "\
        "                              "\
        "                              "\
        "                              "\
        "                              "\
        "                              "\
        "                              "\
        "                              "
    up: 'Level' = None
    down: 'Level' = None
    left: 'Level' = None
    right: 'Level' = None


lev = 0
level = Level
check_point = (0, 0)
rec = None


def get_from_level(x, y):
    if x + y * w > len(level.mapa) or x + y * w < 0:
        return
    return level.mapa[x + y * w]


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.jmp = False
        self.jy = 0
        self.d = True

    def update(self):
        global check_point, rec, level

        if self.y == cli.size[1]-1:
            self.x, self.y = check_point
        dx = 0
        if keyboard.is_pressed("y"):
            pos = cli.getRelativePos()
            self.x, self.y = pos
        if keyboard.is_pressed("e"):
            check_point = self.x, self.y
        if keyboard.is_pressed("a"):
            self.d = False
            if get_from_level(self.x - 1, self.y) in ("@", "h"):
                dx = -1
            elif get_from_level(self.x - 1, self.y) == " " or get_from_level(self.x - 1, self.y - 1) == " ":
                dx = -1
                if get_from_level(self.x - 1, self.y - 1) == " " and get_from_level(self.x - 1, self.y) != " ":
                    self.y -= 1
        if keyboard.is_pressed("d"):
            self.d = True
            if get_from_level(self.x + 1, self.y) in ("@", "h"):
                dx = +1
            elif get_from_level(self.x + 1, self.y) == " " or get_from_level(self.x + 1, self.y - 1) == " ":
                dx = +1
                if get_from_level(self.x + 1, self.y - 1) == " " and get_from_level(self.x + 1, self.y) != " ":
                    self.y -= 1
        if (keyboard.is_pressed("space") and get_from_level(self.x, self.y + 1) in ("*", 'p')) or\
                get_from_level(self.x, self.y + 1) == '.':
            self.jmp = True
        if isinstance(rec, cli.Record):
            rec.update()
        if keyboard.is_pressed("r"):
            rec = cli.Record()
        if keyboard.is_pressed("t"):
            rec.write(f"replay_{datetime.datetime.now().strftime('%d,%m,%Y,%H,%M,%S')}")
            rec = None
        self.x += dx
        y = self.y
        if (get_from_level(self.x, self.y + 1) == " " or get_from_level(self.x, self.y + 1) == "@" or \
            get_from_level(self.x, self.y + 1) == "#") and not self.jmp:
            self.y += 1
        if self.jmp:
            self.y -= 1
            self.jy += 1
            if get_from_level(self.x, self.y) == "!" or get_from_level(self.x, self.y) == "?":
                self.jy = 0
                self.jmp = False
                self.x, self.y = check_point
            if self.jy >= 5 or get_from_level(self.x, self.y - 1) != " " and get_from_level(self.x, self.y - 1) != "#" \
                    or self.y - 1 < 0:
                self.jy = 0
                self.jmp = False
        if get_from_level(self.x, y) != 'h':
            if get_from_level(self.x, y + 1) == "?" or get_from_level(self.x, y + 1) == "!" \
                    or get_from_level(self.x, self.y) == "!":
                self.x, self.y = check_point
        if self.x < 0 and level.left is not None:
            level = level.left
        if self.x > cli.size[0] and level.right is not None:
            level = level.right
        if self.y < 0 and level.up is not None:
            level = level.up
        if self.y > cli.size[1] and level.down is not None:
            level = level.down

        cli.rect(self.x, self.y, 0, 0, 'p' if self.d else 'q', (255, 200, 100), (0, 0, 0))


player = Player(0, 0)
t = time.time()
while True:
    if time.time() - t >= 1 / 10:
        cli.clear()
        for j in range(h):
            for i in range(w):
                c = level.mapa[j * w + i]
                col = (255, 255, 255)
                if c == "?":
                    col = (255, 0, 0)
                if c == "!":
                    col = (255, 255, 0)
                if c == "@":
                    col = (0, 255, 0)
                if c == "#":
                    col = (0, 255, 0)
                if c == ".":
                    col = (0, 0, 255)
                if c != "p" and c != "h":
                    cli.rect(i, j, 0, 0, c, col, (0, 0, 0))
        player.update()
        cli.update()
        cli.draw()
        if cli.size[0] != w or cli.size[1] != h:
            os.system(f'mode con: cols={w} lines={h}')
        t = time.time()
