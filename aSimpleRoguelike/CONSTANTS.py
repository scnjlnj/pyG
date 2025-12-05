import logging
import pygame as pg
logging.basicConfig(level=0)
logger =  logging.getLogger("main")
logger.info("starting")
clock = pg.time.Clock()

# Constants
MAX_FPS = 20
TPF = float("{:.2f}".format((1 / MAX_FPS)))
# Scenes

# game constants
SCREENRECT = pg.Rect(0, 0, 1000, 400)
ACTOR_RECT = pg.Rect(0, 0, 20, 20)