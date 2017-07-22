from ctypes import byref, sizeof
from time import sleep
from PyWSendInput import SENDINPUT, INPUT, INPUT_KEYBOARD, KEYBDINPUT

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004


def keyboard_press(vkcode):
    keyboard_input = INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(vkcode))
    SENDINPUT(1, byref(keyboard_input), sizeof(keyboard_input))


def keyboard_release(vkcode):
    keyboard_input = INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(
        vkcode, dwFlags=KEYEVENTF_KEYUP))
    SENDINPUT(1, byref(keyboard_input), sizeof(keyboard_input))


def keyboard_tap(vkcode, repeats=1, delay=0):
    keyboard_inputs = (INPUT * 2)(INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(vkcode)), INPUT(
        INPUT_KEYBOARD, ki=KEYBDINPUT(vkcode, dwFlags=KEYEVENTF_KEYUP)))
    for _ in range(0, repeats):
        SENDINPUT(2, keyboard_inputs, sizeof(INPUT))
        sleep(delay)
        