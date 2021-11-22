from pico2d import *
import re
from block import Block
from boy import Boy



class MapTile:

    def __init__(self):
        self.MovingX = 0
        self.Tilelist = list()
        self.blocklist = []
        for i in range(53):
            self.blocklist.append(load_image('./res/map/block/b%d.png' % i))
        self.Load_Map("map1.py")

    def update(self):
        pass

    def draw(self):
        self.draw_block(self.MovingX)

    def set_movingX(self, X):
        self.MovingX = X

    def get_bb(Tilelist):
        return Tilelist.x , Tilelist.y , Tilelist.x + 60, Tilelist.y + 60

    def Load_Map(self, NAME):
        fr = open(NAME, 'r')
        line = fr.readline()
        while line:
            line = fr.readline()
            vars = re.findall(r'\d+', line)
            if vars == []:
                pass
            else:
                self.Tilelist.append(Block(int(vars[0]), int(vars[1]), int(vars[2]), int(vars[3])))



    def draw_block(self, MovingX):
        for i in range(len(self.Tilelist)):
            self.blocklist[self.Tilelist[i].type].clip_draw(0, 0, 16, 16, self.Tilelist[i].x + 30 - MovingX, self.Tilelist[i].y + 30, 60, 60)
        # for i in self.Tilelist:
        #     draw_rectangle(*i.get_bb())



