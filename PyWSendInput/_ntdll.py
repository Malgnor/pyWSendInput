from ctypes import wintypes, WinDLL, Structure

NTDLL = WinDLL('ntdll')

NTSTATUS = wintypes.LONG
KAFFINITY = wintypes.ULONG
KPRIORITY = wintypes.ULONG


class CLIENTID(Structure):
    _fields_ = [('UniqueProcess', wintypes.HANDLE),
                ('UniqueThread', wintypes.HANDLE)]


class THREADBASICINFORMATION(Structure):
    _fields_ = [
        ('ExitStatus', NTSTATUS),
        ('TebBaseAddress', wintypes.LPVOID),
        ('ClientId', CLIENTID),
        ('AffinityMask', KAFFINITY),
        ('Priority', KPRIORITY),
        ('BasePriority', KPRIORITY)]


NTQUERYINFORMATIONTHREAD = NTDLL.NtQueryInformationThread
NTQUERYINFORMATIONTHREAD.argtypes = [
    wintypes.HANDLE, wintypes.LONG, wintypes.LPVOID, wintypes.ULONG, wintypes.PULONG]
NTQUERYINFORMATIONTHREAD.restype = NTSTATUS
