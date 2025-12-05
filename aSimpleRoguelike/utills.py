import pygame as pg
import random


def get_pg_surface(size, color) -> pg.Surface:
    image = pg.Surface(size)
    image.fill(color)
    return image

def get_random_color_pg_surface(size):
    return get_pg_surface(size,[random.randint(0,255),random.randint(0,255),random.randint(0,255)])