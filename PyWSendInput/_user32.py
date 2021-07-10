from ctypes import POINTER, Structure, Union, WinDLL, c_short, c_bool, wintypes

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

    def __repr__(self):
        return '%r(vkCode=%r, shiftState=%r)' % (self.__class__, self.vkCode, self.shiftState)


class KEYSTATERES(Structure):
    _fields_ = [('wasPressed', c_short, 8),
                ('isDown', c_short, 8)]

    def __repr__(self):
        return '%r(isDown=%r, wasPressed=%r)' % (self.__class__, self.isDown, self.wasPressed)

    def __bool__(self):
        return bool(self.wasPressed or self.isDown)


USER32 = WinDLL('user32')

# general
SENDINPUT = USER32.SendInput
SENDINPUT.argtypes = [wintypes.UINT, POINTER(INPUT), wintypes.INT]

GETSYSTEMMETRICS = USER32.GetSystemMetrics

SETPROCESSDPIAWARE = USER32.SetProcessDPIAware
# endgeneral

# keybord
VKKEYSCANEX = USER32.VkKeyScanExW
VKKEYSCANEX.argtypes = [wintypes.WCHAR, wintypes.HKL]
VKKEYSCANEX.restype = KEYSCANRES

GETKEYBOARDLAYOUT = USER32.GetKeyboardLayout
GETKEYBOARDLAYOUT.argtypes = [wintypes.DWORD]
GETKEYBOARDLAYOUT.restype = wintypes.HKL

GETASYNCKEYSTATE = USER32.GetAsyncKeyState
GETASYNCKEYSTATE.argtypes = [wintypes.INT]
GETASYNCKEYSTATE.restype = KEYSTATERES

MAPVIRTUALKEYEX = USER32.MapVirtualKeyExW
MAPVIRTUALKEYEX.argtypes = [wintypes.UINT, wintypes.UINT, wintypes.HKL]
MAPVIRTUALKEYEX.restype = wintypes.UINT
# endkeyboard

# mouse
GETCURSORPOS = USER32.GetCursorPos
GETCURSORPOS.argtypes = [POINTER(wintypes.POINT)]
GETCURSORPOS.restype = c_bool

SETCURSORPOS = USER32.SetCursorPos
SETCURSORPOS.argtypes = [wintypes.INT, wintypes.INT]
SETCURSORPOS.restype = c_bool
# endmouse

# window
FINDWINDOWEX = USER32.FindWindowExW
FINDWINDOWEX.argtypes = [wintypes.HWND,
                         wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR]
FINDWINDOWEX.restype = wintypes.HWND

SWITCHTOTHISWINDOW = USER32.SwitchToThisWindow
SWITCHTOTHISWINDOW.argtypes = [wintypes.HWND, c_bool]
SWITCHTOTHISWINDOW.restype = wintypes.LPVOID

SETFOREGROUNDWINDOW = USER32.SetForegroundWindow
SETFOREGROUNDWINDOW.argtypes = [wintypes.HWND]
SETFOREGROUNDWINDOW.restype = c_bool

GETFOREGROUNDWINDOW = USER32.GetForegroundWindow
GETFOREGROUNDWINDOW.restype = wintypes.HWND

SENDMESSAGE = USER32.SendMessageW
SENDMESSAGE.argtypes = [wintypes.HWND,
                        wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]

GETWINDOWRECT = USER32.GetWindowRect
GETWINDOWRECT.argtypes = [wintypes.HWND, POINTER(wintypes.RECT)]
GETWINDOWRECT.restype = c_bool
# endwindow

# process
GETWINDOWTHREADPROCESSID = USER32.GetWindowThreadProcessId
GETWINDOWTHREADPROCESSID.argtypes = [wintypes.HWND, wintypes.LPDWORD]
GETWINDOWTHREADPROCESSID.restype = wintypes.DWORD
# endprocess
