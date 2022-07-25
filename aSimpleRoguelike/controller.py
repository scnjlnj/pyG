from collections import deque
from queue import Queue

from pynput import keyboard

keyboard_inputs = Queue()
def add_press_event(key):
    global keyboard_inputs
    key.action=1
    vk = key.vk if hasattr(key,"vk") else str(key)
    keyboard_inputs.put_nowait((vk,1))
def add_release_event(key):
    global keyboard_inputs
    key.action=-1
    vk = key.vk if hasattr(key,"vk") else str(key)
    keyboard_inputs.put_nowait((vk,1))
keyboard_listener = keyboard.Listener(
    on_press=add_press_event,
    on_release=add_release_event)


class BaseController(object):
    _event_list = None
    _listener = None

    def get_events_and_reset_queue(self):
        _data = self._event_list.queue
        self._event_list.queue = deque()
        self._event_list.unfinished_tasks = 0
        return _data

class KeyBoardController(BaseController):
    def __init__(self):
        self._event_list = keyboard_inputs
        self._listener = keyboard_listener
        self._listener.start()

if __name__ == '__main__':

    c = KeyBoardController()
    for x in c.get_events():
        print(x,x.action)