from pico2d import *
from block import Block

MapWidth, MapHeight = 1560, 600

open_canvas(MapWidth, MapHeight)


Tilelist = list()
blocklist = []
blockType = 0
for i in range(51):
    blocklist.append(load_image('./res/map/block/b%d.png' % i))
# Tilelist.append(Block(mouseX, mouseY, blockType, False))
def hadle_events():
    global Tilelist
    global blockType
    global running
    global mouseX
    global mouseY
    global MovingX
    global MovingY
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_q:
                blockType += 1
            elif event.key == SDLK_w:
                blockType -= 1
            if event.key == SDLK_RIGHT:
                MovingX += 10
            elif event.key == SDLK_LEFT:
                MovingX -= 10
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                mouseX, mouseY = event.x//60 * 60, (MapHeight - 1 - event.y)//60 * 60
                Tilelist.append(Block(mouseX + MovingX, mouseY + MovingY, blockType, False))
                # draw_block(16 * x, 16 * y, blockType)







def draw_block(x, y, type):
    for i in range(len(Tilelist)):
        blocklist[Tilelist[i].type].clip_draw(0, 0, 16, 16, Tilelist[i].x + 30 - MovingX, Tilelist[i].y + 30, 60, 60)

image = load_image('./res/map/block/b0.png')
running = True
mouseX = 500
mouseY = 500
MovingX = 0
MovingY = 0

while(running):
    clear_canvas()
    draw_block(mouseX, mouseY, blockType)
    update_canvas()
    hadle_events()
    delay(0.01)
close_canvas()