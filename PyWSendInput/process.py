from copy import copy
from ctypes import byref, c_bool, c_int, sizeof, wintypes, c_longlong
from os import path

from PyWSendInput._kernel32 import (CLOSEHANDLE, CONTEXT,
                                    CREATETOOLHELP32SNAPSHOT,
                                    ENUMPROCESSMODULESEX, GETMODULEFILENAMEEX,
                                    GETMODULEINFORMATION, GETTHREADCONTEXT,
                                    GETTHREADSELECTORENRTY, IS64BIT,
                                    ISWOW64PROCESS, LDTENTRY, MODULEINFO,
                                    OPENPROCESS, OPENTHREAD, READPROCESSMEMORY,
                                    THREAD32FIRST, THREAD32NEXT, THREADENTRY32,
                                    WRITEPROCESSMEMORY)
from PyWSendInput._user32 import GETWINDOWTHREADPROCESSID
from PyWSendInput._ntdll import NTQUERYINFORMATIONTHREAD, THREADBASICINFORMATION

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)

TH32CS_SNAPALL = (0x00000001 | 0x00000002 | 0x00000004 | 0x00000008)

THREAD_GET_CONTEXT = 0x0008
THREAD_QUERY_INFORMATION = 0x0040

CONTEXT_PLATFORM = 0x00100000 if IS64BIT else 0x00010000
CONTEXT_SEGMENTS = (CONTEXT_PLATFORM | 0x0004)

LIST_MODULES_32BIT = 0x01
LIST_MODULES_64BIT = 0x02
LIST_MODULES_ALL = 0x03


def get_window_thread_process_id(window, process_id=None):
    return GETWINDOWTHREADPROCESSID(window, process_id)


def get_window_process_id(window):
    dword = wintypes.DWORD()
    GETWINDOWTHREADPROCESSID(window, byref(dword))
    return dword.value


def open_process(process_id, desired_access=PROCESS_ALL_ACCESS, inherit_handle=False):
    return OPENPROCESS(desired_access, inherit_handle, process_id)


def read_process_memory(process, base_address, buffer, size, number_of_bytes_read=None):
    return READPROCESSMEMORY(process, base_address, buffer, size, number_of_bytes_read)


def write_process_memory(process, base_address, buffer, size, number_of_bytes_written=None):
    return WRITEPROCESSMEMORY(process, base_address, buffer, size, number_of_bytes_written)


def close_handle(process):
    return CLOSEHANDLE(process)


def get_threads_from_process_id(pid=None):
    thread_snap = CREATETOOLHELP32SNAPSHOT(TH32CS_SNAPALL, 0)
    threads = []

    if not thread_snap:
        return threads

    thread = THREADENTRY32()
    thread.dwSize = sizeof(THREADENTRY32)

    if not THREAD32FIRST(thread_snap, byref(thread)):
        return threads

    while True:
        if (not pid) or thread.th32OwnerProcessID == pid:
            threads.append(copy(thread))

        if not THREAD32NEXT(thread_snap, byref(thread)):
            break

    close_handle(thread_snap)

    return threads


def is_process_64bit(phandle):
    if IS64BIT:
        iswow64 = c_bool()
        if ISWOW64PROCESS(phandle, byref(iswow64)):
            return not iswow64
        return False

    return False


def open_thread(thid, desired_access=THREAD_GET_CONTEXT | THREAD_QUERY_INFORMATION, inherit_handle=False):
    return OPENTHREAD(desired_access, inherit_handle, thid)


def get_thread_stack(thid, phandle):
    is64b = is_process_64bit(phandle)
    addrtype = c_longlong if is64b else c_int
    stack = addrtype(0)
    thandle = open_thread(thid)
    result = 0

    if not thandle:
        return result

    minfo = MODULEINFO()
    mhandle = get_modules_from_process(phandle).get('KERNEL32.DLL')
    if (not mhandle) or (not GETMODULEINFORMATION(phandle, mhandle, byref(minfo), sizeof(minfo))):
        close_handle(thandle)
        return result

    if is64b == IS64BIT:
        tbi = THREADBASICINFORMATION()
        ntstatus = NTQUERYINFORMATIONTHREAD(
            thandle, 0, byref(tbi), sizeof(tbi), None)
        if ntstatus:
            print('NTSTATUS:', format(ntstatus & 0xffffffff, '#010x'))
            close_handle(thandle)
            return result

        read_process_memory(phandle, tbi.TebBaseAddress +
                            sizeof(stack), byref(stack), sizeof(stack))
    else:
        context = CONTEXT()
        context.ContextFlags = CONTEXT_SEGMENTS
        if not GETTHREADCONTEXT(thandle, byref(context)):
            close_handle(thandle)
            return result

        ldt = LDTENTRY()
        if not GETTHREADSELECTORENRTY(thandle, context.SegFs, byref(ldt)):
            close_handle(thandle)
            return result

        val1 = ldt.HighWord.Bytes.BaseMid & 0xff
        val2 = ldt.HighWord.Bytes.BaseHi & 0xff
        address = ldt.BaseLow + (val1 << 16) + (val2 << 24)
        read_process_memory(phandle, address + sizeof(stack),
                            byref(stack), sizeof(stack))

    if not stack.value:
        close_handle(thandle)
        return result

    result = stack.value
    buffer = (addrtype * (4096 // sizeof(stack)))()

    if not read_process_memory(phandle, stack.value - 4096, buffer, 4096):
        close_handle(thandle)
        return result

    for idx in range(4096 // sizeof(stack) - 1, -1, -1):
        value = buffer[idx]
        if value >= minfo.lpBaseOfDll and value <= minfo.lpBaseOfDll + minfo.SizeOfImage:
            result = stack.value - 4096 + idx * sizeof(stack)
            break

    close_handle(thandle)

    return result


def get_modules_from_process(phandle):
    modules = {}
    hmodules = (wintypes.HMODULE * 1024)()
    cbneeded = wintypes.DWORD()

    if not ENUMPROCESSMODULESEX(phandle, hmodules, sizeof(hmodules), byref(cbneeded), LIST_MODULES_ALL):
        print('fail enum')
        return modules

    for idx in range(0, cbneeded.value // sizeof(wintypes.HMODULE)):
        mname = (wintypes.WCHAR * 1024)()
        if GETMODULEFILENAMEEX(phandle, hmodules[idx], mname, 1024):
            modules[path.split(mname.value)[1]] = hmodules[idx]
        else:
            modules[idx] = hmodules[idx]

    return modules


class Address(object):
    def __init__(self, process_handle, ctype, base_address):
        self._phandle = process_handle
        self._value = ctype()
        self.base_address = base_address
        self.ctype = ctype

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '{:#X}: '.format(self.base_address)+str(self.value)

    @property
    def value(self):
        read_process_memory(self._phandle, self.base_address,
                            byref(self._value), sizeof(self.ctype))
        return self._value.value

    @value.setter
    def value(self, value):
        self._value.value = value
        write_process_memory(self._phandle, self.base_address,
                             byref(self._value), sizeof(self.ctype))

    def change_ctype(self, ctype, value=None):
        self.ctype = ctype
        self._value = ctype(value or self._value.value)


class PointerAddress(Address):
    def __init__(self, process_handle, ctype, base_address, *args):
        super(PointerAddress, self).__init__(
            process_handle, ctype, base_address)
        self.offsets = args
        self._addrtype = c_longlong if is_process_64bit(process_handle) else c_int

    def get_address(self):
        address = self._addrtype(self.base_address)

        for offset in self.offsets[:-1]:
            read_process_memory(self._phandle, address.value +
                                offset, byref(address), sizeof(address))

        return address.value + self.offsets[-1]

    @property
    def value(self):
        read_process_memory(self._phandle, self.get_address(),
                            byref(self._value), sizeof(self.ctype))
        return self._value.value

    @value.setter
    def value(self, value):
        self._value.value = value
        write_process_memory(self._phandle, self.get_address(),
                             byref(self._value), sizeof(self.ctype))
