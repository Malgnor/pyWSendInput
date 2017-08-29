from ctypes import wintypes, byref
from PyWSendInput._kernel32 import (CLOSEHANDLE, OPENPROCESS, READPROCESSMEMORY,
                                    WRITEPROCESSMEMORY)
from PyWSendInput._user32 import GETWINDOWTHREADPROCESSID

PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)


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
