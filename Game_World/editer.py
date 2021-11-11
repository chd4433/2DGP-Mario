from pico2d import *

MapWidth, MapHeight = 1024, 768


def hadle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEBUTTONDOWN:
            if event.button == SDL_BUTTON_LEFT: