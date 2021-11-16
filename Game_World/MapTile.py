from pico2d import *
import re
from block import Block
from boy import Boy



class MapTile:
    def __init__(self):
        self.MovingX = 0
        for i in range(53):
            blocklist.append(load_image('./res/map/block/b%d.png' % i))
        Load_Map("map1.py")

    def update(self):
        pass

    def draw(self):
        draw_block(self.MovingX)

    def set_movingX(self, X):
        self.MovingX = X


def Load_Map(NAME):
    fr = open(NAME, 'r')
    line = fr.readline()
    while line:
        line = fr.readline()
        vars = re.findall(r'\d+', line)
        if vars == []:
            pass
        else:
            Tilelist.append(Block(int(vars[0]), int(vars[1]), int(vars[2]), int(vars[3])))

def draw_block(MovingX):
    for i in range(len(Tilelist)):
        blocklist[Tilelist[i].type].clip_draw(0, 0, 16, 16, Tilelist[i].x + 30 - MovingX, Tilelist[i].y + 30, 60, 60)


Tilelist = list()
blocklist = []
