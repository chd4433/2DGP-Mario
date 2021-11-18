from pico2d import *
import game_framework


class Mushroom():
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('res\Map\icon\mushroom_layer.png')
        self.MovingX = 0
        self.dir = 1
        self.velocity = 1
        self.grabity = False
        self.grabity_check = False
        self.booldeath = False
        self.ani = 0

    def update(self):
        if self.ani <= 16:
            self.ani += 1
            self.y += 60/16
        else:
            pass
            # self.x += 0.3 * self.velocity
        # if self.grabity == False:
        #     self.y -= 0.5;

    def get_bb(self):
        return self.x - self.MovingX - 15, self.y - 15, self.x - self.MovingX + 15, self.y + 15

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
        self.image.clip_draw(0, 0, 16, self.ani, self.x - self.MovingX, self.y, 60, 60)
        draw_rectangle(*self.get_bb())


class Flower():
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('res\Map\icon\\flower_layer.png')
        self.MovingX = 0
        self.grabity = False
        self.grabity_check = False
        self.booldeath = False
        self.ani = 0

    def update(self):
        if self.ani <= 16:
            self.ani += 1
            self.y += 60/16
        else:
            pass


    def get_bb(self):
        return self.x - self.MovingX - 20, self.y - 20, self.x - self.MovingX + 20, self.y + 20


    def draw(self):
        self.image.clip_draw(0, 0, 16, self.ani, self.x - self.MovingX, self.y, 60, 60)
        draw_rectangle(*self.get_bb())
