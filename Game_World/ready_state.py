import game_framework
from pico2d import *
import main_state

name = "ReadyState"
image = None
logo_time = 0.0

def enter():
    global image
    image = load_image('res\state\\ready_state.png')


def exit():
    global image
    del(image)


def handle_events():
    pass


def draw():
    clear_canvas()
    image.clip_draw(0, 0, 256, 240, 400, 300, 800, 600)
    update_canvas()






def update():
    global logo_time
    if (logo_time > 1.0):
        logo_time = 0
        # game_framework.quit()
        game_framework.change_state(main_state)
    delay(0.01)
    logo_time += 0.01


def pause():
    pass


def resume():
    pass






