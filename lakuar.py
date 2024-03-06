import datetime
import os
import time

import keyboard

import cli

cli.init()
w, h = 30, 15
levels = []
console_system = cli.CmdSystem()
with open('lakuar/cfg/levels') as f:
    for m in f.read().split('\n'):
        with open('lakuar/maps/' + m, encoding='utf-8') as fm:
            mf = ''
            exec(fm.read())
            levels.append(mf)
lev = 0
level = levels[lev]
check_point = (0, 0)
rec = None


def get_from_level(x, y):
    if x + y * w > len(level) or x + y * w < 0:
        return
    return level[x + y * w]


def set_level(x, y, char):
    global level
    if x + y * w > len(level) or x + y * w < 0:
        return
    l1 = list(level)
    l1[x + y * w] = char
    level = ''.join(l1)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.jmp = False
        self.jy = 0
        self.d = True

    def update(self):
        global check_point, rec

        if self.y == cli.size[1]-1:
            self.x, self.y = check_point
        dx = 0
        if keyboard.is_pressed("y"):
            pos = cli.getRelativePos()
            self.x, self.y = pos
        if keyboard.is_pressed("e") or get_from_level(self.x, self.y) == 'c':
            if get_from_level(self.x, self.y) == 'c':
                set_level(self.x, self.y, 'C')
            check_point = self.x, self.y
            global ct
            ct = time.time()
        if keyboard.is_pressed("a"):
            self.d = False
            if get_from_level(self.x - 1, self.y) in ("@", "h", "C", 'c'):
                dx = -1
            elif get_from_level(self.x - 1, self.y) == " " or get_from_level(self.x - 1, self.y - 1) == " ":
                dx = -1
                if get_from_level(self.x - 1, self.y - 1) == " " and get_from_level(self.x - 1, self.y) != " ":
                    self.y -= 1
        if keyboard.is_pressed("d"):
            self.d = True
            if get_from_level(self.x + 1, self.y) in ("@", "h", 'C', 'c'):
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
        if (get_from_level(self.x, self.y + 1) in (' ', '#', '@', 'h', 'c', 'C')) and not self.jmp:
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
                    or get_from_level(self.x, self.y) == "!" or \
                    self.y < 0 or self.x < 0 or self.y > cli.size[1] or self.x > cli.size[0]:
                self.x, self.y = check_point
        if get_from_level(self.x, self.y) == "@":
            global lev, level
            lev += 1
            lev = lev % len(levels)
            level = levels[lev]
            check_point = (0, 0)
            self.x, self.y = check_point

        cli.rect(self.x, self.y, 0, 0, 'p' if self.d else 'q', (255, 200, 100), (0, 0, 0))


player = Player(0, 0)
t = time.time()
ct = 0
while True:
    if time.time() - t >= 1 / 10:
        cli.clear()
        for j in range(h):
            for i in range(w):
                c = level[j * w + i]
                if c == ' ':
                    continue
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
                if c != "p" and c != "h" and c != 'c':
                    cli.rect(i, j, 0, 0, c, col, (0, 0, 0))
        player.update()
        if time.time() - ct <= 2:
            # cli.rect(0, 0, 10, 10, '#', (0, 0, 0), (0, 0, 255))
            cli.blit_text(0, 0, "saved...")
        cli.update()
        cli.draw()
        if cli.size[0] != w or cli.size[1] != h:
            os.system(f'mode con: cols={w} lines={h}')
        t = time.time()
