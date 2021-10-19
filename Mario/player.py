from pico2d import *

WIDTH, HEIGHT = 1280, 1024


class Mario:
    def __init__(self):
        self.image = load_image('idle\idle.png')
        self.x = 100
        self.rx = self.x
        self.y = 200
        self.frame = 0
        self.dir = 0
        self.preDir = self.dir
    def update(self):
        global direction
        global growth
        global n
        if growth == 0:
            if self.dir == 1 or self.dir == -1:
                if n < 2:
                    n += 1
                    if self.dir == 1:
                        self.image = load_image('walk\walk1.png')
                    elif self.dir == -1:
                        self.image = load_image('walk\walkL1.png')
                elif n >= 2:
                    n = 1
                    if self.dir == 1:
                        self.image = load_image('walk\walk2.png')
                    elif self.dir == -1:
                        self.image = load_image('walk\walkL2.png')
                if (self.x >= 1280 // 2):
                    self.rx += 15 * self.dir
                else:
                    self.x += 15 * self.dir
                    self.rx += 15 * self.dir
            elif self.dir == 0:
                if self.preDir == 1:
                    self.image = load_image('idle\idle.png')
                elif self.preDir == -1:
                    self.image = load_image('idle\idleL.png')
            if direction == 1:
                global m
                global jumpCount
                jumpSize = 10
                if m < 2:
                    if self.dir == 1:
                        self.image = load_image('jump\jump1.png')
                    elif self.dir == -1:
                        self.image = load_image('jump\jumpL1.png')
                    jumpCount += 1
                    self.y += jumpSize
                    if jumpCount >= 15:
                        m += 1
                elif m >= 2:
                    if self.dir == 1:
                        self.image = load_image('jump\jump2.png')
                    elif self.dir == -1:
                        self.image = load_image('jump\jumpL2.png')
                    jumpCount -= 1
                    self.y -= jumpSize
                    if jumpCount == 0:
                        m = 1
                        direction = 0

        elif growth == 1:
            global growSize
            growSize += 20
            if growSize >= 120:
                self.image = load_image('idle\idle_big.png')
                growth = 2


        elif growth == 2:
            if self.dir == 1 or self.dir == -1:
                if n == 1:
                    n += 1
                    if self.dir == 1:
                        self.image = load_image('walk\walk1_big.png')
                    elif self.dir == -1:
                        self.image = load_image('walk\walkL1_big.png')
                elif n == 2:
                    n += 1
                    if self.dir == 1:
                        self.image = load_image('walk\walk2_big.png')
                    elif self.dir == -1:
                        self.image = load_image('walk\walkL2_big.png')
                elif n == 3:
                    n = 1
                    if self.dir == 1:
                        self.image = load_image('walk\walk3_big.png')
                    elif self.dir == -1:
                        self.image = load_image('walk\walkL3_big.png')
                if (self.x > 1280 // 2):
                    self.rx += 15 * self.dir
                else:
                    self.x += 15 * self.dir
                    self.rx += 15 * self.dir
            elif self.dir == 0:
                if self.preDir == 1:
                    self.image = load_image('idle\idle_big.png')
                elif self.preDir == -1:
                    self.image = load_image('idle\idleL_big.png')
            if direction == 1:
                # global m
                # global jumpCount
                jumpSize = 10
                if m < 2:
                    if self.dir == 1:
                        self.image = load_image('jump\jump1_big.png')
                    elif self.dir == -1:
                        self.image = load_image('jump\jumpL1_big.png')
                    jumpCount += 1
                    self.y += jumpSize
                    if jumpCount >= 15:
                        m += 1
                elif m >= 2:
                    if self.dir == 1:
                        self.image = load_image('jump\jump2_big.png')
                    elif self.dir == -1:
                        self.image = load_image('jump\jumpL2_big.png')
                    jumpCount -= 1
                    self.y -= jumpSize
                    if jumpCount == 0:
                        m = 1
                        direction = 0

        elif growth == 3:
            # global growSize
            growSize += 20
            if growSize >= 120:
                self.image = load_image('idle\idle_fire.png')
                growth = 4

        elif growth == 4:
            global firemotion
            global firecount
            if self.dir == 1 or self.dir == -1:
                if n == 1:
                    n += 1
                    if self.dir == 1:
                        self.image = load_image('walk\walk1_fire.png')
                    elif self.dir == -1:
                        self.image = load_image('walk\walkL1_fire.png')
                elif n == 2:
                    n += 1
                    if self.dir == 1:
                        self.image = load_image('walk\walk2_fire.png')
                    elif self.dir == -1:
                        self.image = load_image('walk\walkL2_fire.png')
                elif n == 3:
                    n = 1
                    if self.dir == 1:
                        self.image = load_image('walk\walk3_fire.png')
                    elif self.dir == -1:
                        self.image = load_image('walk\walkL3_fire.png')
                if (self.x > 1280 // 2):
                    self.rx += 15 * self.dir
                else:
                    self.x += 15 * self.dir
                    self.rx += 15 * self.dir
            elif self.dir == 0:
                if self.preDir == 1:
                    self.image = load_image('idle\idle_fire.png')
                elif self.preDir == -1:
                    self.image = load_image('idle\idleL_fire.png')
            if direction == 1:
                # global m
                # global jumpCount
                jumpSize = 10
                if m < 2:
                    if self.dir == 1:
                        self.image = load_image('jump\jump1_fire.png')
                    elif self.dir == -1:
                        self.image = load_image('jump\jumpL1_fire.png')
                    jumpCount += 1
                    self.y += jumpSize
                    if jumpCount >= 15:
                        m += 1
                elif m >= 2:
                    if self.dir == 1:
                        self.image = load_image('jump\jump2_fire.png')
                    elif self.dir == -1:
                        self.image = load_image('jump\jumpL2_fire.png')
                    jumpCount -= 1
                    self.y -= jumpSize
                    if jumpCount == 0:
                        m = 1
                        direction = 0

            if firemotion == 1:
                firecount += 1
                if self.preDir == 1:
                    self.image = load_image('attack\\attack_fire.png')
                elif self.preDir == -1:
                    self.image = load_image('attack\\attackL_fire.png')
                if firecount >= 5:
                    firecount = 0
                    firemotion = 0


    def draw(self):
        global growth
        global growSize
        if growth == 1:
            self.image.clip_draw(self.frame, 0, 32, 32, self.x, self.y + growSize / 2, 120 , 120 + growSize)
        else:
            self.image.clip_draw(self.frame, 0, 32, 32, self.x, self.y,120,120)
        # self.image.draw

class Map:
    def __init__(self):
        self.image = load_image('map\mapsize.png')
        self.x = 0
    def update(self):
        global player
        if(player.rx <= 1280 // 2):
            self.image.draw(13721 // 2, HEIGHT // 2)
        else:
            self.image.draw(13721 // 2 - (player.rx - 1280 // 2), HEIGHT // 2)

class FireBall:
    def __init__(self):
        self.image = load_image('map\mapsize.png')
        self.x = 0
    def update(self):
        global player
        if(player.rx <= 1280 // 2):
            self.image.draw(13721 // 2, HEIGHT // 2)
        else:
            self.image.draw(13721 // 2 - (player.rx - 1280 // 2), HEIGHT // 2)



def handle_events():
    global running
    global player
    global direction
    global growth
    global firemotion
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                player.preDir = player.dir
                player.dir += 1
            elif event.key == SDLK_LEFT:
                player.preDir = player.dir
                player.dir -= 1
            elif event.key == SDLK_UP:
                player.preDir = player.dir
                direction = 1
            elif event.key == SDLK_DOWN:
                if growth == 0:
                    growth = 1
                elif growth == 2:
                    growth = 3
            elif event.key == SDLK_f:
                firemotion = 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                player.preDir = player.dir
                player.dir -= 1
            elif event.key == SDLK_LEFT:
                player.preDir = player.dir
                player.dir += 1



k = 'walk'
n = 1
m = 1
direction = 0
jumpCount = 0;
growth = 0
growSize = 0
firemotion = 0
firecount = 0
open_canvas(WIDTH, HEIGHT)

background = Map()


running = True
player = Mario()

while running:
    handle_events()
    player.update()
    clear_canvas()
    background.update()
    player.draw()
    update_canvas()

    delay(0.03)