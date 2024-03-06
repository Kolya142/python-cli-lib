import cli
import datetime
cli.init()
cli.hide_cursor()
skeleton_color = (50, 50, 50)
symbol_color = (255, 255, 255)


def draw_skeleton(x, y):
    cli.rect(x+1, y, 3, 0, "░", skeleton_color, (0, 0, 0))
    cli.rect(x, y+1, 0, 1, "░", skeleton_color, (0, 0, 0))
    cli.rect(x+5, y+1, 0, 1, "░", skeleton_color,  (0, 0, 0))
    cli.rect(x, y+4, 0, 1, "░", skeleton_color,  (0, 0, 0))
    cli.rect(x+5, y+4, 0, 1, "░", skeleton_color,  (0, 0, 0))
    cli.rect(x+1, y+3, 3, 0, "░", skeleton_color,  (0, 0, 0))
    cli.rect(x+1, y+6, 3, 0, "░", skeleton_color,  (0, 0, 0))


def draw_base(x, y, e1, e2, e3, e4, e5, e6, e7):
    if e1:
        cli.rect(x + 1, y, 3, 0, "█", symbol_color, symbol_color)
    if e2:
        cli.rect(x, y + 1, 0, 1, "█", symbol_color, symbol_color)
    if e3:
        cli.rect(x + 5, y + 1, 0, 1, "█", symbol_color, symbol_color)
    if e4:
        cli.rect(x, y + 4, 0, 1, "█", symbol_color, symbol_color)
    if e5:
        cli.rect(x + 5, y + 4, 0, 1, "█", symbol_color, symbol_color)
    if e6:
        cli.rect(x + 1, y + 3, 3, 0, "█", symbol_color, symbol_color)
    if e7:
        cli.rect(x + 1, y + 6, 3, 0, "█", symbol_color, symbol_color)


def draw_0(x, y):
    draw_skeleton(x, y)
    draw_base(x, y, 1, 1, 1, 1, 1, 0, 1)


def draw_1(x, y):
    draw_skeleton(x, y)
    draw_base(x, y, 0, 0, 1, 0, 1, 0, 0)


def draw_2(x, y):
    draw_skeleton(x, y)
    draw_base(x, y, 1, 0, 1, 1, 0, 1, 1)


def draw_3(x, y):
    draw_skeleton(x, y)
    draw_base(x, y, 1, 0, 1, 0, 1, 1, 1)


def draw_4(x, y):
    draw_skeleton(x, y)
    draw_base(x, y, 0, 1, 1, 0, 1, 1, 0)


def draw_5(x, y):
    draw_skeleton(x, y)
    draw_base(x, y, 1, 1, 0, 0, 1, 1, 1)


def draw_6(x, y):
    draw_skeleton(x, y)
    draw_base(x, y, 1, 1, 0, 1, 1, 1, 1)


def draw_7(x, y):
    draw_skeleton(x, y)
    draw_base(x, y, 1, 0, 1, 0, 1, 0, 0)


def draw_8(x, y):
    draw_skeleton(x, y)
    draw_base(x, y, 1, 1, 1, 1, 1, 1, 1)


def draw_9(x, y):
    draw_skeleton(x, y)
    draw_base(x, y, 1, 1, 1, 0, 1, 1, 1)


def draw_digit(x, y, d):
    match d:
        case 0:
            draw_0(x, y)
        case 1:
            draw_1(x, y)
        case 2:
            draw_2(x, y)
        case 3:
            draw_3(x, y)
        case 4:
            draw_4(x, y)
        case 5:
            draw_5(x, y)
        case 6:
            draw_6(x, y)
        case 7:
            draw_7(x, y)
        case 8:
            draw_8(x, y)
        case 9:
            draw_9(x, y)


while True:
    time = datetime.datetime.now().time()
    h = time.hour
    m = time.minute
    s = time.second
    # cli.blit_text(0, 0, f'{time.hour}:{time.minute},{time.second}         ', (0, 255, 0))
    h1 = time.hour // 10
    h2 = time.hour % 10
    m1 = time.minute // 10
    m2 = time.minute % 10
    s1 = time.second // 10
    s2 = time.second % 10
    draw_digit(5-4, 5-4, h1)
    draw_digit(20-4, 5-4, h2)
    cli.rect(30-4, 6-4, 0, 0, '█', symbol_color, symbol_color)
    cli.rect(30-4, 10-4, 0, 0, '█', symbol_color, symbol_color)
    draw_digit(35-4, 5-4, m1)
    draw_digit(50-4, 5-4, m2)
    cli.rect(60-4, 11-4, 0, 0, '█', symbol_color, symbol_color)
    draw_digit(65-4, 5-4, s1)
    draw_digit(80-4, 5-4, s2)

    cli.update()
    cli.draw(False)
