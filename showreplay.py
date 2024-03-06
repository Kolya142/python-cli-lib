import os
import time

import cli
import keyboard
cli.init()
t = time.time()
fps = float(input("fps: "))
w, h = map(int, input("size(w,h) in symbols: ").split())
replay = True
refile = input("file: ")
reobje = cli.PlayRecord(refile)

while True:

    if cli.size[0] != w or cli.size[1] != h:
        os.system(f'mode con: cols={w} lines={h}')
    if time.time()-t > 1/fps:
        t = time.time()
        if keyboard.is_pressed('l'):
            replay = True
            refile = cli.input_menu(30)
            reobje = cli.PlayRecord(refile)
        if replay:
            if reobje.frames:
                reobje.update()
            else:
                refile = None
                replay = False
        else:
            cli.clear()
    cli.update()
    cli.draw()
