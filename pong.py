import random

import keyboard

import cli

playermode = 1
cli.init()
p1 = cli.size[1] // 2
p2 = cli.size[1] // 2
p = 10
b1 = 0
b2 = 0
ph = int(p//2)


class Ball:
    x: float = cli.size[0] // 2
    y: float = cli.size[1] // 2
    vx: float = 0.15
    vy: float = 0.15

    def update(self):
        if self.y <= 0 or self.y >= cli.size[1]-1:
            self.vy *= -1

        if self.x <= 0 or self.x >= cli.size[0]-1:
            if self.x < cli.size[0]//2:
                global b2
                b2 += 1
            else:
                global b1
                b1 += 1
            self.x = cli.size[0] // 2
            self.y = cli.size[1] // 2
            self.vx *= -1

        if 4 <= int(self.x) <= 5 and p1-ph <= self.y <= p1+ph:
            self.vx *= -1

        if cli.size[0]-6 <= int(self.x) <= cli.size[0]-5 and p2-ph <= self.y <= p2+ph:
            self.vx *= -1

        self.x += self.vx
        self.y += self.vy
        cli.rect(int(self.x), int(self.y), 1, 1, "*", (255, 255, 255), (0, 0, 0))


ball = Ball()


while True:
    cli.clear()
    ball.update()
    if playermode == 0:
        pos = cli.getRelativePos()
        if pos[0] >= 0 and pos[1] >= 0:
            p1 = pos[1]
        if p2 > ball.y:
            # 0.11 - 0.05
            p2 -= 0.09
        if p2 < ball.y:
            p2 += 0.09
    elif playermode == 2:
        if p1 > ball.y:
            p1 -= 0.09
        if p1 < ball.y:
            p1 += 0.11
        if p2 > ball.y:
            p2 -= 0.08
        if p2 < ball.y:
            p2 += 0.07
    elif playermode == 1:
        if keyboard.is_pressed("w") and p1 > ph:
            p1 -= 0.1
        if keyboard.is_pressed("s") and p1 < cli.size[1]-ph:
            p1 += 0.1
        if keyboard.is_pressed("up") and p2 > ph:
            p2 -= 0.1
        if keyboard.is_pressed("down") and p2 < cli.size[1]-ph:
            p2 += 0.1
    cli.rect(3, int(p1-ph), 1, p-1, "@", (255, 255, 0), (0, 0, 0))
    cli.rect(cli.size[0]-5, int(p2-ph), 1, p-1, "@", (255, 255, 0), (0, 0, 0))
    cli.blit_text(int(cli.size[0]//2.5-2), 0, str(b1))
    cli.blit_text(cli.size[0]//6+cli.size[0]//2-2, 0, str(b2))
    cli.update()
    cli.draw()
