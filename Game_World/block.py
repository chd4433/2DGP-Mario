

class Block():
    def __init__(self, x, y, type, collision):
        self.x = x
        self.y = y
        self.type = type
        self.collision = collision
        self.MovingX = 0

    def get_bb(self):
        return self.x - self.MovingX, self.y , self.x - self.MovingX+ 60, self.y + 60