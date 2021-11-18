from pico2d import *
import game_world
from ball import Ball
import game_framework

history = []

idle = []

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

TIME_PER_ACTION_RUN = 0.3
ACTION_PER_TIME_RUN = 1.0 / TIME_PER_ACTION_RUN

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_DOWN, SHIFT_UP, DASH_TIMER, DEBUG_KEY, FIRE_KEY, SPACE, JUMP_TIMER1, JUMP_TIMER2, TRANS_BIG, TRANS_FIRE = range(14)

event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'SHIFT_DOWN', 'SHIFT_UP', 'DASH_TIMER', 'DEBUG_KEY', 'FIRE_KEY', 'SPACE', 'JUMP_TIMER1', 'JUMP_TIMER2', 'TRANS_BIG', 'TRANS_FIRE']

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_c): FIRE_KEY,
    (SDL_KEYDOWN, SDLK_v): DEBUG_KEY,

    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYDOWN, SDLK_RSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYUP, SDLK_RSHIFT): SHIFT_UP,


    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP
}


# Boy States

class IdleState:

    def enter(boy, event):
        if event == RIGHT_DOWN and boy.bool_leftmove == False:
            boy.velocity += 1
        elif event == LEFT_DOWN and boy.bool_rightmove == False:
            boy.velocity -= 1
        elif event == RIGHT_UP and boy.bool_leftmove == False:
            boy.velocity -= 1
        elif event == LEFT_UP and boy.bool_rightmove == False:
            boy.velocity += 1
        boy.timer = 1000

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        if boy.grabity == False:
            boy.y -= 2;
        if boy.boolbig:
            boy.add_event(TRANS_BIG)
    def draw(boy):
        if boy.dir == 1:
            boy.image = idle[0]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            boy.image = idle[1]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class WalkState:

    def enter(boy, event):
        if event == RIGHT_DOWN and boy.bool_leftmove == False:
            boy.velocity += 1
        elif event == LEFT_DOWN and boy.bool_rightmove == False:
            boy.velocity -= 1
        elif event == RIGHT_UP and boy.bool_leftmove == False:
            boy.velocity -= 1
        elif event == LEFT_UP and boy.bool_rightmove == False:
            boy.velocity += 1
        boy.dir = boy.velocity
        boy.timer = 1000

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        # boy.x += 0.5 * boy.velocity
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            boy.MovingX += boy.velocity
        boy.x = clamp(25, boy.x, 1600 - 25)
        if boy.grabity == False:
            boy.y -= 2;
        if boy.timer <= 750:
            boy.add_event(DASH_TIMER)
        if boy.boolbig:
            boy.add_event(TRANS_BIG)

    def draw(boy):
        if boy.velocity == 1:
            if int(boy.frame) == 0:
                boy.image = load_image('res\walk\walk1.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\walk\walk2.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = load_image('res\walk\walkL1.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\walk\walkL2.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)

class RunState:

    def enter(boy, event):
        boy.timer = 1000
        boy.dir = boy.velocity

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME_RUN * game_framework.frame_time) % 2
        boy.timer -= 1
        # boy.x += boy.velocity
        if boy.grabity == False:
            boy.y -= 2;
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            boy.MovingX += 2 * boy.velocity
        if boy.boolbig:
            boy.add_event(TRANS_BIG)
        boy.x = clamp(25, boy.x, 1600 - 25)

    def draw(boy):
        if boy.velocity == 1:
            if int(boy.frame) == 0:
                boy.image = load_image('res\\run\\run1.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\\run\\run2.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = load_image('res\\run\\runL1.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\\run\\runL2.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class JumpState:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += 1
        elif event == LEFT_DOWN:
            boy.velocity -= 1
        elif event == RIGHT_UP:
            boy.velocity -= 1
        elif event == LEFT_UP:
            boy.velocity += 1
        boy.dir = boy.velocity


    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        # boy.x += boy.dir
        boy.MovingX += boy.dir

        if boy.timer >= 800 and boy.booljump == False:
            boy.y += 2
        else:
            if boy.grabity == False:
                boy.y -= 2;
            else:
                boy.booljump = False
                if boy.dir == 0:
                    boy.add_event(JUMP_TIMER2)
                else:
                    boy.add_event(JUMP_TIMER1)
        if boy.boolbig:
            boy.add_event(TRANS_BIG)



        boy.x = clamp(25, boy.x, 1600 - 25)

    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = load_image('res\jump\jump1.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\jump\jump2.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = load_image('res\jump\jumpL1.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\jump\jumpL2.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class IdleState_Big:

    def enter(boy, event):
        if event == RIGHT_DOWN and boy.bool_leftmove == False:
            boy.velocity += 1
        elif event == LEFT_DOWN and boy.bool_rightmove == False:
            boy.velocity -= 1
        elif event == RIGHT_UP and boy.bool_leftmove == False:
            boy.velocity -= 1
        elif event == LEFT_UP and boy.bool_rightmove == False:
            boy.velocity += 1
        boy.timer = 1000

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        if boy.grabity == False:
            boy.y -= 2;
        if boy.boolFlower:
            boy.add_event(TRANS_FIRE)
    def draw(boy):
        if boy.dir == 1:
            boy.image = idle[2]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            boy.image = idle[3]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class WalkState_Big:

    def enter(boy, event):
        if event == RIGHT_DOWN and boy.bool_leftmove == False:
            boy.velocity += 1
        elif event == LEFT_DOWN and boy.bool_rightmove == False:
            boy.velocity -= 1
        elif event == RIGHT_UP and boy.bool_leftmove == False:
            boy.velocity -= 1
        elif event == LEFT_UP and boy.bool_rightmove == False:
            boy.velocity += 1
        boy.dir = boy.velocity
        boy.timer = 1000

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        boy.timer -= 1
        # boy.x += 0.5 * boy.velocity
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            boy.MovingX += boy.velocity
        boy.x = clamp(25, boy.x, 1600 - 25)
        if boy.grabity == False:
            boy.y -= 2;
        if boy.timer <= 750:
            boy.add_event(DASH_TIMER)
        if boy.boolFlower:
            boy.add_event(TRANS_FIRE)


    def draw(boy):
        if boy.velocity == 1:
            if int(boy.frame) == 0:
                boy.image = load_image('res\walk\walk1_big.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\walk\walk2_big.png')
            elif int(boy.frame) == 2:
                boy.image = load_image('res\walk\walk3_big.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = load_image('res\walk\walkL1_big.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\walk\walkL2_big.png')
            elif int(boy.frame) == 3:
                boy.image = load_image('res\walk\walkL3_big.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)

class RunState_Big:

    def enter(boy, event):
        boy.timer = 1000
        boy.dir = boy.velocity

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME_RUN * game_framework.frame_time) % 3
        boy.timer -= 1
        # boy.x += boy.velocity
        if boy.boolFlower:
            boy.add_event(TRANS_FIRE)
        if boy.grabity == False:
            boy.y -= 2;
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            boy.MovingX += 2 * boy.velocity
        boy.x = clamp(25, boy.x, 1600 - 25)

    def draw(boy):
        if boy.velocity == 1:
            if int(boy.frame) == 0:
                boy.image = load_image('res\\run\\run1_big.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\\run\\run2_big.png')
            elif int(boy.frame) == 2:
                boy.image = load_image('res\\run\\run3_big.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = load_image('res\\run\\runL1_big.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\\run\\runL2_big.png')
            elif int(boy.frame) == 2:
                boy.image = load_image('res\\run\\runL3_big.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class JumpState_Big:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += 1
        elif event == LEFT_DOWN:
            boy.velocity -= 1
        elif event == RIGHT_UP:
            boy.velocity -= 1
        elif event == LEFT_UP:
            boy.velocity += 1
        boy.dir = boy.velocity


    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        # boy.x += boy.dir
        boy.MovingX += boy.dir

        if boy.timer >= 800 and boy.booljump == False:
            boy.y += 2
        else:
            if boy.grabity == False:
                boy.y -= 2;
            else:
                boy.booljump = False
                if boy.dir == 0:
                    boy.add_event(JUMP_TIMER2)
                else:
                    boy.add_event(JUMP_TIMER1)
        if boy.boolFlower:
            boy.add_event(TRANS_FIRE)




        boy.x = clamp(25, boy.x, 1600 - 25)

    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = load_image('res\jump\jump1_big.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\jump\jump2_big.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = load_image('res\jump\jumpL1_big.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\jump\jumpL2_big.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class IdleState_Flower:

    def enter(boy, event):
        if event == RIGHT_DOWN and boy.bool_leftmove == False:
            boy.velocity += 1
        elif event == LEFT_DOWN and boy.bool_rightmove == False:
            boy.velocity -= 1
        elif event == RIGHT_UP and boy.bool_leftmove == False:
            boy.velocity -= 1
        elif event == LEFT_UP and boy.bool_rightmove == False:
            boy.velocity += 1
        boy.timer = 1000

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        if boy.grabity == False:
            boy.y -= 2;
    def draw(boy):
        if boy.dir == 1:
            boy.image = idle[4]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            boy.image = idle[5]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class WalkState_Flower:

    def enter(boy, event):
        if event == RIGHT_DOWN and boy.bool_leftmove == False:
            boy.velocity += 1
        elif event == LEFT_DOWN and boy.bool_rightmove == False:
            boy.velocity -= 1
        elif event == RIGHT_UP and boy.bool_leftmove == False:
            boy.velocity -= 1
        elif event == LEFT_UP and boy.bool_rightmove == False:
            boy.velocity += 1
        boy.dir = boy.velocity
        boy.timer = 1000

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        boy.timer -= 1
        # boy.x += 0.5 * boy.velocity
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            boy.MovingX += boy.velocity
        boy.x = clamp(25, boy.x, 1600 - 25)
        if boy.grabity == False:
            boy.y -= 2;
        if boy.timer <= 750:
            boy.add_event(DASH_TIMER)


    def draw(boy):
        if boy.velocity == 1:
            if int(boy.frame) == 0:
                boy.image = load_image('res\walk\walk1_fire.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\walk\walk2_fire.png')
            elif int(boy.frame) == 2:
                boy.image = load_image('res\walk\walk3_fire.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = load_image('res\walk\walkL1_fire.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\walk\walkL2_fire.png')
            elif int(boy.frame) == 3:
                boy.image = load_image('res\walk\walkL3_fire.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)

class RunState_Flower:

    def enter(boy, event):
        boy.timer = 1000
        boy.dir = boy.velocity

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME_RUN * game_framework.frame_time) % 3
        boy.timer -= 1
        # boy.x += boy.velocity
        if boy.grabity == False:
            boy.y -= 2;
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            boy.MovingX += 2 * boy.velocity
        boy.x = clamp(25, boy.x, 1600 - 25)

    def draw(boy):
        if boy.velocity == 1:
            if int(boy.frame) == 0:
                boy.image = load_image('res\\run\\run1_fire.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\\run\\run2_fire.png')
            elif int(boy.frame) == 2:
                boy.image = load_image('res\\run\\run3_fire.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = load_image('res\\run\\runL1_fire.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\\run\\runL2_fire.png')
            elif int(boy.frame) == 2:
                boy.image = load_image('res\\run\\runL3_fire.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class JumpState_Flower:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += 1
        elif event == LEFT_DOWN:
            boy.velocity -= 1
        elif event == RIGHT_UP:
            boy.velocity -= 1
        elif event == LEFT_UP:
            boy.velocity += 1
        boy.dir = boy.velocity


    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        # boy.x += boy.dir
        boy.MovingX += boy.dir

        if boy.timer >= 800 and boy.booljump == False:
            boy.y += 2
        else:
            if boy.grabity == False:
                boy.y -= 2;
            else:
                boy.booljump = False
                if boy.dir == 0:
                    boy.add_event(JUMP_TIMER2)
                else:
                    boy.add_event(JUMP_TIMER1)



        boy.x = clamp(25, boy.x, 1600 - 25)

    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = load_image('res\jump\jump1_fire.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\jump\jump2_fire.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = load_image('res\jump\jumpL1_fire.png')
            elif int(boy.frame) == 1:
                boy.image = load_image('res\jump\jumpL2_fire.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)

next_state_table = {
    RunState: {SHIFT_UP: WalkState, DASH_TIMER:WalkState, RIGHT_DOWN: IdleState, LEFT_DOWN:IdleState, RIGHT_UP:IdleState, LEFT_UP:IdleState, SPACE:JumpState, TRANS_BIG: RunState_Big },
    IdleState: {RIGHT_UP: WalkState, LEFT_UP: WalkState, RIGHT_DOWN: WalkState, LEFT_DOWN: WalkState, SHIFT_DOWN: IdleState, SHIFT_UP: IdleState, FIRE_KEY: IdleState, SPACE:JumpState, TRANS_BIG: IdleState_Big},
    WalkState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN:RunState, SHIFT_UP: WalkState, FIRE_KEY: WalkState, DASH_TIMER: RunState, SPACE:JumpState, TRANS_BIG:WalkState_Big},
    JumpState: {JUMP_TIMER1: WalkState, JUMP_TIMER2: IdleState, RIGHT_UP:JumpState, LEFT_UP:JumpState, RIGHT_DOWN: JumpState, LEFT_DOWN:JumpState, SPACE:JumpState, TRANS_BIG:IdleState_Big},

    RunState_Big: {SHIFT_UP: WalkState_Big, DASH_TIMER:WalkState_Big, RIGHT_DOWN: IdleState_Big, LEFT_DOWN:IdleState_Big, RIGHT_UP:IdleState_Big, LEFT_UP:IdleState_Big, SPACE:JumpState_Big ,TRANS_FIRE:RunState_Flower},
    IdleState_Big: {RIGHT_UP: WalkState_Big, LEFT_UP: WalkState_Big, RIGHT_DOWN: WalkState_Big, LEFT_DOWN: WalkState_Big, SHIFT_DOWN: IdleState_Big, SHIFT_UP: IdleState_Big, FIRE_KEY: IdleState_Big, SPACE:JumpState_Big, TRANS_FIRE:IdleState_Flower},
    WalkState_Big: {RIGHT_UP: IdleState_Big, LEFT_UP: IdleState_Big, LEFT_DOWN: IdleState_Big, RIGHT_DOWN: IdleState_Big,
               SHIFT_DOWN:RunState_Big, SHIFT_UP: WalkState_Big, FIRE_KEY: WalkState_Big, DASH_TIMER: RunState_Big, SPACE:JumpState_Big ,TRANS_FIRE: WalkState_Flower},
    JumpState_Big: {JUMP_TIMER1: WalkState_Big, JUMP_TIMER2: IdleState_Big, RIGHT_UP:JumpState_Big, LEFT_UP:JumpState_Big, RIGHT_DOWN: JumpState_Big, LEFT_DOWN:JumpState_Big, SPACE:JumpState_Big, TRANS_FIRE:IdleState_Flower},

    RunState_Flower: {SHIFT_UP: WalkState_Flower, DASH_TIMER: WalkState_Flower, RIGHT_DOWN: IdleState_Flower,
                    LEFT_DOWN: IdleState_Flower, RIGHT_UP: IdleState_Flower, LEFT_UP: IdleState_Flower, SPACE: JumpState_Flower, FIRE_KEY: RunState_Flower},
    IdleState_Flower: {RIGHT_UP: WalkState_Flower, LEFT_UP: WalkState_Flower, RIGHT_DOWN: WalkState_Flower,
                        LEFT_DOWN: WalkState_Flower, SHIFT_DOWN: IdleState_Flower, SHIFT_UP: IdleState_Flower,
                         FIRE_KEY: IdleState_Flower, SPACE: JumpState_Flower},
    WalkState_Flower: {RIGHT_UP: IdleState_Flower, LEFT_UP: IdleState_Flower, LEFT_DOWN: IdleState_Flower,
                    RIGHT_DOWN: IdleState_Flower,
                    SHIFT_DOWN: RunState_Flower, SHIFT_UP: WalkState_Flower, FIRE_KEY: WalkState_Flower,
                    DASH_TIMER: RunState_Flower, SPACE: JumpState_Flower},
    JumpState_Flower: {JUMP_TIMER1: WalkState_Flower, JUMP_TIMER2: IdleState_Flower, RIGHT_UP: JumpState_Flower,
                    LEFT_UP: JumpState_Flower, RIGHT_DOWN: JumpState_Flower, LEFT_DOWN: JumpState_Flower, SPACE: JumpState_Flower}
}


class Boy:

    def __init__(self):
        global idle
        self.x, self.y = 800 // 2, 200 #125
        self.MovingX = 0
        self.image = load_image('res\idle\idle0.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.grabity = False
        self.booljump = False
        self.bool_leftmove = False
        self.bool_rightmove = False
        self.boolbig = False
        self.boolFlower = False
        self.plagY = 0
        for i in range(6):
            idle.append(load_image('res\idle\idle%d.png' % i))

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if self.boolbig:
            self.plagY = self.y + 60
        else: self.plagY = self.y
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                history.append(             (self.cur_state.__name__, event_name[event])                )
                self.cur_state = next_state_table[self.cur_state][event]
            except:
                print('State: ', self.cur_state.__name__ , 'Event: ', event_name[event])
                exit(-1)
            # self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def get_bb_stop(self):
        return self.x + self.MovingX - 20, self.y - 60, self.x + self.MovingX + 20, self.y

    def get_bb(self):
        if self.boolbig:
            return self.x - 20, self.y - 60, self.x + 20, self.y + 60
        else:
            return self.x - 20, self.y - 60, self.x + 20, self.y

    def get_grabity(self, check):
        self.grabity = check

    def get_booljump(self, check):
        self.booljump = check

    def get_bool_leftmove(self, check):
        self.bool_leftmove = check

    def get_bool_rightmove(self, check):
        self.bool_rightmove = check

    def fire_ball(self):
        ball = Ball(self.x, self.y, self.dir )
        game_world.add_object(ball, 1)
    def draw(self):
        self.cur_state.draw(self)
        debug_print('Velocity :' + str(self.velocity) + '  Dir:' + str(self.dir))
        draw_rectangle(*self.get_bb())
        
    def getX(self):
        return self.MovingX

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if DEBUG_KEY == key_event:
                print(history[-10:])
            else:
                self.add_event(key_event)
            # self.add_event(key_event)

