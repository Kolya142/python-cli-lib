import dataclasses
import os
import pickle
import time
from typing import List, Callable, Dict, Tuple

from vec import Vec3d

if os.name == 'nt':
    import keyboard
    import win32api
    import win32console
    import win32gui
    window_border_x = 0
    window_border_y = 30


    def getRelativePos():
        pt = win32api.GetCursorPos()  # get current cursor pos
        hwnd1 = win32console.GetConsoleWindow()  # get console window handle
        hwnd2 = win32gui.WindowFromPoint(pt)  # get screen coordinate rect of the console window
        rect1 = win32gui.GetWindowRect(hwnd1)
        cw, ch = 8, 16
        if rect1:
            x, y, w, h = rect1
            w -= x+window_border_x
            h -= y+window_border_y
            w1, h1 = os.get_terminal_size()
            cw = int(w/w1)
            ch = int(h/h1)

        if hwnd1 == hwnd2:
            pos = win32gui.ScreenToClient(hwnd1, pt)  # convert screen coordinate to client coordinate of hwnd.
            return pos[0] // cw, pos[1] // ch
        else:
            return -1, -1


    def getCharSize():
        hwnd1 = win32console.GetConsoleWindow()  # get console window handle
        rect1 = win32gui.GetWindowRect(hwnd1)
        if rect1:
            x, y, w, h = rect1
            w -= x+window_border_x
            h -= y+window_border_y
            w1, h1 = os.get_terminal_size()
            cw = int(w/w1)
            ch = int(h/h1)
            return cw, ch
        return -1, -1

else:
    import click
    from Xlib import display, X
    from ewmh import EWMH


    def getRelativePos():
        raise OSError("unix unsupported, if need you can fix support")
        d = display.Display().screen().root
        data = d.query_pointer()._data  # get current cursor position
        ewmh = EWMH()

        # Get the active window
        active_window = ewmh.getActiveWindow()

        if active_window is not None:
            # Get window geometry (x, y, width, height)
            win_geom = active_window.get_geometry()._data

            # Calculate relative position
            rel_x = data["root_x"] - win_geom['x']
            rel_y = data["root_y"] - win_geom['y']

            return rel_x, rel_y

        return -1, -1

size = os.get_terminal_size()
is_init = False
screen_color_fg = []
screen_color_bg = []
screen = []
symbol_size = (11, 24)
cursor_state = True
# printf(b'lines: %d, columns: %d\n', size.lines, size.columns)


def init():
    global is_init, size, screen, screen_color_fg, screen_color_bg
    if is_init:
        raise Exception("cli is inited")
    is_init = True
    os.system('')
    size = os.get_terminal_size()
    screen = [[' ' for _ in range(size.columns)] for _ in range(size.lines)]
    screen_color_fg = [[(255, 255, 255) for _ in range(size.columns)] for _ in range(size.lines)]
    screen_color_bg = [[(0, 0, 0) for _ in range(size.columns)] for _ in range(size.lines)]


def update():
    global size, screen, screen_color_fg, screen_color_bg
    s = size
    size = os.get_terminal_size()
    if s != size:
        clear()
        if not cursor_state:
            hide_cursor()


def is_valid_pos(x, y):
    if x < 0 or x >= size.columns or y < 0 or y >= size.lines:
        return False
    return True


def set_color_fg(x, y, r, g, b):
    if x < 0 or x >= size.columns or y < 0 or y >= size.lines:
        return
    screen_color_fg[y][x] = (r, g, b)


@dataclasses.dataclass
class Image:
    image: list
    color_fg: list
    color_bg: list

    def make_vec3(self):
        for row in self.color_fg:
            for index, color in enumerate(row):
                row[index] = Vec3d.from_list(color)
        for row in self.color_bg:
            for index, color in enumerate(row):
                row[index] = Vec3d.from_list(color)


def grab_image():
    img = Image(screen, screen_color_fg, screen_color_bg)
    img.make_vec3()
    return img


def rect(x, y, w, h, c, fg, bg):
    for i in range(x, x+w+1):
        for j in range(y, y+h+1):
            set_color_bg(i, j, bg[0], bg[1], bg[2])
            set_color_fg(i, j, fg[0], fg[1], fg[2])
            set_char(i, j, c)


def set_color_bg(x, y, r, g, b):
    if x < 0 or x >= size.columns or y < 0 or y >= size.lines:
        return
    screen_color_bg[y][x] = (r, g, b)


def set_char(x, y, c):
    if x < 0 or x >= size.columns or y < 0 or y >= size.lines:
        return
    screen[y][x] = c


def blit_text(x, y, text, text_color=(255, 255, 255), back_color=None, is_vertical=False):
    if not is_vertical:
        for i in range(x, x+len(text)):
            if back_color:
                set_color_bg(i, y, *back_color)
            set_color_fg(i, y, *text_color)
            set_char(i, y, text[i-x])
    else:
        for j in range(y, y+len(text)):
            if back_color:
                set_color_bg(x, j, *back_color)
            set_color_fg(x, j, *text_color)
            set_char(x, j, text[j-y])


def hide_cursor():
    global cursor_state
    cursor_state = False
    print('\x1b[?25l', end='')


def show_cursor():
    global cursor_state
    cursor_state = True
    print('\x1b[?25h', end='')


def clear():
    global screen, screen_color_fg, screen_color_bg
    screen = [[' ' for _ in range(size.columns)] for _ in range(size.lines)]
    screen_color_fg = [[(255, 255, 255) for _ in range(size.columns)] for _ in range(size.lines)]
    screen_color_bg = [[(0, 0, 0) for _ in range(size.columns)] for _ in range(size.lines)]


def input_menu(width=40):
    text = ""
    hwidth = width // 2
    sav = False
    t = 0
    while True:
        for x in range(size[0] // 2 - hwidth - 1, size[0] // 2 + hwidth + 2):
            for y in range(size[1] // 2 - 1, size[1] // 2 + 2):
                set_color_bg(x, y, 100, 100, 100)

        for x in range(size[0] // 2 - hwidth, size[0] // 2 + hwidth + 1):
            for y in range(size[1] // 2, size[1] // 2 + 1):
                set_color_bg(x, y, 50, 50, 50)
                set_char(x, y, ' ')
        if os.name == 'nt':
            key = keyboard.read_key()
        else:
            key = click.getchar()
        if time.time()-t > 0.15:
            match key:
                case 'backspace':
                    if len(text) >= 1:
                        text = text[:len(text) - 1]
                case "space":
                    text += " "
                case 'enter':
                    sav = True
                    break
                case 'esc':
                    break
                case 'left':
                    pass
                case 'right':
                    pass
                case _:
                    text += key
            if key:
                t = time.time()
        blit_text(size[0] // 2 - hwidth, size[1] // 2, text)
        update()
        draw()
    if sav:
        return text


opt_level = 20
lwq = lambda x, y: abs(x[0]-y[0]) < opt_level and abs(x[1]-y[1]) < opt_level and abs(x[2]-y[2]) < opt_level


class Record:
    def __init__(self):
        self.frames = []

    def update(self):
        self.frames.append((screen, screen_color_fg, screen_color_bg))

    def write(self, fn: str):
        with open(fn, 'wb') as f:
            pickle.dump(self.frames, f)


Cmd_ft = Callable[['CmdCommand', str], None]


@dataclasses.dataclass
class CmdCommand:
    CmdName: str
    CmdFunction: Cmd_ft
    CmdDescription: str
    CurrCmdSystem: 'CmdSystem'


# Command_f(OCommand: CmdCommand, CmdString: str)


def CmdHelp_f(OCommand: CmdCommand, CmdString: str):
    h = ""
    for cmd in OCommand.CurrCmdSystem.commands:
        h += f'{cmd.CmdName}: {cmd.CmdDescription}\n'
    print('', end="\x1b[H", flush=True)
    print(h)
    input("press enter to continue:")


class CmdSystem:
    def __init__(self):
        self.commands: List[CmdCommand] = []
        self.AddCommand("help", CmdHelp_f, "help command")

    def ExecCommand(self, command: str):
        args = command.split()
        for cmd in self.commands:
            if cmd.CmdName == args[0]:
                cmd.CmdFunction(cmd, command)
                break

    def AddCommand(self, name: str, function, description: str):
        command = CmdCommand(name, function, description, self)
        self.commands.append(command)


class PlayRecord:
    def __init__(self, fn: str):
        self.frames = pickle.load(open(fn, 'rb'))[::-1]

    def update(self):
        global screen, screen_color_fg, screen_color_bg
        screen, screen_color_fg, screen_color_bg = self.frames.pop()


class Sprite:
    def __init__(self, x, y, frame: Dict[Tuple[int, int], Tuple[Tuple[int, int, int], Tuple[int, int, int], str]]):
        """
        :param x: x
        :param y: y
        :param frame: {(x, y): ((r, g, b), (r, g, b), char)}
        """
        self.frame = frame
        self.width = 0
        self.height = 0
        for p in self.frame:
            if p[0]-x > self.width:
                self.width = p[0]-x
            if p[1]-y > self.height:
                self.height = p[1]-y
        self.x = x
        self.y = y

    def update(self, x_, y_):
        for p in self.frame:
            x, y = p
            x = x - self.x + x_
            y = y - self.y + y_
            bg, fg, c = self.frame[p]
            set_color_bg(x, y, bg[0], bg[1], bg[2])
            set_color_fg(x, y, fg[0], fg[1], fg[2])
            set_char(x, y, c)

    @classmethod
    def from_img(cls, x, y, fn: str):
        with open(fn, 'rb') as f:
            o = pickle.load(f)
            if isinstance(o, tuple):
                o = o[0]
            d = {}
            for i in o:
                d[i] = ((0, 0, 0), o[i], '█')
            return cls(x, y, d)


def draw(colored: bool = True):
    global printes
    print('\x1b[H', end='')
    last_bg = (0, 0, 0)
    last_fg = (0, 0, 0)
    t = ""
    for y in range(size.lines):
        line = ""
        for x in range(size.columns):
            bg_col = screen_color_bg[y][x]
            fg_col = screen_color_fg[y][x]
            bg = f'\x1b[48;2;{bg_col[0]};{bg_col[1]};{bg_col[2]}m'
            fg = f'\x1b[38;2;{fg_col[0]};{fg_col[1]};{fg_col[2]}m'
            if colored:
                if bg_col == (0, 0, 0):
                    bg = "\x1b[0m"
                if fg_col == (0, 0, 0):
                    fg = "\x1b[0m"
                if not lwq(last_bg, bg_col) or not lwq(last_fg, fg_col):
                    line += bg + fg + screen[y][x]
                    last_fg = fg_col
                    last_bg = bg_col
                else:
                    line += screen[y][x]
            else:
                line += screen[y][x]

        t += line
        # print(line.encode())
        # printf(line.encode())
    print(t, end="\x1b[H", flush=True)
    return len(t)
