from ctypes import byref, sizeof
from time import sleep
from PyWSendInput import SENDINPUT, INPUT, INPUT_MOUSE, MOUSEINPUT

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


def __mouse_click(flag):
    mouse_input = INPUT(INPUT_MOUSE, mi=MOUSEINPUT(
        dwFlags=flag))
    SENDINPUT(1, byref(mouse_input), sizeof(INPUT))


def mouse_move(input_x, input_y, absolute=False):
    mouse_input = INPUT(INPUT_MOUSE, mi=MOUSEINPUT(
        input_x, input_y, dwFlags=MOUSEEVENTF_MOVE + (MOUSEEVENTF_ABSOLUTE if absolute else 0x0)))
    SENDINPUT(1, byref(mouse_input), sizeof(INPUT))


def mouse_wheel_move(movement, horizontal=False):
    mouse_input = INPUT(INPUT_MOUSE, mi=MOUSEINPUT(
        mouseData=movement, dwFlags=MOUSEEVENTF_HWHEEL if horizontal else MOUSEEVENTF_WHEEL))
    SENDINPUT(1, byref(mouse_input), sizeof(INPUT))


def mouse_left_click(repeats=1, delay=0):
    for _ in range(0, repeats):
        __mouse_click(MOUSEEVENTF_LEFTDOWN)
        __mouse_click(MOUSEEVENTF_LEFTUP)
        sleep(delay)


def mouse_right_click(repeats=1, delay=0):
    for _ in range(0, repeats):
        __mouse_click(MOUSEEVENTF_RIGHTDOWN)
        __mouse_click(MOUSEEVENTF_RIGHTUP)
        sleep(delay)


def mouse_middle_click(repeats=1, delay=0):
    for _ in range(0, repeats):
        __mouse_click(MOUSEEVENTF_MIDDLEDOWN)
        __mouse_click(MOUSEEVENTF_MIDDLEUP)
        sleep(delay)
