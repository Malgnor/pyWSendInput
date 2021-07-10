from ctypes import byref, sizeof, wintypes
from time import sleep

from PyWSendInput._user32 import (GETCURSORPOS, GETSYSTEMMETRICS, INPUT, INPUT_MOUSE,
                                  MOUSEINPUT, SENDINPUT, SETCURSORPOS)

XBUTTON1 = 0x0001
XBUTTON2 = 0x0002

MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_HWHEEL = 0x01000
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_MOVE_NOCOALESCE = 0x2000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_VIRTUALDESK = 0x4000
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100

MOUSE_ABSOLUTE_MAX = 65535  # 0xFFFF


def mouse_event(flags):
    mouse_inputs = (INPUT * len(flags))()
    for i, flag in enumerate(flags):
        mouse_inputs[i] = INPUT(INPUT_MOUSE, mi=MOUSEINPUT(dwFlags=flag))

    return SENDINPUT(len(flags), mouse_inputs, sizeof(INPUT))


def mouse_move(input_x, input_y, absolute=False):
    mouse_input = INPUT(INPUT_MOUSE, mi=MOUSEINPUT(
        input_x, input_y, dwFlags=MOUSEEVENTF_MOVE + (MOUSEEVENTF_ABSOLUTE if absolute else 0)))

    return SENDINPUT(1, byref(mouse_input), sizeof(INPUT))


def mouse_wheel_move(movement, horizontal=False):
    mouse_input = INPUT(INPUT_MOUSE, mi=MOUSEINPUT(
        mouseData=movement, dwFlags=MOUSEEVENTF_HWHEEL if horizontal else MOUSEEVENTF_WHEEL))

    return SENDINPUT(1, byref(mouse_input), sizeof(INPUT))


def mouse_left_click(repeats=1, delay=0):
    count = 0
    for _ in range(0, repeats):
        count += mouse_event([MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP])
        sleep(delay)

    return count


def mouse_right_click(repeats=1, delay=0):
    count = 0
    for _ in range(0, repeats):
        count += mouse_event([MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP])
        sleep(delay)

    return count


def mouse_middle_click(repeats=1, delay=0):
    count = 0
    for _ in range(0, repeats):
        count += mouse_event([MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP])
        sleep(delay)

    return count


def get_cursor_position():
    point = wintypes.POINT()
    GETCURSORPOS(byref(point))
    return (point.x, point.y)


def get_screen_size():
    return (GETSYSTEMMETRICS(0), GETSYSTEMMETRICS(1))

def set_cursor_pos(x, y):
    return SETCURSORPOS(x, y)
