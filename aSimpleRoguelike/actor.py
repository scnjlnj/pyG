import random
from collections import defaultdict

from controller import BaseController, KeyBoardController
from skills import *

class BaseActor(object):
    _controller=None
    h=None
    v=None
    mesh=None
    speed_h=0
    speed_v=0
    skills_ctrcode_map = {
        "U" : MoveUp,
        "D" : MoveDown,
        "L" : MoveLeft,
        "R" : MoveRight,
    }
    event_ctrcode_map = {
        87:"U",
        83:"D",
        65:"L",
        68:"R"
    }
    casting = set()
    def __init__(self,controller):
        self._controller=controller
        self.mesh = chr(ord("a")+random.randint(0,25))
        self.casting= set()
    def update_action(self):
        ctr:BaseController = self._controller

        for e in set(ctr.get_events_and_reset_queue()):
            if e[0] in self.event_ctrcode_map:
                skl = self.skills_ctrcode_map[self.event_ctrcode_map[e[0]]]
            else:continue
            if e[1] == 1 and skl not in self.casting:
                self.casting.add(skl)
            elif e[1] == -1 and skl in self.casting:
                self.casting.remove(skl)
        for sks in Conflicts:
            cnt=0
            for sk in sks:
                if sk in self.casting:cnt+=1
            if cnt>1:
                self.casting -= set(sks)

if __name__ == '__main__':
    kbctr = KeyBoardController()
    actor = BaseActor(controller = kbctr)
    actor.update_action()