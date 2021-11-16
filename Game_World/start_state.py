import game_framework
from pico2d import *
import ready_state

name = "StartState"
start_image = None
image = None
image2 = None
logo_time = 0.0
MapHeight = 600

def enter():
    global image, image2, start_image
    start_image = load_image('res\state\start_state.png')
    image = load_image('res\state\start_state.png')
    image2 = load_image('res\state\start_state_1.png')


def exit():
    global image
    del(image)


def update():
    pass

def draw():
        global start_image
        clear_canvas()
        start_image.clip_draw(0, 0, 256, 240, 400, 300, 800, 600)
        update_canvas()





def handle_events():
    global image, image2, start_image
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEMOTION:
            mouseX, mouseY = event.x , MapHeight - 1 - event.y
            if mouseX >= 260 and mouseX <= 600:
                if mouseY >= 200 and mouseY<= 250:
                    start_image = image2
                else: start_image = image
            else: start_image = image
        if event.type == SDL_MOUSEBUTTONDOWN:
            mouseX, mouseY = event.x, MapHeight - 1 - event.y
            if mouseX >= 260 and mouseX <= 600:
                if mouseY >= 200 and mouseY<= 250:
                    if event.button == SDL_BUTTON_LEFT:
                        game_framework.change_state(ready_state)
        if event.type == SDL_QUIT:
            game_framework.quit()




def pause(): pass


def resume(): pass




