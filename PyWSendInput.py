from ctypes import *
from ctypes import wintypes
import time, math

'''
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

SendInput = WinDLL('user32').SendInput
SendInput.argtypes = [wintypes.UINT, POINTER(INPUT), wintypes.INT]

'''
mouse = INPUT(0, mi=MOUSEINPUT(dwFlags=0x0001))
for ang in [math.pi/5*i for i in range(0, 21)]:
    time.sleep(0.05)
    mouse.mi.dx = int(math.cos(ang)*50)
    mouse.mi.dy = int(math.sin(ang)*50)
    SendInput(1, byref(mouse), sizeof(mouse))
'''