from pico2d import *
import game_world
import game_framework

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2


class Ball:
    image = None
    imagelist = []
    def __init__(self, x = 400, y = 300, velocity = 1):
        if Ball.image == None:
            for i in range(4):
                Ball.imagelist.append(load_image('res\\fire\\fire%d.png' % i))
            Ball.image = load_image('res\\fire\\fire0.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.MovingX = 0
        self.frame = 0

    def draw(self):
        if int(self.frame) == 0:
            self.image = Ball.imagelist[0]
        elif int(self.frame) == 1:
            self.image = Ball.imagelist[1]
        elif int(self.frame) == 2:
            self.image = Ball.imagelist[2]
        elif int(self.frame) == 3:
            self.image = Ball.imagelist[3]
        self.image.clip_draw(0, 0, 8, 8, self.x, self.y, 16, 16)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.velocity
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if self.x < 0 or self.x > 800:
            game_world.remove_object(self)

    def set_movingX(self, X):
        self.MovingX = X

    def get_bb(self):
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8