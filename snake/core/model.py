import os
import random
import threading
import time
from queue import Queue, Empty
from collections import deque

import keyboard

SIZE = 12
fps = 20

class Table(object):
    def __init__(self):
        self.size = SIZE
        self.objects = []
    def print_in_str(self):
        os.system("cls")
        print("\n")
        table = [["·"]*SIZE for x in range(self.size)]
        for o in self.objects:
            if type(o) is Snake:
                char = o.tail_char
                for t in o.tail:
                    x,y = t
                    table[x][y] = char
            char = str(o)
            x,y = o.body
            table[x][y] = char
        for i in table:
            print("\t".join(i))
            print("\n")
    def init(self):
        mid = SIZE//2
        walls = [Wall((x,0)) for x in range(SIZE)]+\
                [Wall((0,x)) for x in range(1,SIZE)]+\
                [Wall((x,SIZE-1)) for x in range(1,SIZE)]+\
                [Wall((SIZE-1,x)) for x in range(1,SIZE-1)]
        user = Snake((mid,mid))
        self.objects+=walls+[user]
        return user
    def spawn(self, action):
        pass
class BaseObject(object):
    def __init__(self,pos):
        self.body = pos
        self.static=None
        self.alive = None
class Wall(BaseObject):
    def __init__(self,pos):
        super().__init__(pos)
        self.static=True
    def __str__(self):
        return "#"
class Food(BaseObject):
    def __init__(self,pos):
        super().__init__(pos)
        self.static=False
    def __str__(self):
        return "*"
class Snake(BaseObject):
    def __init__(self,pos):
        super().__init__(pos)
        self.head=pos
        self.tail=deque()
        self.lenth = 1
        self.static = False
        self.alive = True
        self.tail_char = "⚪"
        self.vel = 20
        self.direction = "Up"
        self.motivation = 0
    def __str__(self):
        return "@"
    def __repr__(self):
        return f"<Snake:{self.lenth}>"
    def move(self):
        self.motivation+=self.vel/fps
        if self.motivation>=1:
            self.motivation-=1
            x,y = self.body
            if self.direction == "Up":
                self.body = (x-1,y)
            elif self.direction == "Down":
                self.body = (x+1,y)
            elif self.direction == "Left":
                self.body = (x,y-1)
            elif self.direction == "Right":
                self.body = (x,y+1)
    def handel_collision(self,obj):
        pass



if __name__ == '__main__':
    tab = Table()
    user = tab.init()
    # t.print_in_str()
    action=Queue()
    tick=0
    def get_keyboard_input(q):
        def set_action(s):
            q.empty()
            q.put(s)
        keyboard.add_hotkey('up', set_action,args=("Up",))
        keyboard.add_hotkey('down', set_action,args=("Down",))
        keyboard.add_hotkey('left', set_action,args=("Left",))
        keyboard.add_hotkey('right', set_action,args=("Right",))
        keyboard.wait()
    t = threading.Thread(target=get_keyboard_input,args=(action,))
    t.setDaemon(True)
    t.start()
    while True:
        try:
            data = action.get_nowait()
        except Empty:
            data="empty"
        if data and data in ("Up","Down","Left","Right"):
            user.direction = data
        #move
        user.move()
        #handel_collision

        #spawn
        os.system("cls")
        tab.print_in_str()
        time.sleep(1/fps)
        tick+=1
    print("OK")