from ctypes import WinDLL, wintypes, c_size_t, c_bool, POINTER

KERNEL32 = WinDLL('kernel32')

# process
OPENPROCESS = KERNEL32.OpenProcess
OPENPROCESS.argtypes = [wintypes.DWORD, c_bool, wintypes.DWORD]
OPENPROCESS.restype = wintypes.HANDLE

WRITEPROCESSMEMORY = KERNEL32.WriteProcessMemory
WRITEPROCESSMEMORY.argtypes = [
    wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, c_size_t, POINTER(c_size_t)]
WRITEPROCESSMEMORY.restype = c_bool

READPROCESSMEMORY = KERNEL32.ReadProcessMemory
READPROCESSMEMORY.argtypes = [
    wintypes.HANDLE, wintypes.LPCVOID, wintypes.LPVOID, c_size_t, POINTER(c_size_t)]
READPROCESSMEMORY.restype = c_bool

CLOSEHANDLE = KERNEL32.CloseHandle
CLOSEHANDLE.argtypes = [wintypes.HANDLE]
CLOSEHANDLE.restype = c_bool
# endprocess
