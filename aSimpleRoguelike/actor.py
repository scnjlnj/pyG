import random
import pygame as pg
from pygame.sprite import Sprite

from CONSTANTS import TPF, ACTOR_RECT, SCREENRECT
from controller import BaseController, KeyBoardController
from resources.image import actor_base_image
from skills import *

class System(Sprite):
    pass

class BaseActor(Sprite):
    _controller=None
    mesh=None
    speed_h=0
    speed_v=0
    MAX_SPEED = 50
    skills_ctrcode_map = {
        ("U",1) : MoveUp,
        ("U",-1) : MoveUpEnd,
        ("D",1) : MoveDown,
        ("D",-1) : MoveDownEnd,
        ("L",1) : MoveLeft,
        ("L",-1) : MoveLeftEnd,
        ("R",1) : MoveRight,
        ("R",-1) : MoveRightEnd,
    }
    event_ctrcode_map = {
        87:"U",
        83:"D",
        65:"L",
        68:"R"
    }
    casting = set()
    def __init__(self,controller,mesh,frame=0,system=False):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.rect = mesh.get_rect(midbottom=SCREENRECT.midbottom)
        self.origtop = self.rect.top
        self._controller=controller
        self.image = mesh
        self.casting= set()
        self.system=system
        self.frame = frame
    def update_action(self):
        ctr:BaseController = self._controller
        for e in ctr.get_events_and_reset_queue():
            vk, action = e
            if vk in self.event_ctrcode_map:
                skl = self.skills_ctrcode_map[(self.event_ctrcode_map[vk],action)]
            elif vk == "Key.esc":
                self._controller.exit_flag=True
                continue
            else:continue
            self.load_skill(skl)
        print(self.rect)
    def load_skill(self, s):
        s.load(self)
        if not s.load_only:
            self.casting.add(s)
    def step_by(self):
        self.rect.move_ip(self.speed_h*TPF, self.speed_v*TPF)
        self.rect = self.rect.clamp(SCREENRECT)
        self.frame+=1
