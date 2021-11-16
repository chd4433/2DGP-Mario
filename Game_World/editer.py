from pico2d import *
from block import Block
import re

MapWidth, MapHeight = 800, 600

open_canvas(MapWidth, MapHeight)
FILE_NAME = "map1.py"
TEST = "Test.py"

Tilelist = list()
blocklist = []
blockType = 0
for i in range(53):
    blocklist.append(load_image('./res/map/block/b%d.png' % i))
# Tilelist.append(Block(mouseX, mouseY, blockType, False))

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



def hadle_events():
    global Tilelist
    global blockType
    global running
    global mouseX
    global mouseY
    global MovingX
    global MovingY
    global block_collision
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_q:
                blockType += 1
                if blockType > 52:
                    blockType = 0
            elif event.key == SDLK_w:
                blockType -= 1
                if blockType < 0:
                    blockType = 52
            if event.key == SDLK_RIGHT:
                MovingX += 120
            elif event.key == SDLK_LEFT:
                MovingX -= 120
            if event.key == SDLK_s:
                f = open(FILE_NAME, 'w')
                f.write("from block import Block\n")
                for i in range(len(Tilelist)):
                    f.write("Block(%d, %d, %d, %d),\n" % (Tilelist[i].x , Tilelist[i].y, Tilelist[i].type, Tilelist[i].collision))
                f.close()
            if event.key == SDLK_x:
                fill_allBlock()
            if event.key == SDLK_z:
                Load_Map(FILE_NAME)
            if event.key == SDLK_v:
                if block_collision == 0:
                    block_collision = 1
                    print("충돌 O")
                elif block_collision == 1:
                    block_collision = 0
                    print("충돌 x")
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                mouseX, mouseY = (event.x + MovingX)//60 * 60, ((MapHeight - 1 - event.y) + MovingY)//60 * 60
                Tilelist.append(Block(mouseX , mouseY, blockType, block_collision))
                # draw_block(16 * x, 16 * y, blockType)




def fill_allBlock():
    for i in range(MapHeight//60):
        for j in range(MapWidth//60):
            Tilelist.append(Block((j + MovingX//60) * 60, i * 60, blockType, 0))


def draw_block():
    for i in range(len(Tilelist)):
        blocklist[Tilelist[i].type].clip_draw(0, 0, 16, 16, Tilelist[i].x + 30 - MovingX, Tilelist[i].y + 30, 60, 60)

def display_currBlock():
    blocklist[blockType].clip_draw(0, 0, 16, 16, MapWidth - 16, MapHeight - 16, 32, 32)







# image = load_image('./res/map/block/b0.png')
running = True
mouseX = 500
mouseY = 500
MovingX = 0
MovingY = 0
block_collision = 0

while(running):
    clear_canvas()
    draw_block()
    display_currBlock()
    update_canvas()
    hadle_events()
    delay(0.01)
close_canvas()