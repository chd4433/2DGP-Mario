import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from grass import Grass
from MapTile import MapTile
from Mob import Gomba, Turtle
from ball import Ball



name = "MainState"

boy = None
mapTile = None
Mob_Gomba = None
Mob_Tuttle = None
# mapTile = MapTile()
# boy = Boy()
def enter():
    global boy
    global mapTile
    global Mob_Gomba, Mob_Tuttle
    boy = Boy()
    # grass = Grass()
    mapTile = MapTile()
    Mob_Gomba = Gomba()
    Mob_Tuttle = Turtle()
    game_world.add_object(mapTile, 0)
    game_world.add_object(boy, 1)
    game_world.add_object(Mob_Gomba, 2)
    game_world.add_object(Mob_Tuttle, 2)




def exit():
    global boy, mapTile, Mob_Gomba, Mob_Tuttle
    del boy
    del mapTile
    del Mob_Gomba

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            boy.handle_event(event)


def update():
    global boy, mapTile, Mob_Gomba, Mob_Tuttle
    mapTile.set_movingX(boy.getX())
    Mob_Gomba.set_movingX(boy.getX())
    Mob_Tuttle.set_movingX(boy.getX())
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()







