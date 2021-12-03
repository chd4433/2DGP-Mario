from pico2d import *
import game_framework

class goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.MovingX = 0
        self.image = load_image('res\map\element\goal.png')

    def draw(self):
        self.image.clip_draw(0,0,160,176,self.x - self.MovingX,self.y,600,500)
        draw_rectangle(*self.get_bb())

    def set_movingX(self, X):
        self.MovingX = X

    def update(self):
        pass

    def get_bb(self):
        return self.x - self.MovingX - 300, self.y - 250 , self.x - self.MovingX + 300, self.y + 450