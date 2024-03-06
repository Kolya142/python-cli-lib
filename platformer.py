import abc
import time

import keyboard
# from pynput.mouse import Listener

from vec import Vec2d, dist
import cli

cli.init()

gravity = 0.05
# mouse_events = []
#
#
# def on_click(x, y, button, pressed):
#     mouse_events.append((x, y, button, pressed))
#
#
# with Listener(on_click=on_click) as listener:
#     listener.join()


class Object(abc.ABC):
    def __init__(self, pos: Vec2d):
        self.pos = pos

    def step_to(self, pos: Vec2d, step_size: int):
        p = self.pos - pos
        p.norm()
        self.pos -= p * step_size

    def render(self):
        pass

    def update(self):
        pass


# class TestObject(Object):
#     def render(self):
#         pos = self.pos - camera_offset
#         pos.x, pos.y = int(pos.x), int(pos.y)
#         cli.rect(pos.x, pos.y, 0, 0, 'o', (255, 255, 255), (0, 0, 0))
#
#     def update(self):
#         self.step_to(Vec2d.from_list(cli.getRelativePos()), 1)


class Wall(Object):

    def render(self):
        global camera
        pos = self.pos - camera.pos
        cli.rect(int(pos.x), int(pos.y), 0, 0, '#', (155, 155, 155), (0, 0, 0))


class Camera(Object):
    def __init__(self):
        super().__init__(Vec2d(0, 0))  # Camera's current position
        self.motion_speed = 1  # Speed at which the camera moves
        self.motion_speed_minus = 1  # Adjusted speed when near screen edge
        self.target_object = None  # The object that the camera is following
        self.lerp_factor = 0.7  # Lerp factor controls the smoothness

    def update(self):
        if self.target_object:
            distance_to_target = dist(self.target_object.pos, self.pos)
            # print(distance_to_target)

            motion_threshold = self.motion_speed + (Vec2d.from_list(cli.size) / 2).mag()
            new_pos = self.target_object.pos - Vec2d.from_list(cli.size) / 2

            if distance_to_target >= motion_threshold and not self.is_target_on_screen_edge(self.target_object.pos):
                self.step_to(new_pos, self.motion_speed)
            elif self.is_target_on_screen_edge(self.target_object.pos):
                self.step_to(new_pos, self.motion_speed_minus)

            self.pos.x, self.pos.y = int(self.pos.x), int(self.pos.y)

    def step_to(self, target_pos: Vec2d, step_size: int):
        # Apply linear interpolation (lerping) towards the target position
        self.pos = self.pos + (target_pos - self.pos) * self.lerp_factor

    @staticmethod
    def is_target_on_screen_edge(target_pos: Vec2d) -> bool:
        screen_size = Vec2d.from_list(cli.size)
        margin = 4  # Pixels from the edge to be considered as on the edge
        on_left_edge = target_pos.x <= margin
        on_right_edge = target_pos.x >= screen_size.x - margin
        on_top_edge = target_pos.y <= margin
        on_bottom_edge = target_pos.y >= screen_size.y - margin
        return on_left_edge or on_right_edge or on_top_edge or on_bottom_edge


wall_poses = cli.Sprite.from_img(0, 0, 'platex').frame
walls = [Wall(Vec2d.from_list(pos)) for pos in wall_poses]


class Player(Object):
    def __init__(self, pos: Vec2d):
        super().__init__(pos)
        self.dir = Vec2d(0, 0)
        self.vel = Vec2d(0, 0)

    def render(self):
        pos = self.pos - camera.pos
        dire = self.pos - self.dir
        dire.norm()
        dire *= 1
        dire -= camera.pos
        dire += self.pos
        cli.rect(int(pos.x), int(pos.y), 0, 0, '@', (255, 255, 255), (0, 0, 0))
        cli.rect(int(dire.x), int(dire.y), 0, 0, 'o', (255, 0, 0), (0, 0, 0))

    def handle_collision(self):
        for wall in walls:
            if self.pos + self.vel == wall.pos:
                self.vel.x *= -0.1
                self.vel.y *= -0.1
                break
            # i = 0
            # # Check x-axis collision
            # if abs(self.pos.x + self.vel.x - wall.pos.x) <= 0.5:
            #     self.vel.x *= -0.1
            #     i = 1
            #
            # # Check y-axis collision
            # if abs(self.pos.y + self.vel.y - wall.pos.y) <= 0.5:
            #     self.vel.y *= -0.1
            #     i = 1
            #
            # if i:
            #     break

    def update(self):
        self.dir = Vec2d.from_list(cli.getRelativePos()) + camera.pos
        self.vel += Vec2d(0, gravity)
        p = self.pos - self.dir
        p.norm()
        p *= 1
        # e = None
        # if len(mouse_events) > 0:
        #     e = mouse_events.pop()
        for wall in walls:
            if wall.pos == self.pos + Vec2d(0, 1):
                if keyboard.is_pressed('space'):
                    self.vel += Vec2d(0, -5 / gravity)
                elif keyboard.is_pressed('a'):
                    self.vel += Vec2d(-1, 0)
                elif keyboard.is_pressed('d'):
                    self.vel += Vec2d(1, 0)
            else:
                if keyboard.is_pressed('a'):
                    self.vel += Vec2d(-0.01, 0)
                elif keyboard.is_pressed('d'):
                    self.vel += Vec2d(0.01, 0)
        vel = self.vel + p
        vel.norm()
        for wall in walls:
            if keyboard.is_pressed('q') and self.dir != self.pos \
                    and (wall.pos == self.pos + self.vel + p or wall.pos == self.pos + vel):
                o = self.pos + self.vel + p
                # cli.rect(int(o.x), int(o.y), 0, 0, '$', (255, 255, 0), (0, 0, 0))
                o = self.pos + vel
                # cli.rect(int(o.x), int(o.y), 0, 0, '$', (255, 255, 0), (0, 0, 0))
                self.vel -= p * 4
                break
        vel = self.vel
        vel.norm()
        self.handle_collision()

        self.pos += self.vel


obj = Player(Vec2d(3, 0))
camera = Camera()
camera.motion_speed = 5
camera.motion_speed_minus = 2
camera.target_object = obj

while True:
    time.sleep(1 / 50)
    cli.clear()
    for wall in walls:
        wall.render()
    n1 = False
    if keyboard.is_pressed('left'):
        n1 = True
        obj.pos.x -= 1
        obj.vel.x -= 1
    if keyboard.is_pressed('up'):
        n1 = True
        obj.pos.y -= 1
        obj.vel.y -= 1
    if keyboard.is_pressed('right'):
        n1 = True
        obj.pos.x += 1
        obj.vel.x += 1
    if keyboard.is_pressed('down'):
        n1 = True
        obj.pos.y += 1
        obj.vel.y += 1
    if not n1:
        obj.update()
    obj.render()
    if keyboard.is_pressed("r"):
        obj = Player(Vec2d(3, 0))
        camera.target_object = obj
    if 0:
        if keyboard.is_pressed("w"):
            camera_offset.y -= 0.2
        if keyboard.is_pressed("a"):
            camera_offset.x -= 0.2
        if keyboard.is_pressed("s"):
            camera_offset.y += 0.2
        if keyboard.is_pressed("d"):
            camera_offset.x += 0.2
    else:
        camera.update()
    cli.update()
    cli.draw()
