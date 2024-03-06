import os
import time
import pickle
import keyboard
import cli

cli.init()
cli.hide_cursor()
drawed = {}  # x, y: r, g, b
current_color = (255, 255, 255)
t = time.time() - 10
rec = cli.Record()
key_pressed = None


def save():
    fn = cli.input_menu()
    if fn:
        rec.write(fn)


lt = 0
pos = (-1, -1)
ttq = time.time()

while True:

    # if pos != (-1, -1):
    #    cli.set_char(pos[0], pos[1], ' ')

    pos = cli.getRelativePos()
    cli.clear()
    for i in drawed:
        cli.set_char(i[0], i[1], "█")
        cli.set_color_fg(i[0], i[1], drawed[i][0], drawed[i][1], drawed[i][2])
        cli.set_color_bg(i[0], i[1], drawed[i][0], drawed[i][1], drawed[i][2])
    if keyboard.is_pressed("tab") and time.time()-ttq > 0.25:
        rec.update()
        ttq = time.time()
    cli.blit_text(0, 0, f'cursor-pos: {pos}  ', text_color=(255, 255, 255))
    cli.blit_text(30, 0, f'keys: space-draw,q-select color,esc-clear,r-remove,s-save,tab-add', text_color=(255, 255, 0))
    cli.blit_text(0, 1, f'drawed-count: {len(drawed)}', text_color=(255, 255, 255))
    # cli.rect(0, 3, 30, 0, ' ', (0, 0, 0), (0, 0, 0))
    cli.blit_text(0, 3, f'current_color: {current_color}', back_color=current_color, text_color=(200, 200, 100))
    cli.blit_text(0, 8, str(lt))
    fps_text = f'fps: {round(1 / (time.time() - t), 2)}'
    t = time.time()
    cli.blit_text(cli.size[0] - 11, 0, fps_text)
    cli.set_color_bg(0, 2, 0, 0, 0)
    cli.set_color_bg(1, 2, 20, 20, 20)
    cli.set_color_bg(2, 2, 50, 50, 50)
    cli.set_color_bg(3, 2, 100, 100, 100)
    cli.set_color_bg(4, 2, 255, 255, 255)
    cli.set_color_bg(5, 2, 255, 0, 0)
    cli.set_color_bg(6, 2, 255, 255, 0)
    cli.set_color_bg(7, 2, 0, 255, 0)
    cli.set_color_bg(8, 2, 0, 255, 255)
    cli.set_color_bg(9, 2, 0, 0, 255)
    cli.set_color_bg(10, 2, 255, 0, 255)
    if os.name == 'nt':
        if keyboard.is_pressed('esc'):
            cli.clear()
            drawed = {}
        if keyboard.is_pressed('s'):
            save()

        if pos != (-1, -1):
            cli.set_char(pos[0], pos[1], '*')
            cli.set_color_fg(pos[0], pos[1], current_color[0], current_color[1], current_color[2])
            if keyboard.is_pressed('q') and cli.is_valid_pos(pos[0], pos[1]):
                current_color = cli.screen_color_bg[pos[1]][pos[0]]
            if (current_color == (0, 0, 0) and keyboard.is_pressed('space')) or keyboard.is_pressed('r'):
                if (pos[0], pos[1]) in drawed:
                    drawed.pop((pos[0], pos[1]))
            if keyboard.is_pressed('space') and current_color != (0, 0, 0):
                drawed[(pos[0], pos[1])] = (current_color[0], current_color[1], current_color[2])
            if not keyboard.is_pressed('space') and not keyboard.is_pressed('q'):
                if cli.is_valid_pos(pos[0], pos[1]):
                    color = cli.screen_color_bg[pos[1]][pos[0]]
                    cli.set_color_fg(pos[0], pos[1], 255 - color[0], 255 - color[1], 255 - color[2])
    cli.update()
    lt = cli.draw(True)
