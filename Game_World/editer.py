from pico2d import *
from block import Block

MapWidth, MapHeight = 1024, 768

open_canvas(MapWidth, MapHeight)

blocklist = []
blockType = 0
for i in range(51):
    blocklist.append(load_image('./res/map/block/b%d.png' % i))
def hadle_events():
    global blockType
    global running
    global mouseX
    global mouseY
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_1:
                blockType = 1
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT:
                mouseX, mouseY = event.x//16 * 16, (MapHeight - 1 - event.y)//16 * 16
                # draw_block(16 * x, 16 * y, blockType)







def draw_block(x, y, type):
    blocklist[type].clip_draw(0, 0, 16, 16, x, y)

image = load_image('./res/map/block/b0.png')
running = True
mouseX = 500
mouseY = 500


while(running):
    clear_canvas()
    draw_block(mouseX, mouseY, blockType)
    update_canvas()
    hadle_events()
    delay(0.01)
close_canvas()