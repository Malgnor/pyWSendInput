from copy import copy
from ctypes import byref, c_bool, c_int, sizeof, wintypes
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
    stack = c_int(0)
    thandle = open_thread(thid)
    result = 0

    if not thandle:
        return result

    minfo = MODULEINFO()
    mhandle = get_modules_from_process(phandle).get('KERNEL32.DLL')
    if (not mhandle) or (not GETMODULEINFORMATION(phandle, mhandle, byref(minfo), sizeof(minfo))):
        close_handle(thandle)
        return result

    is64b = is_process_64bit(phandle)

    if is64b == IS64BIT:
        pass
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

        val1 = ldt.HighWord.Bytes.BaseMid if ldt.HighWord.Bytes.BaseMid >= 0 else 256 + \
            ldt.HighWord.Bytes.BaseMid
        val2 = ldt.HighWord.Bytes.BaseHi if ldt.HighWord.Bytes.BaseHi >= 0 else 256 + \
            ldt.HighWord.Bytes.BaseHi
        address = ldt.BaseLow + (val1 << 16) + (val2 << 24)
        read_process_memory(phandle, address + 4, byref(stack), 4)

    if not stack.value:
        close_handle(thandle)
        return result

    result = stack.value
    addrsize = 8 if is64b else 4
    buffer = (c_int * (4096 // addrsize))()

    if not read_process_memory(phandle, stack.value - 4096, buffer, 4096):
        close_handle(thandle)
        return result

    for idx in range(4096 // 4 - 1, -1, -1):
        value = buffer[idx]
        if value >= minfo.lpBaseOfDll and value <= minfo.lpBaseOfDll + minfo.SizeOfImage:
            result = stack.value - 4096 + idx * addrsize
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
