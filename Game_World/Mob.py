from pico2d import *
import game_framework
import game_world

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2



class Gomba():
    def __init__(self):
        self.x, self.y = 700, 200
        self.image = load_image('res\Mob\gomba_1.png')
        self.dir = -1
        self.velocity = -1
        self.frame = 0
        self.MovingX = 0
        self.grabity = False
        self.grabity_check = False
        self.booldeath = False
        self.deathtime = 0

    def update(self):
        self.x += 0.3 * self.velocity
        if self.grabity == False:
            self.y -= 0.5;
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        if self.frame >= 2:
            self.frame = 0
        if self.booldeath:
            self.frame = 2
            self.deathtime += 1

    def set_movingX(self, X):
        self.MovingX = X

    def get_bb(self):
        return self.x - self.MovingX - 20, self.y - 25, self.x - self.MovingX + 20, self.y + 25

    def get_grabity(self, check):
        self.grabity = check

    def get_grabitycheck(self, check):
        self.grabity_check = self.grabity_check and check

    def set_grabitycheck(self):
        return self.grabity_check



    def collideUpDown_false(self, a, b):
        left_a, bottom_a, right_a, top_a = a.get_bb()
        left_b, bottom_b, right_b, top_b = b.get_bb()
        if left_b < left_a < right_b or left_b < right_a < right_b:
            if bottom_a < top_b:
                self.grabity_check = True
            else:
                self.grabity_check = self.grabity_check or False
        else:
            self.grabity_check = self.grabity_check or False

    def draw(self):
        self.image.clip_draw(int(self.frame) * 42, 0 ,42, 33, self.x - self.MovingX, self.y, 60, 60)
        draw_rectangle(*self.get_bb())


class Turtle():
    def __init__(self):
        self.x, self.y = 900, 200
        self.image = load_image('res\Mob\Turtle_1.png')
        self.dir = -1
        self.velocity = -1
        self.frame = 0
        self.MovingX = 0
        self.grabity = False
        self.grabity_check = False
        self.booldeath = False
        self.deathtime = 0

    def update(self):
        self.x += 0.3 * self.velocity
        if self.grabity == False:
            self.y -= 0.5;
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        if self.frame >= 2:
            self.frame = 0
        if self.booldeath:
            self.frame = 5
            self.deathtime += 1

    def set_movingX(self, X):
        self.MovingX = X

    def get_bb(self):
        return self.x - self.MovingX - 25, self.y - 30, self.x - self.MovingX + 25, self.y + 30

    def get_grabity(self, check):
        self.grabity = check

    def get_grabitycheck(self, check):
        self.grabity_check = self.grabity_check and check

    def set_grabitycheck(self):
        return self.grabity_check

    def collideUpDown_false(self, a, b):
        left_a, bottom_a, right_a, top_a = a.get_bb()
        left_b, bottom_b, right_b, top_b = b.get_bb()
        if left_b < left_a < right_b or left_b < right_a < right_b:
            if bottom_a < top_b:
                self.grabity_check = True
            else:
                self.grabity_check = self.grabity_check or False
        else:
            self.grabity_check = self.grabity_check or False

    def draw(self):
        self.image.clip_draw(int(self.frame) * 59, 0 ,59, 64, self.x - self.MovingX, self.y, 80, 80)
        draw_rectangle(*self.get_bb())