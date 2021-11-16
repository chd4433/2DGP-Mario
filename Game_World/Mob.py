from pico2d import *
import game_framework
import game_world

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2



class Gomba():
    def __init__(self):
        self.x, self.y = 800, 90
        self.image = load_image('res\Mob\gomba_1.png')
        self.dir = -1
        self.velocity = -1
        self.frame = 0
        self.MovingX = 0

    def update(self):
        self.x += 0.3 * self.velocity
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        if self.frame >= 2:
            self.frame = 0

    def set_movingX(self, X):
        self.MovingX = X

    def draw(self):
        global MovingX
        self.image.clip_draw(int(self.frame) * 42, 0 ,42, 33, self.x - self.MovingX, self.y, 60, 60)


class Turtle():
    def __init__(self):
        self.x, self.y = 1000, 90
        self.image = load_image('res\Mob\Turtle_1.png')
        self.dir = -1
        self.velocity = -1
        self.frame = 0
        self.MovingX = 0

    def update(self):
        self.x += 0.3 * self.velocity
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        if self.frame >= 2:
            self.frame = 0

    def set_movingX(self, X):
        self.MovingX = X

    def draw(self):
        self.image.clip_draw(int(self.frame) * 59, 0 ,59, 64, self.x - self.MovingX, self.y, 80, 80)