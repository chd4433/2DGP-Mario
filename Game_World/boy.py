from pico2d import *
import game_world
from ball import Ball
import game_framework
import server

history = []

idle = []
walk = []
run = []
jump = []
past_MovingX = 0
past_boyX = 0

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

DOWN_SPEED_MPPS = 9.8 * 2
DOWN_SPEED_PPPS = DOWN_SPEED_MPPS * PIXEL_PER_METER
DOWN_SPEED_MPS = 0

JUMP_SPEED_PPS = 40.0 * 1000.0 / 60.0 / 60.0 * PIXEL_PER_METER



TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

TIME_PER_ACTION_RUN = 0.3
ACTION_PER_TIME_RUN = 1.0 / TIME_PER_ACTION_RUN

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_DOWN, SHIFT_UP, DASH_TIMER, DEBUG_KEY, FIRE_KEY, SPACE, JUMP_TIMER1, JUMP_TIMER2, TRANS_BIG, TRANS_FIRE, DEATH, TRANS_SMALL, GOAL = range(17)

event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'SHIFT_DOWN', 'SHIFT_UP', 'DASH_TIMER', 'DEBUG_KEY', 'FIRE_KEY', 'SPACE', 'JUMP_TIMER1', 'JUMP_TIMER2', 'TRANS_BIG', 'TRANS_FIRE', 'DEATH', 'TRANS_SMALL', 'GOAL']

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


class GoalState:
    def enter(boy, event):
        global past_boyX, past_MovingX
        boy.timer = 1000
        past_MovingX = boy.MovingX
        past_boyX = boy.x
        boy.velocity = RUN_SPEED_PPS

    def exit(boy, event):
        pass

    def do(boy):
        global past_boyX, past_MovingX
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        if boy.y >= 125:
            boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
            boy.y -= boy.grabity_speed * game_framework.frame_time
        else:
            if boy.bool_leftmove == False and boy.bool_rightmove == False:
                if boy.MovingX < 0 and boy.x <= 400:
                    boy.x += boy.velocity * game_framework.frame_time
                    if boy.x > 400:
                        boy.MovingX += boy.velocity * game_framework.frame_time
                        boy.x = 400
                elif boy.MovingX >= boy.maxtile_x - 800 and boy.x >= 400:
                    boy.x += boy.velocity * game_framework.frame_time
                    if boy.x < 400:
                        boy.x = 400
                        boy.MovingX += boy.velocity * game_framework.frame_time
                elif boy.x == 400:
                    boy.MovingX += boy.velocity * game_framework.frame_time
        if past_MovingX + 435 + past_boyX <= boy.MovingX + boy.x:
            boy.velocity = 0
            boy.next_stage = True

    def draw(boy):
        if int(boy.frame) == 0:
            if boy.y >= 125:
                if boy.boolFlower == True:
                    boy.image = jump[8]
                elif boy.boolbig == True:
                    boy.image = jump[4]
                else:
                    boy.image = jump[0]
            else:
                if boy.boolFlower == True:
                    boy.image = walk[10]
                elif boy.boolbig == True:
                    boy.image = walk[4]
                else:
                    boy.image = walk[0]

        elif int(boy.frame) == 1:
            if boy.y >= 125:
                if boy.boolFlower == True:
                    boy.image = jump[9]
                elif boy.boolbig == True:
                    boy.image = jump[5]
                else:
                    boy.image = jump[1]
            else:
                if boy.boolFlower == True:
                    boy.image = walk[11]
                elif boy.boolbig == True:
                    boy.image = walk[5]
                else:
                    boy.image = walk[1]

        boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class DeathState:
    def enter(boy, event):
        boy.timer = 1000
        boy.bgm.stop()
        boy.death_sound.play()

    def exit(boy, event):
        pass

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        if boy.invincibility:
            boy.timer2 -= 1
            if boy.timer2 <= 900:
                boy.timer2 = 1000
                boy.invincibility = False

        if boy.timer >= 900:
            boy.y += 1
        else:
            if boy.y >= -50:
                boy.y -= 2
            else:
                boy.death = True
                boy.invincibility = False

    def draw(boy):
        if int(boy.frame) == 0:
            boy.image = load_image('res\dead\dead1.png')
        elif int(boy.frame) == 1:
            boy.image = load_image('res\dead\dead2.png')
        boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)



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
        boy.invincibility = False

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        if boy.grabity == False:
            if boy.y >= -50:
                boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
                boy.y -= boy.grabity_speed * game_framework.frame_time
            else:
                boy.add_event(DEATH)
        else:
            boy.grabity_speed = 0
        if boy.boolbig:
            boy.add_event(TRANS_BIG)
            boy.grow_sound.play()
        if boy.boolFlower:
            boy.add_event(TRANS_FIRE)
            boy.grow_sound.play()
        if boy.invincibility:
            boy.timer2 -= 1
            boy.add_event(DEATH)
            if boy.timer2 <= 900:
                boy.timer2 = 1000
                boy.invincibility = False
        if boy.bgoal:
            boy.add_event(GOAL)

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
            if boy.MovingX < 0 and boy.x <= 400 :
                boy.x += boy.velocity * game_framework.frame_time
                if boy.x > 400:
                    boy.MovingX += boy.velocity * game_framework.frame_time
                    boy.x = 400
            elif boy.MovingX >= boy.maxtile_x - 800 and boy.x >= 400:
                boy.x += boy.velocity * game_framework.frame_time
                if boy.x < 400:
                    boy.x = 400
                    boy.MovingX += boy.velocity * game_framework.frame_time
            elif boy.x == 400:
                boy.MovingX += boy.velocity * game_framework.frame_time

        if boy.bgoal:
            boy.add_event(GOAL)

        boy.x = clamp(25, boy.x, 800 - 25)
        if boy.grabity == False:
            if boy.y >= -50:
                boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
                boy.y -= boy.grabity_speed * game_framework.frame_time
            else:
                boy.add_event(DEATH)
        else:
            boy.grabity_speed = 0
        if boy.timer <= 750:
            boy.add_event(DASH_TIMER)
        if boy.boolFlower:
            boy.add_event(TRANS_FIRE)
            boy.grow_sound.play()
        if boy.boolbig:
            boy.add_event(TRANS_BIG)
            boy.grow_sound.play()
        if boy.invincibility:
            boy.timer2 -= 1
            boy.add_event(DEATH)
            if boy.timer2 <= 900:
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
            if boy.y >= -50:
                boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
                boy.y -= boy.grabity_speed * game_framework.frame_time
            else:
                boy.add_event(DEATH)
        else:
            boy.grabity_speed = 0
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            if boy.MovingX < 0 and boy.x <= 400:
                boy.x += 2 * boy.velocity * game_framework.frame_time
                if boy.x > 400:
                    boy.MovingX += 2 * boy.velocity * game_framework.frame_time
                    boy.x = 400
            elif boy.MovingX >= boy.maxtile_x - 800 and boy.x >= 400:
                boy.x += 2 * boy.velocity * game_framework.frame_time
                if boy.x < 400:
                    boy.x = 400
                    boy.MovingX += 2 * boy.velocity * game_framework.frame_time
            elif boy.x == 400:
                boy.MovingX += 2 * boy.velocity * game_framework.frame_time
        if boy.boolbig:
            boy.add_event(TRANS_BIG)
            boy.grow_sound.play()
        if boy.boolFlower:
            boy.add_event(TRANS_FIRE)
            boy.grow_sound.play()
        if boy.invincibility:
            boy.timer2 -= 1
            boy.add_event(DEATH)
            if boy.timer2 <= 900:
                boy.timer2 = 1000
                boy.invincibility = False
                # boy.add_event(DEATH)
        boy.x = clamp(25, boy.x, 800 - 25)

        if boy.bgoal:
            boy.add_event(GOAL)

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
        boy.jumpy = boy.y
        if boy.bool_air == False:
            boy.Jump_sound.play()
            boy.bool_air = True


    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()
            boy.timer2 = 1000

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        # boy.x += boy.dir
        if boy.MovingX < 0 and boy.x <= 400:
            boy.x += boy.velocity * game_framework.frame_time
            if boy.x > 400:
                boy.MovingX += boy.velocity * game_framework.frame_time
                boy.x = 400
        elif boy.MovingX >= boy.maxtile_x - 800 and boy.x >= 400:
            boy.x += boy.velocity * game_framework.frame_time
            if boy.x < 400:
                boy.x = 400
                boy.MovingX += boy.velocity * game_framework.frame_time
        elif boy.x == 400:
            boy.MovingX += boy.velocity * game_framework.frame_time

        if boy.timer >= 900 and boy.booljump == False:
            boy.y += JUMP_SPEED_PPS * game_framework.frame_time
        elif boy.bool_monster_bully and boy.booljump == False:
            boy.monster_bully_count += 1
            boy.y += JUMP_SPEED_PPS * game_framework.frame_time
            if boy.monster_bully_count >= 10:
                boy.monster_bully_count = 0
                boy.bool_monster_bully = False
                boy.grabity_speed = 0
        else:
            if boy.grabity == False:
                if boy.y >= -50:
                    boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
                    boy.y -= boy.grabity_speed * game_framework.frame_time
                else:
                    boy.add_event(DEATH)
            else:
                boy.grabity_speed = 0
                boy.booljump = False
                boy.bool_air = False
                if boy.dir == 0:
                    boy.add_event(JUMP_TIMER2)
                else:
                    boy.add_event(JUMP_TIMER1)
        if boy.boolbig:
            boy.add_event(TRANS_BIG)
            boy.grow_sound.play()
        if boy.boolFlower:
            boy.add_event(TRANS_FIRE)
            boy.grow_sound.play()

        if boy.invincibility:
            boy.timer2 -= 1
            boy.add_event(DEATH)
            if boy.timer2 <= 900:
                boy.timer2 = 1000
                boy.invincibility = False
                # boy.add_event(DEATH)

        if boy.bgoal:
            boy.add_event(GOAL)



        boy.x = clamp(25, boy.x, 800 - 25)

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
            if boy.y >= -50:
                boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
                boy.y -= boy.grabity_speed * game_framework.frame_time
            else:
                boy.add_event(DEATH)
        else:
            boy.grabity_speed = 0
        if boy.boolFlower:
            boy.add_event(TRANS_FIRE)
            boy.grow_sound.play()

        if boy.invincibility:
            if boy.invin_timer == 1000:
                boy.backgrow_sound.play()
            boy.invin_timer -= 1
            boy.sizey -= 0.3
            if boy.invin_timer <= 900:
                boy.invin_timer = 1000
                boy.invincibility = False
                boy.add_event(TRANS_SMALL)
                boy.boolbig = False
                boy.sizey = 120

        if boy.bgoal:
            boy.add_event(GOAL)
    def draw(boy):
        if boy.dir == 1:
            boy.image = idle[2]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y - (120 - boy.sizey), 120, boy.sizey)
        else:
            boy.image = idle[3]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y - (120 - boy.sizey), 120, boy.sizey)


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
        # boy.timer2 = 1000
        boy.runstate = False

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        boy.timer -= 1
        # boy.x += 0.5 * boy.velocity
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            if boy.MovingX < 0 and boy.x <= 400:
                boy.x += boy.velocity * game_framework.frame_time
                if boy.x > 400:
                    boy.MovingX += boy.velocity * game_framework.frame_time
                    boy.x = 400
            elif boy.MovingX >= boy.maxtile_x - 800 and boy.x >= 400:
                boy.x += boy.velocity * game_framework.frame_time
                if boy.x < 400:
                    boy.x = 400
                    boy.MovingX += boy.velocity * game_framework.frame_time
            elif boy.x == 400:
                boy.MovingX += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 800 - 25)
        if boy.grabity == False:
            if boy.y >= -50:
                boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
                boy.y -= boy.grabity_speed * game_framework.frame_time
            else:
                boy.add_event(DEATH)
        else:
            boy.grabity_speed = 0
        if boy.timer <= 750:
            boy.add_event(DASH_TIMER)
        if boy.boolFlower:
            boy.add_event(TRANS_FIRE)
            boy.grow_sound.play()

        if boy.invincibility:
            if boy.invin_timer == 1000:
                boy.backgrow_sound.play()
            boy.invin_timer -= 1
            boy.sizey -= 0.3
            if boy.invin_timer <= 900:
                boy.invin_timer = 1000
                boy.invincibility = False
                boy.add_event(TRANS_SMALL)
                boy.boolbig = False
                boy.sizey = 120
        if boy.bgoal:
            boy.add_event(GOAL)


    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = walk[4]
            elif int(boy.frame) == 1:
                boy.image = walk[5]
            elif int(boy.frame) == 2:
                boy.image = walk[6]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y - (120 - boy.sizey), 120, boy.sizey)
        else:
            if int(boy.frame) == 0:
                boy.image = walk[7]
            elif int(boy.frame) == 1:
                boy.image = walk[8]
            elif int(boy.frame) == 3:
                boy.image = walk[9]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y - (120 - boy.sizey), 120, boy.sizey)

class RunState_Big:

    def enter(boy, event):
        boy.timer = 1000
        # boy.timer2 = 1000
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
            boy.grow_sound.play()
        if boy.grabity == False:
            if boy.y >= -50:
                boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
                boy.y -= boy.grabity_speed * game_framework.frame_time
            else:
                boy.add_event(DEATH)
        else:
            boy.grabity_speed = 0
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            if boy.MovingX < 0 and boy.x <= 400:
                boy.x += 2 * boy.velocity * game_framework.frame_time
                if boy.x > 400:
                    boy.MovingX += 2 * boy.velocity * game_framework.frame_time
                    boy.x = 400
            elif boy.MovingX >= boy.maxtile_x - 800 and boy.x >= 400:
                boy.x += 2 * boy.velocity * game_framework.frame_time
                if boy.x < 400:
                    boy.x = 400
                    boy.MovingX += 2 * boy.velocity * game_framework.frame_time
            elif boy.x == 400:
                boy.MovingX += 2 * boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 800- 25)

        if boy.invincibility:
            if boy.invin_timer == 1000:
                boy.backgrow_sound.play()
            boy.invin_timer -= 1
            boy.sizey -= 0.3
            if boy.invin_timer <= 900:
                boy.invin_timer = 1000
                boy.invincibility = False
                boy.add_event(TRANS_SMALL)
                boy.boolbig = False
                boy.sizey = 120
        if boy.bgoal:
            boy.add_event(GOAL)

    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = run[4]
            elif int(boy.frame) == 1:
                boy.image = run[5]
            elif int(boy.frame) == 2:
                boy.image = run[6]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y - (120 - boy.sizey), 120, boy.sizey)
        else:
            if int(boy.frame) == 0:
                boy.image = run[7]
            elif int(boy.frame) == 1:
                boy.image = run[8]
            elif int(boy.frame) == 2:
                boy.image = run[9]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y - (120 - boy.sizey), 120, boy.sizey)


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
        # boy.timer2 = 1000
        boy.runstate = False
        if boy.bool_air == False:
            boy.Jump_sound.play()
            boy.bool_air = True


    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        # boy.x += boy.dir
        if boy.MovingX < 0 and boy.x <= 400:
            boy.x += boy.velocity * game_framework.frame_time
            if boy.x > 400:
                boy.MovingX += boy.velocity * game_framework.frame_time
                boy.x = 400
        elif boy.MovingX >= boy.maxtile_x - 800 and boy.x >= 400:
            boy.x += boy.velocity * game_framework.frame_time
            if boy.x < 400:
                boy.x = 400
                boy.MovingX += boy.velocity * game_framework.frame_time
        elif boy.x == 400:
            boy.MovingX += boy.velocity * game_framework.frame_time

        if boy.timer >= 900 and boy.booljump == False:
            boy.y += JUMP_SPEED_PPS * game_framework.frame_time
        elif boy.bool_monster_bully and boy.booljump == False:
            boy.monster_bully_count += 1
            boy.y += JUMP_SPEED_PPS * game_framework.frame_time
            if boy.monster_bully_count >= 10:
                boy.monster_bully_count = 0
                boy.bool_monster_bully = False
                boy.grabity_speed = 0
        else:
            if boy.grabity == False:
                if boy.y >= -50:
                    boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
                    boy.y -= boy.grabity_speed * game_framework.frame_time
                else:
                    boy.add_event(DEATH)
            else:
                boy.grabity_speed = 0
                boy.booljump = False
                boy.bool_air = False
                if boy.dir == 0:
                    boy.add_event(JUMP_TIMER2)
                else:
                    boy.add_event(JUMP_TIMER1)
        if boy.boolFlower:
            boy.add_event(TRANS_FIRE)
            boy.grow_sound.play()

        if boy.invincibility:
            if boy.invin_timer == 1000:
                boy.backgrow_sound.play()
            boy.invin_timer -= 1
            boy.sizey -= 0.3
            if boy.invin_timer <= 900:
                boy.invin_timer = 1000
                boy.invincibility = False
                boy.add_event(TRANS_SMALL)
                boy.boolbig = False
                boy.sizey = 120

        if boy.bgoal:
            boy.add_event(GOAL)




        boy.x = clamp(25, boy.x, 800 - 25)

    def draw(boy):
        if boy.dir == 1:
            if int(boy.frame) == 0:
                boy.image = jump[4]
            elif int(boy.frame) == 1:
                boy.image = jump[5]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y - (120 - boy.sizey), 120, boy.sizey)
        else:
            if int(boy.frame) == 0:
                boy.image = jump[6]
            elif int(boy.frame) == 1:
                boy.image = jump[7]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y - (120 - boy.sizey), 120, boy.sizey)


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
            if boy.y >= -50:
                boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
                boy.y -= boy.grabity_speed * game_framework.frame_time
            else:
                boy.add_event(DEATH)
        else:
            boy.grabity_speed = 0
        if boy.invincibility:
            if boy.invin_timer == 1000:
                boy.backgrow_sound.play()
            boy.invin_timer -= 1
            if boy.invin_timer <= 900:
                boy.invin_timer = 1000
                boy.invincibility = False
                boy.add_event(TRANS_BIG)
                boy.boolFlower = False
        if boy.bgoal:
            boy.add_event(GOAL)
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
            if boy.MovingX < 0 and boy.x <= 400:
                boy.x += boy.velocity * game_framework.frame_time
                if boy.x > 400:
                    boy.MovingX += boy.velocity * game_framework.frame_time
                    boy.x = 400
            elif boy.MovingX >= boy.maxtile_x - 800 and boy.x >= 400:
                boy.x += boy.velocity * game_framework.frame_time
                if boy.x < 400:
                    boy.x = 400
                    boy.MovingX += boy.velocity * game_framework.frame_time
            elif boy.x == 400:
                boy.MovingX += boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 800 - 25)
        if boy.grabity == False:
            if boy.y >= -50:
                boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
                boy.y -= boy.grabity_speed * game_framework.frame_time
            else:
                boy.add_event(DEATH)
        else:
            boy.grabity_speed = 0
        if boy.timer <= 750:
            boy.add_event(DASH_TIMER)


        if boy.invincibility:
            if boy.invin_timer == 1000:
                boy.backgrow_sound.play()
            boy.invin_timer -= 1
            if boy.invin_timer <= 900:
                boy.invin_timer = 1000
                boy.invincibility = False
                boy.add_event(TRANS_BIG)
                boy.boolFlower = False

        if boy.bgoal:
            boy.add_event(GOAL)


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
            if boy.y >= -50:
                boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
                boy.y -= boy.grabity_speed * game_framework.frame_time
            else:
                boy.add_event(DEATH)
        else:
            boy.grabity_speed = 0
        if boy.bool_leftmove == False and boy.bool_rightmove == False:
            if boy.MovingX < 0 and boy.x <= 400:
                boy.x += 2 * boy.velocity * game_framework.frame_time
                if boy.x > 400:
                    boy.MovingX += 2 * boy.velocity * game_framework.frame_time
                    boy.x = 400
            elif boy.MovingX >= boy.maxtile_x - 800 and boy.x >= 400:
                boy.x += 2 * boy.velocity * game_framework.frame_time
                if boy.x < 400:
                    boy.x = 400
                    boy.MovingX += 2 * boy.velocity * game_framework.frame_time
            elif boy.x == 400:
                boy.MovingX += 2 * boy.velocity * game_framework.frame_time
        boy.x = clamp(25, boy.x, 800 - 25)

        if boy.bgoal:
            boy.add_event(GOAL)

        if boy.invincibility:
            if boy.invin_timer == 1000:
                boy.backgrow_sound.play()
            boy.invin_timer -= 1
            if boy.invin_timer <= 900:
                boy.invin_timer = 1000
                boy.invincibility = False
                boy.add_event(TRANS_BIG)
                boy.boolFlower = False

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
        if boy.bool_air == False:
            boy.Jump_sound.play()
            boy.bool_air = True


    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2
        boy.timer -= 1
        # boy.x += boy.dir
        if boy.MovingX < 0 and boy.x <= 400:
            boy.x += boy.velocity * game_framework.frame_time
            if boy.x > 400:
                boy.MovingX += boy.velocity * game_framework.frame_time
                boy.x = 400
        elif boy.MovingX >= boy.maxtile_x - 800 and boy.x >= 400:
            boy.x += boy.velocity * game_framework.frame_time
            if boy.x < 400:
                boy.x = 400
                boy.MovingX += boy.velocity * game_framework.frame_time
        elif boy.x == 400:
            boy.MovingX += boy.velocity * game_framework.frame_time

        if boy.timer >= 900 and boy.booljump == False:
            boy.y += JUMP_SPEED_PPS * game_framework.frame_time
        elif boy.bool_monster_bully and boy.booljump == False:
            boy.monster_bully_count += 1
            boy.y += JUMP_SPEED_PPS * game_framework.frame_time
            if boy.monster_bully_count >= 10:
                boy.monster_bully_count = 0
                boy.bool_monster_bully = False
                boy.grabity_speed = 0
        else:
            if boy.grabity == False:
                if boy.y >= -50:
                    boy.grabity_speed += DOWN_SPEED_PPPS * game_framework.frame_time
                    boy.y -= boy.grabity_speed * game_framework.frame_time
                else:
                    boy.add_event(DEATH)
            else:
                boy.grabity_speed = 0
                boy.booljump = False
                boy.bool_air = False
                if boy.dir == 0:
                    boy.add_event(JUMP_TIMER2)
                else:
                    boy.add_event(JUMP_TIMER1)

        if boy.invincibility:
            if boy.invin_timer == 1000:
                boy.backgrow_sound.play()
            boy.invin_timer -= 1
            if boy.invin_timer <= 900:
                boy.invin_timer = 1000
                boy.invincibility = False
                boy.boolFlower = False

        if boy.bgoal:
            boy.add_event(GOAL)



        boy.x = clamp(25, boy.x, 800 - 25)

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
    RunState: {SHIFT_UP: WalkState, DASH_TIMER:WalkState, RIGHT_DOWN: IdleState, LEFT_DOWN:IdleState, RIGHT_UP:IdleState, FIRE_KEY: RunState,
               LEFT_UP:IdleState, SPACE:JumpState, TRANS_BIG: RunState_Big, DEATH: DeathState, SHIFT_DOWN: RunState, GOAL: GoalState, TRANS_FIRE: RunState_Flower},
    IdleState: {RIGHT_UP: WalkState, LEFT_UP: WalkState, RIGHT_DOWN: WalkState, LEFT_DOWN: WalkState, SHIFT_DOWN: IdleState, SHIFT_UP: IdleState, TRANS_FIRE: IdleState_Flower,
                FIRE_KEY: IdleState, SPACE:JumpState, TRANS_BIG: IdleState_Big, DEATH: DeathState, JUMP_TIMER1:IdleState, GOAL: GoalState},
    WalkState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, TRANS_FIRE:WalkState_Flower, JUMP_TIMER2:WalkState, JUMP_TIMER1:WalkState,
               SHIFT_DOWN:RunState, SHIFT_UP: WalkState, FIRE_KEY: WalkState, DASH_TIMER: RunState, SPACE:JumpState, TRANS_BIG:WalkState_Big, DEATH: DeathState, GOAL: GoalState},
    JumpState: {JUMP_TIMER1: WalkState, JUMP_TIMER2: IdleState, RIGHT_UP:JumpState, LEFT_UP:JumpState, RIGHT_DOWN: JumpState, TRANS_FIRE:JumpState_Flower,
                LEFT_DOWN:JumpState, SPACE:JumpState, TRANS_BIG:IdleState_Big, DEATH: DeathState, SHIFT_UP: JumpState , SHIFT_DOWN: JumpState, GOAL: GoalState , FIRE_KEY: JumpState},

    RunState_Big: {SHIFT_UP: WalkState_Big, DASH_TIMER:WalkState_Big, RIGHT_DOWN: IdleState_Big, LEFT_DOWN:IdleState_Big, RIGHT_UP:IdleState_Big, LEFT_UP:IdleState_Big, FIRE_KEY:RunState_Big,
                   SPACE:JumpState_Big ,TRANS_FIRE:RunState_Flower, TRANS_SMALL:RunState, SHIFT_DOWN: RunState_Big, DEATH: DeathState, GOAL: GoalState},
    IdleState_Big: {RIGHT_UP: WalkState_Big, LEFT_UP: WalkState_Big, RIGHT_DOWN: WalkState_Big, LEFT_DOWN: WalkState_Big, SHIFT_DOWN: IdleState_Big, TRANS_BIG:IdleState_Big,
                    SHIFT_UP: IdleState_Big, FIRE_KEY: IdleState_Big, SPACE:JumpState_Big, TRANS_FIRE:IdleState_Flower, TRANS_SMALL:IdleState, DEATH: DeathState, GOAL: GoalState},
    WalkState_Big: {RIGHT_UP: IdleState_Big, LEFT_UP: IdleState_Big, LEFT_DOWN: IdleState_Big, RIGHT_DOWN: IdleState_Big, DEATH: DeathState, JUMP_TIMER2:WalkState_Big,
               SHIFT_DOWN:RunState_Big, SHIFT_UP: WalkState_Big, FIRE_KEY: WalkState_Big, DASH_TIMER: RunState_Big, SPACE:JumpState_Big ,TRANS_FIRE: WalkState_Flower, TRANS_SMALL: WalkState, GOAL: GoalState},
    JumpState_Big: {JUMP_TIMER1: WalkState_Big, JUMP_TIMER2: IdleState_Big, RIGHT_UP:JumpState_Big, LEFT_UP:JumpState_Big, DEATH: DeathState,FIRE_KEY:JumpState_Big,
                    RIGHT_DOWN: JumpState_Big, LEFT_DOWN:JumpState_Big, SPACE:JumpState_Big, TRANS_FIRE:IdleState_Flower, SHIFT_UP: JumpState_Big, SHIFT_DOWN:JumpState_Big, TRANS_SMALL: JumpState, GOAL: GoalState},

    RunState_Flower: {SHIFT_UP: WalkState_Flower, DASH_TIMER: WalkState_Flower, RIGHT_DOWN: IdleState_Flower, DEATH: DeathState, GOAL: GoalState,
                    LEFT_DOWN: IdleState_Flower, RIGHT_UP: IdleState_Flower, LEFT_UP: IdleState_Flower, SPACE: JumpState_Flower, FIRE_KEY: RunState_Flower, SHIFT_DOWN: RunState_Flower, TRANS_BIG: RunState_Big},
    IdleState_Flower: {RIGHT_UP: WalkState_Flower, LEFT_UP: WalkState_Flower, RIGHT_DOWN: WalkState_Flower, DEATH: DeathState, TRANS_FIRE:IdleState_Flower,
                        LEFT_DOWN: WalkState_Flower, SHIFT_DOWN: IdleState_Flower, SHIFT_UP: IdleState_Flower, GOAL: GoalState,
                         FIRE_KEY: IdleState_Flower, SPACE: JumpState_Flower, TRANS_BIG:IdleState_Big},
    WalkState_Flower: {RIGHT_UP: IdleState_Flower, LEFT_UP: IdleState_Flower, LEFT_DOWN: IdleState_Flower, JUMP_TIMER2:WalkState_Flower,
                    RIGHT_DOWN: IdleState_Flower, TRANS_BIG:WalkState_Big, DEATH: DeathState, GOAL: GoalState,JUMP_TIMER1 :WalkState_Flower,
                    SHIFT_DOWN: RunState_Flower, SHIFT_UP: WalkState_Flower, FIRE_KEY: WalkState_Flower,
                     DASH_TIMER: RunState_Flower, SPACE: JumpState_Flower},
    JumpState_Flower: {JUMP_TIMER1: WalkState_Flower, JUMP_TIMER2: IdleState_Flower, RIGHT_UP: JumpState_Flower, TRANS_BIG:JumpState_Big, DEATH: DeathState, GOAL: GoalState,
                    LEFT_UP: JumpState_Flower, RIGHT_DOWN: JumpState_Flower, LEFT_DOWN: JumpState_Flower, SPACE: JumpState_Flower, SHIFT_UP: JumpState_Flower, SHIFT_DOWN: JumpState_Flower, FIRE_KEY:JumpState_Flower},

    DeathState: {},

    GoalState: {GOAL: GoalState}
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
        self.death = False
        self.maxtile_x = 0
        self.jumpy = 0
        self.bgoal = False
        self.grabity_speed = 0
        self.invin_timer = 1000
        self.sizey = 120
        self.next_stage = False
        self.bool_air = False
        self.font = load_font('ENCR10B.TTF', 16)
        self.bool_monster_bully = False
        self.monster_bully_count = 0
        self.bgm = load_music('res\sound\Super Mario Bross.mp3')
        self.bgm.set_volume(16)
        self.bgm.repeat_play()
        self.Jump_sound = load_wav('res\sound\Jump.wav')
        self.Jump_sound.set_volume(16)
        self.item_sound = load_wav('res\sound\Itemsprouting.wav')
        self.item_sound.set_volume(16)
        self.grow_sound = load_wav('res\sound\Power up.wav')
        self.grow_sound.set_volume(16)
        self.backgrow_sound = load_wav('res\sound\Power up.wav')
        self.backgrow_sound.set_volume(16)
        self.kill_sound = load_wav('res\sound\kill_mob.wav')
        self.kill_sound.set_volume(16)
        self.fire_sound = load_wav('res\sound\Throwing fireball.wav')
        self.fire_sound.set_volume(16)
        self.death_sound = load_wav('res\sound\Mario dies.wav')
        self.death_sound.set_volume(16)
        # self.clear_sound = load_music('res\sound\clear.mp3')
        # self.clear_sound.set_volume(32)



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
        if self.boolbig or self.boolFlower:
            self.plagY = self.y + 60
        else: self.plagY = self.y
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            # print('State: ', self.cur_state)
            try:
                history.append((self.cur_state.__name__, event_name[event]))
                self.cur_state = next_state_table[self.cur_state][event]
            except:
                print('State: ', self.cur_state.__name__, 'Event: ', event_name[event])
                exit(-1)
            # self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)




    def get_bool_goal(self, check):
        self.bgoal = check


    def get_bb_stop(self):
        return self.x + self.MovingX - 20, self.y - 60, self.x + self.MovingX + 20, self.y

    def get_bb(self):
        if self.boolbig or self.boolFlower:
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

    def get_maxtile(self, check):
        self.maxtile_x = check

    def before_movingx(self):
        if self.runstate == False:
            if self.dir == 1:
                self.MovingX -= self.velocity * game_framework.frame_time + 1
            else:
                self.MovingX -= self.velocity * game_framework.frame_time - 1
        else:
            if self.dir == 1:
                self.MovingX -= 2 * self.velocity * game_framework.frame_time + 2
            else:
                self.MovingX -= 2 * self.velocity * game_framework.frame_time - 2

    def fire_ball(self):
        ball = Ball(self.x, self.y - 5, self.dir * 2, self.MovingX)
        self.fire_sound.play()
        game_world.add_object(ball, 3)
    def draw(self):
        self.cur_state.draw(self)
        # debug_print('Velocity :' + str(self.velocity) + '  Dir:' + str(self.dir) + ' MovingX:' + str(self.MovingX))
        self.font.draw(0, 780, 'Velocity :' + str(self.velocity) + '  Dir:' + str(self.dir), (255, 255, 0))
        draw_rectangle(*self.get_bb())
        # print('MovingX:', self.MovingX)
        
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

