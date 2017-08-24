from ctypes import sizeof
from time import sleep

from PyWSendInput._user32 import (GETKEYBOARDLAYOUT, INPUT, INPUT_KEYBOARD, KEYBDINPUT,
                                  SENDINPUT, VKKEYSCANEX)
from PyWSendInput.vkcodes import ALT_KEY, CTRL_KEY, SHIFT_KEY

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004

MODIFIER_SHIFT = 1
MODIFIER_CTRL = 2
MODIFIER_ALT = 4


def keyboard_press(vkcodes):
    keyboard_inputs = (INPUT * len(vkcodes))()
    for i, vkcode in enumerate(vkcodes):
        keyboard_inputs[i] = INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(vkcode))

    return SENDINPUT(len(vkcodes), keyboard_inputs, sizeof(INPUT))


def keyboard_release(vkcodes):
    keyboard_inputs = (INPUT * len(vkcodes))()
    for i, vkcode in enumerate(vkcodes):
        keyboard_inputs[i] = INPUT(
            INPUT_KEYBOARD, ki=KEYBDINPUT(vkcode, dwFlags=KEYEVENTF_KEYUP))

    return SENDINPUT(len(vkcodes), keyboard_inputs, sizeof(INPUT))


def keyboard_tap(vkcodes, repeats=1, delay=0):
    keyboard_inputs = (INPUT * (2 * len(vkcodes)))()
    for i, vkcode in enumerate(vkcodes):
        keyboard_inputs[(i * 2)] = INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(vkcode))
        keyboard_inputs[(i * 2) + 1] = INPUT(INPUT_KEYBOARD,
                                             ki=KEYBDINPUT(vkcode, dwFlags=KEYEVENTF_KEYUP))

    count = 0
    for _ in range(0, repeats):
        count += SENDINPUT(2 * len(vkcodes), keyboard_inputs, sizeof(INPUT))
        sleep(delay)

    return count


def keyboard_write(text, ignore_modifiers=False):
    layout = GETKEYBOARDLAYOUT(0)

    inputs = []
    for char in text:
        result = VKKEYSCANEX(char, layout)

        if not ignore_modifiers:
            if MODIFIER_SHIFT & result.shiftState:
                inputs.append(INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(SHIFT_KEY)))
            if MODIFIER_CTRL & result.shiftState:
                inputs.append(INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(CTRL_KEY)))
            if MODIFIER_ALT & result.shiftState:
                inputs.append(INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(ALT_KEY)))

        if inputs and result.vkCode == inputs[-1].ki.wVk:
            inputs.append(INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT()))

        inputs.append(INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(result.vkCode)))

        if not ignore_modifiers:
            if MODIFIER_SHIFT & result.shiftState:
                inputs.append(INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(
                    SHIFT_KEY, dwFlags=KEYEVENTF_KEYUP)))
            if MODIFIER_CTRL & result.shiftState:
                inputs.append(INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(
                    CTRL_KEY, dwFlags=KEYEVENTF_KEYUP)))
            if MODIFIER_ALT & result.shiftState:
                inputs.append(INPUT(INPUT_KEYBOARD, ki=KEYBDINPUT(
                    ALT_KEY, dwFlags=KEYEVENTF_KEYUP)))

    keyboard_inputs = (INPUT * len(inputs))()
    for i, value in enumerate(inputs):
        keyboard_inputs[i] = value

    return SENDINPUT(len(inputs), keyboard_inputs, sizeof(INPUT))
