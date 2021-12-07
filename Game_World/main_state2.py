import random
import json
import os

from pico2d import *
import game_framework
import game_world

from boy import Boy
from grass import Grass
from boy import DeathState, GoalState
from MapTile import *
from Mob import Gomba, Turtle
from item import Mushroom, Flower
from block import Block
import collision
import server
from ball import Ball
import ready_state
import gameover_state
from goal import *

name = "MainState"

Moblist = list()
itemlist = list()
itemlist_Flower = list()
boy = None
mapTile = None
Mob_Gomba = None
Mob_Tuttle = None
destination = None
block = Block(0, 0, 0, 0)
bool_grabity = False

bool_all_tile = False
bool_all_tile2 = False
bool_jumpdown = True


# mapTile = MapTile()
# boy = Boy()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


def collideUpDown(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_b < left_a < right_b or left_b < right_a < right_b:
        if bottom_a < top_b:
            return True
        else:
            return False
    else:
        return False


def collideUpDown_false(a, b):
    global bool_all_tile
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_b < left_a < right_b or left_b < right_a < right_b:
        if bottom_a < top_b:
            bool_all_tile = True
        else:
            bool_all_tile = bool_all_tile or False
    else:
        bool_all_tile = bool_all_tile or False


def collidejump(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_b < left_a < right_b or left_b < right_a < right_b:
        if top_a > bottom_b:
            return True
        else:
            return False
    else:
        return False


def collide_left(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if bottom_b < top_a < top_b or bottom_b < bottom_b < top_b:
        if right_a > left_b:
            return True
        else:
            return False
    else:
        return False


def collide_leftright(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if bottom_b < top_a < top_b or bottom_b < bottom_a < top_b:
        if left_b < right_a < right_b or left_b < left_a < right_b:
            return True
        else:
            return False
    else:
        return False


def collide_all(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_b < right_a < right_b:
        return 1
    elif left_b < left_a < right_b:
        return 2
    elif bottom_b < bottom_a < top_b:
        return 3
    elif bottom_b < top_a < top_b:
        return 4


def collide_only_all(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if bottom_b <= top_a <= (top_b + bottom_b) / 2:
        if left_b <= left_a <= right_b:
            return 'top'
        if left_b <= right_a <= right_b:
            return 'top'
        if left_b >= left_a and right_a >= right_b:
            return 'top'

    if (top_b + bottom_b) / 2 <= bottom_a <= top_b:
        if left_b <= left_a <= right_b:
            return 'bottom'
        if left_b <= right_a <= right_b:
            return 'bottom'
        if left_b >= left_a and right_a >= right_b:
            return 'bottom'

    if (left_b + right_b) / 2 <= left_a <= right_b:
        if bottom_b <= top_a <= top_b:
            return 'left'
        if bottom_b <= bottom_a <= top_b:
            return 'left'
        if bottom_a <= top_b <= bottom_b:
            return 'left'
        if bottom_a <= bottom_b <= bottom_b:
            return 'left'

    if left_b <= right_a <= (left_b + right_b) / 2:
        if bottom_b <= top_a <= top_b:
            return 'right'
        if bottom_b <= bottom_a <= top_b:
            return 'right'
        if bottom_a <= top_b <= bottom_b:
            return 'right'
        if bottom_a <= bottom_b <= bottom_b:
            return 'right'


def enter():
    global boy
    global mapTile
    global Moblist, Mob_Gomba, Mob_Tuttle, destination
    boy = Boy()
    boy.MovingX = 0
    # grass = Grass()
    mapTile = MapTile('map2.py')
    Mob_Gomba = Gomba(800, 500, 0)
    Mob_Tuttle = Turtle(1500, 500, 0)
    # Moblist.append(Mob_Gomba)
    # Moblist.append(Gomba(1200, 500, 0))
    # Moblist.append(Gomba(1400, 500, 0))
    Moblist.append(Gomba(2700, 800))
    Moblist.append(Gomba(2400, 1500))
    Moblist.append(Gomba(1700, 500))
    Moblist.append(Gomba(3400, 2500))
    Moblist.append(Gomba(5000, 2500))
    Moblist.append(Turtle(5000, 2500))
    Moblist.append(Turtle(4500, 2500))
    Moblist.append(Turtle(500, 2500))
    Moblist.append(Turtle(5000, 1500))
    Moblist.append(Turtle(5000, 2500))
    Moblist.append(Mob_Tuttle)
    destination = goal(7200, 310)
    game_world.add_object(mapTile, 0)
    game_world.add_object(boy, 5)
    # game_world.add_object(Mob_Gomba, 2)
    # game_world.add_object(Mob_Tuttle, 2)
    for i in Moblist:
        game_world.add_object(i, 2)
    game_world.add_object(destination, 4)
    boy.get_maxtile(mapTile.maxtile_x)


def exit():
    global boy, mapTile, Moblist, itemlist, itemlist_Flower
    # del boy
    # del mapTile
    Moblist.clear()
    itemlist.clear()
    itemlist_Flower.clear()

    # for i in Moblist:
    #     Moblist.remove(i)
    game_world.clear()


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
            if boy.cur_state == DeathState or boy.cur_state == GoalState:
                pass
            else:
                boy.handle_event(event)


def update():
    global boy, mapTile, Mob_Gomba, Mob_Tuttle, bool_all_tile, bool_all_tile2, bool_jumpdown, Moblist, itemlist, itemlist_Flower, destination, bool_grabity

    for i in mapTile.Tilelist:
        i.MovingX = boy.getX()
    for i in itemlist:
        i.MovingX = boy.getX()
    for i in itemlist_Flower:
        i.MovingX = boy.getX()
    for i in game_world.select_object(3):
        i.MovingX = boy.getX()
    destination.set_movingX(boy.getX())
    mapTile.set_movingX(boy.getX())
    for i in Moblist:
        i.set_movingX(boy.getX())
        if i.x - 1000 <= boy.x + boy.MovingX:
            i.set_velocity(-1)
    # Mob_Gomba.set_movingX(boy.getX())
    # Mob_Tuttle.set_movingX(boy.getX())
    for game_object in game_world.all_objects():
        game_object.update()
    for i in mapTile.Tilelist:
        if i.collision >= 1:
            if collide(boy, i):
                if collide_only_all(boy, i) == "left":
                    print("left")
                    boy.before_movingx()
                elif collide_only_all(boy, i) == "right":
                    print("right")
                    boy.before_movingx()

                if i.y < boy.plagY < i.y + 10:
                    if collidejump(boy, i):
                        boy.y -= 5
                        boy.get_booljump(True)
                        bool_jumpdown = False
                        boy.get_grabity(False)
                        if i.collision == 1:
                            if boy.boolbig == True or boy.boolFlower == True:
                                mapTile.remove(i)
                        if i.collision == 2:
                            i.collision = 1  # 수정 해야함
                            i.type += 1
                            item_mushroom = Mushroom(i.x + 30, i.y + 30)
                            item_mushroom.MovingX = boy.getX()
                            itemlist.append(item_mushroom)
                            game_world.add_object(item_mushroom, 3)
                        if i.collision == 3:
                            i.collision = 1
                            i.type += 1
                            item_Flower = Flower(i.x + 30, i.y + 30)
                            item_Flower.MovingX = boy.getX()
                            itemlist_Flower.append(item_Flower)
                            game_world.add_object(item_Flower, 3)
                if collideUpDown(boy, i) and bool_jumpdown == True:
                    boy.get_grabity(True)
                collideUpDown_false(boy, i)
                if bool_all_tile == False:
                    boy.get_grabity(False)
                # if collide_left(boy, i):
                #     boy.get_bool_leftmove(True)
                #     boy.x -= 2
                bool_jumpdown = True
        else:
            collideUpDown_false(boy, i)
            if bool_all_tile == False:
                boy.get_grabity(False)
    for i in itemlist:
        if collide(boy, i):
            itemlist.remove(i)
            game_world.remove_object(i)
            boy.boolbig = True
    for i in itemlist_Flower:
        if collide(boy, i):
            itemlist_Flower.remove(i)
            game_world.remove_object(i)
            boy.boolFlower = True

    for j in Moblist:
        if boy.invincibility == False:
            if collide(boy, j):
                if collide_only_all(boy, j) == 'left' or collide_only_all(boy, j) == 'right':
                    boy.get_invincibility(True)
                    # print(j.mob_lifetime())
                    print('데미지')
                if collide_only_all(boy, j) == 'bottom':
                    print('밟기')
                    j.booldeath = True
        if j.deathtime >= 10:
            Moblist.remove(j)
            game_world.remove_object(j)

        for k in game_world.select_object(3):
            if collide(j, k):
                print('불맞음')
                j.booldeath = True
                game_world.remove_object(k)
        bool_grabity = False
        for i in mapTile.Tilelist:
            if i.collision >= 1:
                if collide(j, i):
                    if collide_only_all(j, i) == 'left':
                        j.change_velocity(True, 'left')
                    elif collide_only_all(j, i) == 'right':
                        j.change_velocity(True, 'right')
                    if collide_only_all(j, i) == 'bottom':
                        bool_grabity = True
        if bool_grabity:
            j.get_grabity(True)
        else:
            j.get_grabity(False)

    if boy.bgoal == False:
        if collide(boy, destination):
            boy.get_bool_goal(True)

    bool_all_tile = False

    if boy.death:
        server.life -= 1
        if server.life >= 0:
            game_framework.change_state(ready_state)
        else:
            game_framework.change_state(gameover_state)

    if boy.next_stage:
        game_framework.change_state(ready_state)
        server.roundnumber_state += 1


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()







