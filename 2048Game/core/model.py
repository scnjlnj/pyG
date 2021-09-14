import os
import random
import time

import keyboard

SIZE = 6
SPAWN_LIST = [2, 4, 8]


class Table(object):
    def __init__(self):
        self.table = [[Cube() for _ in range(SIZE)] for _ in range(SIZE)]
        self.sum = 0

    @property
    def T(self):
        ret = [[self.table[y][x] for y in range(SIZE)]for x in range(SIZE)]
        return ret


    def print_in_str(self):
        os.system("cls")
        print("\n" * 3)
        for x in self.table:
            out = "\t".join([str(i.val) for i in x])
            print(f"""\t{out}\t""")

    def move(self, action):
        for cube_list in self.T if action in ("Up","Down") else self.table:
            Cube.merge(cube_list,action)

    def spawn(self, action):
        x, y = None, None
        if action == "Down":
            x = 0
        elif action == "Up":
            x = -1
        elif action == "Left":
            y = -1
        elif action == "Right":
            y = 0
        else:
            print(f"{action} not support,Spawn error")
            return
        try:
            x, y = (random.choice([i for i in range(SIZE) if self.table[i][y].val == 0]), y) if x is None else (
        x, random.choice([i for i in range(SIZE) if self.table[x][i].val == 0]))
        except IndexError as e:
            return
        self.table[x][y].val = random.choice(SPAWN_LIST)


class Cube(object):
    def __init__(self, num=0):
        self.val = num

    def __str__(self):
        return self.val
    def __repr__(self):
        return f"<Cube:{self.val}>"
    @classmethod
    def merge(cls, cube_list, action):

        if action in ("Down","Right"):
            cur = len(cube_list)-1
            temp = None
            while cur>-1:
                if cube_list[cur].val!=0 and temp and temp.val==cube_list[cur].val:
                    temp.val*=2
                    cube_list[cur].val=0
                elif cube_list[cur].val!=0:
                    temp = cube_list[cur]
                cur-=1
            p=len(cube_list)-1
            for i in range(len(cube_list)-1,-1,-1):
                if cube_list[i].val==0:
                    while p>-1 and cube_list[p].val==0:p-=1
                    if p==-1:
                        break
                    else:
                        cube_list[i].val, cube_list[p].val = cube_list[p].val, cube_list[i].val
                p-=1
        elif action in ("Up","Left"):
            cur = 0
            temp = None
            while cur<len(cube_list):
                if cube_list[cur].val!=0 and temp and temp.val==cube_list[cur].val:
                    temp.val*=2
                    cube_list[cur].val=0
                elif cube_list[cur].val!=0:
                    temp = cube_list[cur]
                cur+=1
            p=0
            for i in range(len(cube_list)):
                if cube_list[i].val == 0:
                    while p <len(cube_list) and cube_list[p].val == 0: p += 1
                    if p == len(cube_list):
                        break
                    else:
                        cube_list[i].val, cube_list[p].val = cube_list[p].val, cube_list[i].val
                p+=1


if __name__ == '__main__':
    t = Table()
    action=""
    def set_action(s):
        action = s
        t.move(action)
        t.spawn(action)
        t.print_in_str()
    keyboard.add_hotkey('up', set_action,args=("Up",))
    keyboard.add_hotkey('down', set_action,args=("Down",))
    keyboard.add_hotkey('left', set_action,args=("Left",))
    keyboard.add_hotkey('right', set_action,args=("Right",))
    keyboard.wait()

    # cube_list = [Cube(0),Cube(2),Cube(4),Cube(0)]
    # Cube.merge(cube_list,"Down")
    # Cube.merge(cube_list,"Up")
    # print("OK")