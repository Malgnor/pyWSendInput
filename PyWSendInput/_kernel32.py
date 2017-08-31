from ctypes import WinDLL, wintypes, c_size_t, c_bool, POINTER, Structure

KERNEL32 = WinDLL('kernel32')


class THREADENTRY32(Structure):
    _fields_ = [
        ('dwSize', wintypes.DWORD),
        ('cntUsage', wintypes.DWORD),
        ('th32ThreadID', wintypes.DWORD),
        ('th32OwnerProcessID', wintypes.DWORD),
        ('tpBasePri', wintypes.LONG),
        ('tpDeltaPri', wintypes.LONG),
        ('dwFlags', wintypes.DWORD)]

    def __repr__(self):
        return '%r(th32ThreadID=%r, th32OwnerProcessID=%r)' % (self.__class__, self.th32ThreadID, self.th32OwnerProcessID)


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

CREATETOOLHELP32SNAPSHOT = KERNEL32.CreateToolhelp32Snapshot
CREATETOOLHELP32SNAPSHOT.argtypes = [wintypes.DWORD, wintypes.DWORD]
CREATETOOLHELP32SNAPSHOT.restype = wintypes.HANDLE

THREAD32FIRST = KERNEL32.Thread32First
THREAD32FIRST.argtypes = [wintypes.HANDLE, POINTER(THREADENTRY32)]
THREAD32FIRST.restype = c_bool

THREAD32NEXT = KERNEL32.Thread32Next
THREAD32NEXT.argtypes = [wintypes.HANDLE, POINTER(THREADENTRY32)]
THREAD32NEXT.restype = c_bool
# endprocess
