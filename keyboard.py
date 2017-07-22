from ctypes import byref, sizeof
from time import sleep
from PyWSendInput import SENDINPUT, INPUT, INPUT_KEYBOARD, KEYBDINPUT

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004


def keyboard_press(vkcodes):
    keyboard_inputs = (INPUT * len(vkcodes))()
    for i, vkcode in enumerate(vkcodes):
        keyboard_inputs[i] = INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(vkcode))
    SENDINPUT(len(vkcodes), keyboard_inputs, sizeof(INPUT))


def keyboard_release(vkcodes):
    keyboard_inputs = (INPUT * len(vkcodes))()
    for i, vkcode in enumerate(vkcodes):
        keyboard_inputs[i] = INPUT(
            INPUT_KEYBOARD, ki=KEYBDINPUT(vkcode, dwFlags=KEYEVENTF_KEYUP))
    SENDINPUT(len(vkcodes), keyboard_inputs, sizeof(INPUT))


def keyboard_tap(vkcodes, repeats=1, delay=0):
    keyboard_inputs = (INPUT * (2 * len(vkcodes)))()
    for i, vkcode in enumerate(vkcodes):
        keyboard_inputs[(i * 2)] = INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(vkcode))
        keyboard_inputs[(i * 2) + 1] = INPUT(INPUT_KEYBOARD,
                                             ki=KEYBDINPUT(vkcode, dwFlags=KEYEVENTF_KEYUP))
    for _ in range(0, repeats):
        SENDINPUT(2 * len(vkcodes), keyboard_inputs, sizeof(INPUT))
        sleep(delay)
