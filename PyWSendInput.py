from ctypes import POINTER, Structure, Union, WinDLL, c_short, wintypes

# https://msdn.microsoft.com/en-us/library/ms646310(v=vs.85).aspx

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2


class MOUSEINPUT(Structure):
    _fields_ = [('dx', wintypes.LONG),
                ('dy', wintypes.LONG),
                ('mouseData', wintypes.DWORD),
                ('dwFlags', wintypes.DWORD),
                ('time', wintypes.DWORD),
                ('dwExtraInfo', wintypes.PULONG)]


class KEYBDINPUT(Structure):
    _fields_ = [('wVk', wintypes.WORD),
                ('wScan', wintypes.WORD),
                ('dwFlags', wintypes.DWORD),
                ('time', wintypes.DWORD),
                ('dwExtraInfo', wintypes.PULONG)]


class HARDWAREINPUT(Structure):
    _fields_ = [('uMsg', wintypes.DWORD),
                ('wParamL', wintypes.WORD),
                ('wParamH', wintypes.WORD)]


class UNION(Union):
    _fields_ = [('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT)]


class INPUT(Structure):
    _anonymous_ = ('union',)
    _fields_ = [('type', wintypes.DWORD),
                ('union', UNION)]


class KEYSCANRES(Structure):
    _fields_ = [('vkCode', c_short, 8),
                ('shiftState', c_short, 8)]


USER32 = WinDLL('user32')

SENDINPUT = USER32.SendInput
SENDINPUT.argtypes = [wintypes.UINT, POINTER(INPUT), wintypes.INT]

VKKEYSCANEX = USER32.VkKeyScanExW
VKKEYSCANEX.argtypes = [wintypes.WCHAR, wintypes.HKL]
VKKEYSCANEX.restype = KEYSCANRES

GETKEYBOARDLAYOUT = USER32.GetKeyboardLayout
GETKEYBOARDLAYOUT.argtypes = [wintypes.DWORD]
GETKEYBOARDLAYOUT.restype = wintypes.HKL

GETSYSTEMMETRICS = USER32.GetSystemMetrics

SETPROCESSDPIAWARE = USER32.SetProcessDPIAware

GETCURSORPOS = USER32.GetCursorPos
GETCURSORPOS.argtypes = [POINTER(wintypes.POINT)]
