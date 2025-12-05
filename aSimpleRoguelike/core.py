import logging
import os
import time
from copy import deepcopy

from actor import BaseActor
from controller import KeyBoardController

from CONSTANTS import *
from resources.image import actor_base_image
from utills import get_random_color_pg_surface


def dev_show(output):
    for row in output:
        print("   ".join(row))


class World(object):
    data=[]
    def __init__(self,screen_rect,kbctr):
        # Initialize pygame
        if pg.get_sdl_version()[0] == 2:
            pg.mixer.pre_init(44100, 32, 2, 1024)
        pg.init()
        if pg.mixer and not pg.mixer.get_init():
            print("Warning, no sound")
            pg.mixer = None

        # Set the display mode
        winstyle = 0  # |FULLSCREEN
        bestdepth = pg.display.mode_ok(screen_rect.size, winstyle, 32)
        self.screen = pg.display.set_mode(screen_rect.size, winstyle, bestdepth)

        # decorate the game window
        icon = pg.transform.scale(actor_base_image, (32, 32))
        pg.display.set_icon(icon)
        pg.display.set_caption("Testtinggg")
        pg.mouse.set_visible(1)

        # create the background, tile the bgd image
        background = pg.Surface(screen_rect.size)
        background.fill([255, 255, 255])
        self.screen.blit(background, (0, 0))
        pg.display.flip()
        self.sprites = pg.sprite.Group()
        self.all = pg.sprite.RenderUpdates()
        BaseActor.containers = self.all,self.sprites
        # screen.blit(background, (0, 0))
        self.frame = 0
        self.actors = [BaseActor(kbctr,get_random_color_pg_surface([1,1]),system=True)]
        self.objs = []
    @property
    def current_bg(self):
        background = pg.Surface(screen_rect.size)
        background.fill([255, 255, 255])
        return background
    @property
    def end_flag(self):
        return self.actors[0]._controller.exit_flag

    def step_by(self):
        self.frame +=1
        for actor in self.actors:
            if actor.system:
                continue
            actor.update_action()
        for actor in self.actors:
            if actor.system:
                continue
            actor.step_by()

        return True

    def show(self):
        self.all.clear(self.screen,self.current_bg)
        dirty = self.all.draw(self.screen)
        pg.display.update(dirty)


    def add_actor(self, pos_h,pos_v, actor):
        actor.rect.update(pos_h,pos_v,*actor.rect.size)

        self.actors.append(actor)

# def get_user_action():
#     act = input("input action:\n")
#     return UserAction(act)



