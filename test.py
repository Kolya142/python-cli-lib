import cli
import time
import vnoise
cli.init()
noise = vnoise.Noise()
cli.hide_cursor()
t = time.time() - 10
a = 0

while True:
    for y in range(cli.size[1]):
        for x in range(cli.size[0]):
            r = max(int(noise.noise3(x+a, y+a, 0.1, 1)*255), 0)
            g = max(int(noise.noise3(x+a, y+a, 0.2)*255), 0)
            b = max(int(noise.noise3(x+a, y+a, 0.3)*255), 0)

            cli.rect(x, y, 0, 0, '█', (r, g, b), (r, g, b))
    cli.blit_text(0, 0, f'fps: {1/(time.time()-t)}')
    t = time.time()
    a += 0.1
    cli.update()
    cli.draw()

