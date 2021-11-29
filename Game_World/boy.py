from pico2d import *
import game_world
from ball import Ball
import game_framework

history = []

idle = []
walk = []
run = []
jump = []

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)



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
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN and boy.bool_rightmove == False:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP and boy.bool_leftmove == False:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP and boy.bool_rightmove == False:
            boy.velocity += RUN_SPEED_PPS
        boy.timer = 1000
        boy.timer2 = 1000

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
        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 500:
                boy.timer2 = 1000
                boy.invincibility = False
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
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN and boy.bool_rightmove == False:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP and boy.bool_leftmove == False:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP and boy.bool_rightmove == False:
            boy.velocity += RUN_SPEED_PPS
        boy.dir = clamp(-1,boy.velocity, 1)
        boy.timer = 1000
        boy.timer2 = 1000
        boy.runstate = False

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        # boy.x += 0.5 * boy.velocity
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            boy.MovingX += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600 - 25)
        if boy.grabity == False:
            boy.y -= 2;
        if boy.timer <= 750:
            boy.add_event(DASH_TIMER)
        if boy.boolbig:
            boy.add_event(TRANS_BIG)
        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 500:
                boy.timer2 = 1000
                boy.invincibility = False
    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = walk[0]
            elif int(boy.frame) == 1:
                boy.image = walk[1]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = walk[2]
            elif int(boy.frame) == 1:
                boy.image = walk[3]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)

class RunState:

    def enter(boy, event):
        boy.timer = 1000
        boy.timer2 = 1000
        boy.dir = clamp(-1,boy.velocity, 1)
        boy.runstate = True

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
            boy.MovingX += 2 * boy.velocity * game_framework.frame_time
        if boy.boolbig:
            boy.add_event(TRANS_BIG)
        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 500:
                boy.timer2 = 1000
                boy.invincibility = False
        boy.x = clamp(25, boy.x, 1600 - 25)

    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = run[0]
            elif int(boy.frame) == 1:
                boy.image = run[1]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = run[2]
            elif int(boy.frame) == 1:
                boy.image = run[3]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class JumpState:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
        boy.dir = clamp(-1,boy.velocity, 1)
        boy.runstate = False


    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()
            boy.timer2 = 1000

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        # boy.x += boy.dir
        boy.MovingX += boy.velocity * game_framework.frame_time

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

        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 500:
                boy.timer2 = 1000
                boy.invincibility = False



        boy.x = clamp(25, boy.x, 1600 - 25)

    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = jump[0]
            elif int(boy.frame) == 1:
                boy.image = jump[1]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = jump[2]
            elif int(boy.frame) == 1:
                boy.image = jump[3]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)



class IdleState_Big:

    def enter(boy, event):
        if event == RIGHT_DOWN and boy.bool_leftmove == False:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN and boy.bool_rightmove == False:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP and boy.bool_leftmove == False:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP and boy.bool_rightmove == False:
            boy.velocity += RUN_SPEED_PPS
        boy.timer = 1000
        boy.timer2 = 1000

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

        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 500:
                boy.timer2 = 1000
                boy.invincibility = False
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
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN and boy.bool_rightmove == False:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP and boy.bool_leftmove == False:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP and boy.bool_rightmove == False:
            boy.velocity += RUN_SPEED_PPS
        boy.dir = clamp(-1,boy.velocity, 1)
        boy.timer = 1000
        boy.timer2 = 1000
        boy.runstate = False

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        boy.timer -= 1
        # boy.x += 0.5 * boy.velocity
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            boy.MovingX += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600 - 25)
        if boy.grabity == False:
            boy.y -= 2;
        if boy.timer <= 750:
            boy.add_event(DASH_TIMER)
        if boy.boolFlower:
            boy.add_event(TRANS_FIRE)

        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 500:
                boy.timer2 = 1000
                boy.invincibility = False


    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = walk[4]
            elif int(boy.frame) == 1:
                boy.image = walk[5]
            elif int(boy.frame) == 2:
                boy.image = walk[6]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = walk[7]
            elif int(boy.frame) == 1:
                boy.image = walk[8]
            elif int(boy.frame) == 3:
                boy.image = walk[9]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)

class RunState_Big:

    def enter(boy, event):
        boy.timer = 1000
        boy.timer2 = 1000
        boy.dir = clamp(-1,boy.velocity, 1)
        boy.runstate = True

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
            boy.MovingX += 2 * boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600 - 25)

        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 500:
                boy.timer2 = 1000
                boy.invincibility = False

    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = run[4]
            elif int(boy.frame) == 1:
                boy.image = run[5]
            elif int(boy.frame) == 2:
                boy.image = run[6]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = run[7]
            elif int(boy.frame) == 1:
                boy.image = run[8]
            elif int(boy.frame) == 2:
                boy.image = run[9]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class JumpState_Big:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
        boy.dir = clamp(-1,boy.velocity, 1)
        boy.timer2 = 1000
        boy.runstate = False


    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        # boy.x += boy.dir
        boy.MovingX += boy.velocity * game_framework.frame_time

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

        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 500:
                boy.timer2 = 1000
                boy.invincibility = False




        boy.x = clamp(25, boy.x, 1600 - 25)

    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = jump[4]
            elif int(boy.frame) == 1:
                boy.image = jump[5]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = jump[6]
            elif int(boy.frame) == 1:
                boy.image = jump[7]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class IdleState_Flower:

    def enter(boy, event):
        if event == RIGHT_DOWN and boy.bool_leftmove == False:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN and boy.bool_rightmove == False:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP and boy.bool_leftmove == False:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP and boy.bool_rightmove == False:
            boy.velocity += RUN_SPEED_PPS
        boy.timer = 1000
        boy.timer2 = 1000

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        if boy.grabity == False:
            boy.y -= 2;

        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 500:
                boy.timer2 = 1000
                boy.invincibility = False
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
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN and boy.bool_rightmove == False:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP and boy.bool_leftmove == False:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP and boy.bool_rightmove == False:
            boy.velocity += RUN_SPEED_PPS
        boy.dir = clamp(-1,boy.velocity, 1)
        boy.timer = 1000
        boy.timer2 = 1000
        boy.runstate = False

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        boy.timer -= 1
        # boy.x += 0.5 * boy.velocity
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            boy.MovingX += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600 - 25)
        if boy.grabity == False:
            boy.y -= 2;
        if boy.timer <= 750:
            boy.add_event(DASH_TIMER)
        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 500:
                boy.timer2 = 1000
                boy.invincibility = False


    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = walk[10]
            elif int(boy.frame) == 1:
                boy.image = walk[11]
            elif int(boy.frame) == 2:
                boy.image = walk[12]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = walk[13]
            elif int(boy.frame) == 1:
                boy.image = walk[14]
            elif int(boy.frame) == 3:
                boy.image = walk[15]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)

class RunState_Flower:

    def enter(boy, event):
        boy.timer = 1000
        boy.timer2 = 1000
        boy.dir = clamp(-1,boy.velocity, 1)
        boy.runstate = True

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
            boy.MovingX += 2 * boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 1600 - 25)

        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 500:
                boy.timer2 = 1000
                boy.invincibility = False

    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = run[10]
            elif int(boy.frame) == 1:
                boy.image = run[11]
            elif int(boy.frame) == 2:
                boy.image = run[12]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = run[13]
            elif int(boy.frame) == 1:
                boy.image = run[14]
            elif int(boy.frame) == 2:
                boy.image = run[15]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class JumpState_Flower:

    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            boy.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            boy.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            boy.velocity += RUN_SPEED_PPS
        boy.dir = clamp(-1,boy.velocity, 1)
        boy.timer2 = 1000
        boy.runstate = False


    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        # boy.x += boy.dir
        boy.MovingX += boy.velocity * game_framework.frame_time

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

        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 500:
                boy.timer2 = 1000
                boy.invincibility = False



        boy.x = clamp(25, boy.x, 1600 - 25)

    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = jump[8]
            elif int(boy.frame) == 1:
                boy.image = jump[9]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if int(boy.frame) == 0:
                boy.image = jump[10]
            elif int(boy.frame) == 1:
                boy.image = jump[11]
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
        self.invincibility = False
        self.runstate = False

        for i in range(6):
            idle.append(load_image('res\idle\idle%d.png' % i))
        for i in range(16):
            walk.append(load_image('res\walk\walk%d.png' % i))
        for i in range(16):
            run.append(load_image('res\\run\\run%d.png' % i))
        for i in range(12):
            jump.append(load_image('res\jump\jump%d.png' % i))

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

    def get_invincibility(self, check):
        self.invincibility = check

    def before_movingx(self):
        if self.runstate == False:
            self.MovingX -= self.velocity * game_framework.frame_time
        else:
            self.MovingX -= 2 * self.velocity * game_framework.frame_time

    def fire_ball(self):
        ball = Ball(self.x, self.y, self.dir * 2)
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

