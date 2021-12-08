import game_framework
from pico2d import *
import main_state
import main_state2
import server

name = "ReadyState"
image = None
state_number = None
state_roundnumber = None
life_number = None
logo_time = 0.0


def enter():
    global image, state_number, state_roundnumber, life_number
    image = load_image('res\state\\ready_state.png')
    state_number = load_image('res\state\\Number.png')
    state_roundnumber = load_image('res\state\\Number.png')
    life_number = load_image('res\state\\Number.png')


def exit():
    global image
    del(image)


def handle_events():
    pass


def draw():
    clear_canvas()
    image.clip_draw(0, 0, 256, 240, 400, 300, 800, 600)
    state_number.clip_draw(9 * server.number_state, 0, 9, 8, 490, 528, 27, 20)
    state_number.clip_draw(9 * server.number_state, 0, 9, 8, 438, 388, 27, 20)
    state_roundnumber.clip_draw(9 * server.roundnumber_state, 0, 9, 8, 540, 528, 27, 20)
    state_roundnumber.clip_draw(9 * server.roundnumber_state, 0, 9, 8, 490, 388, 27, 20)
    life_number.clip_draw(9 * server.life, 0, 9, 8, 466, 310, 27, 20)
    update_canvas()






def update():
    global logo_time
    if (logo_time > 1.0):
        logo_time = 0
        # game_framework.quit()
        if server.roundnumber_state == 1:
            game_framework.change_state(main_state2)
        elif server.roundnumber_state == 2:
            game_framework.change_state(main_state)
    delay(0.01)
    logo_time += 0.01


def pause():
    pass


def resume():
    pass






