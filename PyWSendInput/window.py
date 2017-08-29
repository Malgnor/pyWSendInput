from PyWSendInput._user32 import FINDWINDOWEX, SWITCHTOTHISWINDOW, SETFOREGROUNDWINDOW, GETFOREGROUNDWINDOW


def find_window(window_name='', parent=None, child_after=None, window_class=None):
    return FINDWINDOWEX(parent, child_after, window_class, window_name)


def switch_to_this_window(window, alt_tab=False):
    return SWITCHTOTHISWINDOW(window, alt_tab)


def set_foreground_window(window):
    return SETFOREGROUNDWINDOW(window)


def get_foreground_window():
    return GETFOREGROUNDWINDOW
