from copy import copy
from ctypes import byref, sizeof, wintypes

from PyWSendInput._kernel32 import (CLOSEHANDLE, CREATETOOLHELP32SNAPSHOT,
                                    OPENPROCESS, READPROCESSMEMORY,
                                    THREAD32FIRST, THREAD32NEXT, THREADENTRY32,
                                    WRITEPROCESSMEMORY)
from PyWSendInput._user32 import GETWINDOWTHREADPROCESSID

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
TH32CS_SNAPALL = (0x00000001 | 0x00000002 | 0x00000004 | 0x00000008)


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


def get_threads_from_process(pid=None):
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
