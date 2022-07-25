import logging
import os

from actor import BaseActor
from controller import KeyBoardController

logging.basicConfig(level=0)
logger =  logging.getLogger("main")
logger.info("starting")

# Scenes

class World(object):
    data=[]
    def __init__(self,size_h,size_v):
        self.static_data = [['.']*size_h]*(size_v-1)+["_"]*size_h
        self.actors = []
        self.objs = []

    def step_by(self,user_action):
        self.data.append(user_action.action)
        return True

    def show(self):
        os.system("clear")
        output = self.static_data
        for actor in self.actors:
            self.render_actor(actor)
        # self.deal_light()
        print(f"showWorld:{self.output}")
        # `cls` for windows
        # os.system("cls")

    def get_events(self):
        pass

    def add_actor(self, pos_h,pos_v, actor):
        actor.h = pos_h
        actor.v = pos_v
        self.actors.append(actor)

    def render_actor(self,board, actor:BaseActor):
        h,v = actor.h,actor.v
        board[v][h] = actor.mesh

# def get_user_action():
#     act = input("input action:\n")
#     return UserAction(act)




def main():
    world = World(30,50)
    kbctr = KeyBoardController()
    actor = BaseActor(controller = kbctr)
    world.add_actor(10,10,actor)
    while 1:
        events = world.get_events()
        if action.over_flag:
            break
        changed = world.step_by(events = events)
        if changed:
            world.show()
    logger.info("over")
    logger.info("exiting")


if __name__ == '__main__':
    main()