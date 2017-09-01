from ctypes import WinDLL, wintypes, c_size_t, c_bool, POINTER, Structure, Union
from platform import architecture

IS64BIT = True if architecture()[0] == '64bit' else False

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


class _LDTBYTES(Structure):
    _fields_ = [('BaseMid', wintypes.BYTE),
                ('Flags1', wintypes.BYTE),
                ('Flags2', wintypes.BYTE),
                ('BaseHi', wintypes.BYTE)]


class _LDTBITS(Structure):
    _fields_ = [('BaseMid', wintypes.DWORD, 8),
                ('Type', wintypes.DWORD, 5),
                ('Dpl', wintypes.DWORD, 2),
                ('Pres', wintypes.DWORD, 1),
                ('LimitHi', wintypes.DWORD, 4),
                ('Sys', wintypes.DWORD, 1),
                ('Reserved_0', wintypes.DWORD, 1),
                ('Default_Big', wintypes.DWORD, 1),
                ('Granularity', wintypes.DWORD, 1),
                ('BaseHi', wintypes.DWORD, 8)]


class HIGHWORD(Union):
    _fields_ = [('Bytes', _LDTBYTES),
                ('Bits', _LDTBITS)]


class LDTENTRY(Structure):
    _fields_ = [
        ('LimitLow', wintypes.WORD),
        ('BaseLow', wintypes.WORD),
        ('HighWord', HIGHWORD)]


SIZEOF80387REGISTERS = 80


class FLOATINGSAVEAREA(Structure):
    _fields_ = [
        ('ControlWord', wintypes.DWORD),
        ('StatusWord', wintypes.DWORD),
        ('TagWord', wintypes.DWORD),
        ('ErrorOffset', wintypes.DWORD),
        ('ErrorSelector', wintypes.DWORD),
        ('DataOffset', wintypes.DWORD),
        ('DataSelector', wintypes.DWORD),
        ('RegisterArea', wintypes.BYTE * SIZEOF80387REGISTERS),
        ('Cr0NpxState', wintypes.DWORD)
    ]


MAXIMUMSUPPORTEDEXTENSION = 512


class CONTEXT(Structure):
    _fields_ = [
        ('ContextFlags', wintypes.DWORD),
        ('Dr0', wintypes.DWORD),
        ('Dr1', wintypes.DWORD),
        ('Dr2', wintypes.DWORD),
        ('Dr3', wintypes.DWORD),
        ('Dr6', wintypes.DWORD),
        ('Dr7', wintypes.DWORD),
        ('FloatSave', FLOATINGSAVEAREA),
        ('SegGs', wintypes.DWORD),
        ('SegFs', wintypes.DWORD),
        ('SegEs', wintypes.DWORD),
        ('SegDs', wintypes.DWORD),
        ('Edi', wintypes.DWORD),
        ('Esi', wintypes.DWORD),
        ('Ebx', wintypes.DWORD),
        ('Edx', wintypes.DWORD),
        ('Ecx', wintypes.DWORD),
        ('Eax', wintypes.DWORD),
        ('Ebp', wintypes.DWORD),
        ('Eip', wintypes.DWORD),
        ('SegCs', wintypes.DWORD),
        ('EFlags', wintypes.DWORD),
        ('Esp', wintypes.DWORD),
        ('SegSs', wintypes.DWORD),
        ('ExtendedRegisters', wintypes.BYTE * MAXIMUMSUPPORTEDEXTENSION)]


class MODULEINFO(Structure):
    _fields_ = [('lpBaseOfDll', wintypes.LPVOID),
                ('SizeOfImage', wintypes.DWORD),
                ('EntryPoint', wintypes.LPVOID)]


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

ISWOW64PROCESS = KERNEL32.IsWow64Process
ISWOW64PROCESS.argtypes = [wintypes.HANDLE, POINTER(c_bool)]
ISWOW64PROCESS.restype = c_bool

GETTHREADSELECTORENRTY = KERNEL32.Wow64GetThreadSelectorEntry if IS64BIT else KERNEL32.GetThreadSelectorEntry
GETTHREADSELECTORENRTY.argtypes = [
    wintypes.HANDLE, wintypes.DWORD, POINTER(LDTENTRY)]
GETTHREADSELECTORENRTY.restype = c_bool

GETTHREADCONTEXT = KERNEL32.Wow64GetThreadContext if IS64BIT else KERNEL32.GetThreadContext
GETTHREADCONTEXT.argtypes = [wintypes.HANDLE, POINTER(CONTEXT)]
GETTHREADCONTEXT.restype = c_bool

OPENTHREAD = KERNEL32.OpenThread
OPENTHREAD.argtypes = [wintypes.DWORD, c_bool, wintypes.DWORD]
OPENTHREAD.restype = wintypes.HANDLE

GETMODULEHANDLE = KERNEL32.GetModuleHandleW
GETMODULEHANDLE.argtypes = [wintypes.LPCWSTR]
GETMODULEHANDLE.restype = wintypes.HMODULE

GETMODULEINFORMATION = KERNEL32.K32GetModuleInformation
GETMODULEINFORMATION.argtypes = [
    wintypes.HANDLE, wintypes.HMODULE, POINTER(MODULEINFO), wintypes.DWORD]
GETMODULEINFORMATION.restype = c_bool

ENUMPROCESSMODULESEX = KERNEL32.K32EnumProcessModulesEx
ENUMPROCESSMODULESEX.argtypes = [wintypes.HANDLE, POINTER(
    wintypes.HMODULE), wintypes.DWORD, POINTER(wintypes.DWORD), wintypes.DWORD]
ENUMPROCESSMODULESEX.restype = c_bool

GETMODULEFILENAMEEX = KERNEL32.K32GetModuleFileNameExW
GETMODULEFILENAMEEX.argtypes = [
    wintypes.HANDLE, wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD]
GETMODULEFILENAMEEX.restype = wintypes.DWORD
# endprocess
