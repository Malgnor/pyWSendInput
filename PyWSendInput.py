from ctypes import wintypes, Structure, Union, WinDLL, POINTER

''' https://msdn.microsoft.com/en-us/library/ms646310(v=vs.85).aspx
UINT WINAPI SendInput(
  _In_ UINT    nInputs,
  _In_ LPINPUT pInputs,
  _In_ int     cbSize
);

typedef struct tagMOUSEINPUT {
  LONG      dx;
  LONG      dy;
  DWORD     mouseData;
  DWORD     dwFlags;
  DWORD     time;
  ULONG_PTR dwExtraInfo;
} MOUSEINPUT, *PMOUSEINPUT;

typedef struct tagKEYBDINPUT {
  WORD      wVk;
  WORD      wScan;
  DWORD     dwFlags;
  DWORD     time;
  ULONG_PTR dwExtraInfo;
} KEYBDINPUT, *PKEYBDINPUT;

typedef struct tagHARDWAREINPUT {
  DWORD uMsg;
  WORD  wParamL;
  WORD  wParamH;
} HARDWAREINPUT, *PHARDWAREINPUT;

typedef struct tagINPUT {
  DWORD type;
  union {
    MOUSEINPUT    mi;
    KEYBDINPUT    ki;
    HARDWAREINPUT hi;
  };
} INPUT, *PINPUT;
'''

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


SENDINPUT = WinDLL('user32').SendInput
SENDINPUT.argtypes = [wintypes.UINT, POINTER(INPUT), wintypes.INT]
