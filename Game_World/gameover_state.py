import game_framework
from pico2d import *
import server

name = "ReadyState"
image = None
state_number = None
state_roundnumber = None

logo_time = 0.0


def enter():
    global image, state_number, state_roundnumber
    image = load_image('res\state\\GameOver.png')
    state_number = load_image('res\state\\Number.png')
    state_roundnumber = load_image('res\state\\Number.png')



def exit():
    global image
    del(image)


def handle_events():
    pass


def draw():
    clear_canvas()
    image.clip_draw(0, 0, 256, 240, 400, 300, 800, 600)
    state_number.clip_draw(9 * server.number_state, 0, 9, 8, 490, 528, 27, 20)
    state_roundnumber.clip_draw(9 * server.roundnumber_state, 0, 9, 8, 540, 528, 27, 20)
    update_canvas()






def update():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.quit()



def pause():
    pass


def resume():
    pass






