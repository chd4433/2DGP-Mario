import game_framework
from pico2d import *
import server

name = "ReadyState"
image = None
state_number = None
state_roundnumber = None

logo_time = 0.0


End_sound = None


def enter():
    global image, state_number, state_roundnumber, End_sound
    image = load_image('res\state\\End_state1.png')
    End_sound = load_music('res\sound\Ending.mp3')
    End_sound.set_volume(32)
    End_sound.repeat_play()




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






