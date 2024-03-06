from random import random, randint, choice
from typing import List, Tuple
from collections import deque
import pickle
import time

import keyboard

import cli

cli.init()
world: List['Entity'] = []
tree: dict = pickle.load(open("xtre", 'rb'))
tree: List[Tuple[int, int]] = list(tree.keys())
# gravity = 0.001
# frames = 500
# ricochet_force = -1
# air_stop = 0.999

gravity = 0.0005
frames = 10000
autostat = False
ricochet_force = -1.001
movement_speed = 0.2
air_stop = 1


class Entity:
    x: float
    y: float
    vx: float
    vy: float
    ovx: float | None = None
    ovy: float | None = None
    c: str
    col: object
    static: bool
    ricochet: bool
    target_x: float | None = None
    target_y: float | None = None

    def __init__(self, x, y, c, col, *, is_static: bool = False, ricochet: bool = False, vx: float = 0, vy: float = 0):
        self.x = x
        self.y = y
        self.c = c
        self.col = col
        self.vx = vx
        self.vy = vy
        self.static = is_static
        self.ricochet = ricochet

    def update(self):
        if self.target_x is not None and self.target_y is not None:
            # Calculate the direction towards the target
            direction_x = self.target_x - self.x
            direction_y = self.target_y - self.y
            while True:
                p = False
                for enter in ents:
                    if int(self.x + direction_x * movement_speed) == int(enter.x) \
                            and int(self.y + direction_y * movement_speed) == int(enter.y):
                        if abs(self.vx) < abs(self.vy):
                            direction_x += 0.5 if self.target_x > self.x else -0.2
                        else:
                            direction_y += 0.5 if self.target_y > self.y else -0.2
                        p = True

                if not p:
                    break
            self.vx = direction_x * movement_speed
            self.vy = direction_y * movement_speed

            # Check if close to target and stop
            if int(self.target_x) == int(self.x) and int(self.y) == int(self.target_y):
                self.vx = self.ovx
                self.vy = self.ovy
                self.ovx = None
                self.ovy = None
                if autostat:
                    self.static = True
                self.x = self.target_x
                self.y = self.target_y
                # self.ricochet = True
                self.target_x = None
                self.target_y = None

        if not self.static:
            x = self.x
            y = self.y
            self.x += self.vx
            self.y += self.vy
            for obj in world:
                if obj is self:
                    continue
                if int(self.x) == int(obj.x) and int(self.y) == int(obj.y):
                    if abs(self.vx) > abs(self.vy):
                        self.x = x
                        if obj.ricochet:
                            self.vx *= ricochet_force
                        else:
                            self.vx *= .3
                    else:
                        self.y = y
                        if obj.ricochet:
                            self.vy *= ricochet_force
                        else:
                            self.vy *= .3
            self.vy *= air_stop
            self.vx *= air_stop
            self.vy += gravity
            if self.x < 0:
                self.x = cli.size[0] - self.x
            if self.y < 0:
                self.y = cli.size[1] - self.y
            if self.x > cli.size[0] + 1:
                self.x = self.x - cli.size[0]
            if self.y > cli.size[1] + 1:
                self.y = self.y - cli.size[1]

        cli.rect(int(self.x), int(self.y), 0, 0, self.c, self.col, (0, 0, 0))

    def move_to(self, x: float, y: float):
        self.target_x = x
        self.target_y = y
        # self.ricochet = False
        self.ovx = self.vx
        self.ovy = self.vy
        # self.x = x
        # self.y = y
        # self.vx *= 0.3
        # self.vy *= 0.3


ents = []
entst = dict()
record = False
rec = None
record_file = ""
play = False
# print(len(tree))
# input()
for _ in range(200):
    world.append(
        Entity(randint(0, cli.size[0]), randint(0, cli.size[1]), '&',
               [randint(0, 255), randint(0, 255), randint(0, 255)], vx=randint(-15, 15) / 5,
               vy=randint(-5, 5) / 5, ricochet=True))
    ents.append(world[-1])
ents2 = ents.copy()
for val in tree:
    for key in ents2:
        entst[key] = val
        ents2.remove(key)
        break
del ents2
binds = {}
# for i in tree:
#     world.append(Entity(i[0], i[1], '&', (255, 0, 255), ricochet=True))
# print(entst)
# input()
for i in range(cli.size[0]):
    world.append(Entity(i, cli.size[1] - 1, '*', [255, int(i / cli.size[0] * 255), 0], is_static=True, ricochet=True))
    world.append(Entity(i, 0, '*', [255, 255-int(i / cli.size[0] * 255), 0], is_static=True, ricochet=True))
for i in range(cli.size[1]):
    world.append(Entity(cli.size[0] - 1, i, '*', [255, int(i / cli.size[1] * 255), 0], is_static=True, ricochet=True))
    world.append(Entity(0, i, '*', [255, 255-int(i / cli.size[1] * 255), 0], is_static=True, ricochet=True))
t = time.time()


def build_xmas_tree():
    for p in entst:
        p.move_to(entst[p][0], entst[p][1])
        # p.ricochet = False


def build_from_file(fn: str):
    ens = list(pickle.load(open(fn, 'rb')).keys())
    for i in range(len(ens)):
        ents[i].move_to(ens[i][0], ens[i][1])
        # p.ricochet = False


def find_path(starts, goals, entities):
    def is_blocked(node):
        return any(node == (int(entity.x), int(entity.y)) for entity in entities)

    def get_neighbors(node):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4-directional movement
        return [(node[0] + dx, node[1] + dy) for dx, dy in directions if not is_blocked((node[0] + dx, node[1] + dy))]

    visited = set()
    start = (int(starts[0]), int(starts[1]))
    goal = (int(goals[0]), int(goals[1]))
    queue = deque([(start, [start])])  # Queue of (position, path)

    while queue:
        current_position, path = queue.popleft()
        if current_position == goal:
            return path  # Goal reached

        for neighbor in get_neighbors(current_position):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None  # No path found


def command_exec(cmd):
    global record, record_file, rec, play
    for command in cmd.split(';'):
        if len(command.split()) >= 2 and command.split()[0] in ("frames", "grav",
                                                                "air", "rich", "bind",
                                                                "build", "movspeed", "record", "play"):
            var = command.split()[0]
            match var:
                case "frames":
                    global frames
                    frames = float(command.split()[1])
                case "grav":
                    global gravity
                    gravity = float(command.split()[1])
                case "air":
                    global air_stop
                    air_stop = float(command.split()[1])
                case "rich":
                    global ricochet_force
                    ricochet_force = float(command.split()[1])
                case "build":
                    build_from_file(command.split()[1])
                case "movspeed":
                    global movement_speed
                    movement_speed = float(command.split()[1])
                case "record":
                    record = True
                    record_file = command.split()[1]
                    rec = cli.Record()
                case "play":
                    play = True
                    rec = cli.PlayRecord(command.split()[1])
                case "bind":
                    if len(command.split()) == 3:
                        # print(command)
                        binds[command.split()[1]] = command.split()[2]
                        # print(binds)
                        # input()
                    if len(command.split()) == 4:
                        # print(command)
                        binds[command.split()[1]] = command.split()[2] + ' ' + command.split()[3]
                        # print(binds)
                        # input()
        if len(command.split()) == 1 and command.split()[0] in ("elo", "rand", "nom", "richd", "riche", "unfr", "stop"
                                                                "autostatd", "autostate"):
            var = command.split()[0]
            global autostat
            match var:
                case "elo":
                    build_xmas_tree()
                case "rand":
                    for enter in ents:
                        enter.x, enter.y = randint(0, cli.size[0]), randint(0, cli.size[1])
                        enter.vx, enter.vy = randint(-15, 15) / 5, randint(-5, 5) / 5
                        enter.target_x = None
                        enter.target_y = None
                case "nom":
                    for enter in ents:
                        enter.x, enter.y = randint(0, cli.size[0]), cli.size[1] - 2
                        enter.vx, enter.vy = 0, 0
                        enter.target_x = None
                        enter.target_y = None
                case "richd":
                    for enter in ents:
                        enter.ricochet = False
                case "riche":
                    for enter in ents:
                        enter.ricochet = True
                case "unfr":
                    for enter in ents:
                        enter.static = False
                case "autostatd":
                    autostat = False
                case "autostate":
                    autostat = True
                case "stop":
                    record = False
                    rec.write(record_file)
                    record_file = ""


auto_exec = ["bind e elo", "bind r rand", "bind n nom", "bind u unfr", "bind o movspeed 0.5", "bind p movspeed 0.2",
             "bind a autostate", "bind w autostatd", "bind s stop", "bind j frames 10", "bind k frames 600",
             "bind 1 build t1", "bind 2 build t2", "bind 3 build t3", "bind 4 elo", "bind 5 build t5"]
for cmd in auto_exec:
    command_exec(cmd)

while True:
    pos = cli.getRelativePos()
    if time.time() - t >= 1 / frames:

        cli.clear()
        for ent in world:
            # cli.blit_text(int(ent.x), int(ent.y-1), f'{round(ent.x)},{round(ent.y)}')
            ent.update()
            t = time.time()
        if pos != (-1, -1) and keyboard.is_pressed("space"):
            ent = choice(ents)
            ent.move_to(pos[0], pos[1])
        if record and isinstance(rec, cli.Record):
            rec.update()
        if play and isinstance(rec, cli.PlayRecord):
            if not rec.frames:
                play = False
                rec = None
            else:
                rec.update()
        if pos != (-1, -1) and keyboard.is_pressed("q"):
            e = ents[0]
            p = find_path(pos, [e.x, e.y], ents)
            for i in p:
                cli.rect(i[0], i[1], 0, 0, '*', (255, 0, 255), (0, 255, 0))
    if keyboard.is_pressed('tab'):
        com = cli.input_menu()
        command_exec(com)
    for key in binds:
        if keyboard.is_pressed(key):
            command_exec(binds[key])

    cli.update()
    cli.draw()
