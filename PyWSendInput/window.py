from PyWSendInput._user32 import FINDWINDOWEX, SWITCHTOTHISWINDOW, SETFOREGROUNDWINDOW, GETFOREGROUNDWINDOW, SENDMESSAGE

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_CHAR = 0x0102


def find_window(window_name='', parent=None, child_after=None, window_class=None):
    return FINDWINDOWEX(parent, child_after, window_class, window_name)


def switch_to_this_window(window, alt_tab=False):
    return SWITCHTOTHISWINDOW(window, alt_tab)


def set_foreground_window(window):
    return SETFOREGROUNDWINDOW(window)


def get_foreground_window():
    return GETFOREGROUNDWINDOW()


def send_message(window, msg, wparam, lparam=0):
    return SENDMESSAGE(window, msg, wparam, lparam)


class Window(object):
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.handle = kwargs.pop('handle', None) or find_window(self.name)

    def send_key_press(self, vkcodes):
        for vkcode in vkcodes:
            send_message(self.handle, WM_KEYDOWN, vkcode)

    def send_key_release(self, vkcodes):
        for vkcode in vkcodes:
            send_message(self.handle, WM_KEYUP, vkcode, 1)

    def send_key_tap(self, vkcodes):
        for vkcode in vkcodes:
            send_message(self.handle, WM_KEYDOWN, vkcode)
            send_message(self.handle, WM_KEYUP, vkcode, 1)

    def send_text(self, text):
        for char in text:
            send_message(self.handle, WM_KEYDOWN, ord(char))
            send_message(self.handle, WM_CHAR, ord(char), 1)
            send_message(self.handle, WM_KEYUP, ord(char), 1)
