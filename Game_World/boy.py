from pico2d import *
import game_world
from ball import Ball

history = []

idle = []


# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_DOWN, SHIFT_UP, DASH_TIMER, DEBUG_KEY, FIRE_KEY, SPACE, JUMP_TIMER1, JUMP_TIMER2 = range(12)

event_name = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'SHIFT_DOWN', 'SHIFT_UP', 'DASH_TIMER', 'DEBUG_KEY', 'FIRE_KEY', 'SPACE', 'JUMP_TIMER1', 'JUMP_TIMER2']

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
        if event == RIGHT_DOWN:
            boy.velocity += 1
        elif event == LEFT_DOWN:
            boy.velocity -= 1
        elif event == RIGHT_UP:
            boy.velocity -= 1
        elif event == LEFT_UP:
            boy.velocity += 1
        boy.timer = 1000

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.timer -= 1

    def draw(boy):
        if boy.dir == 1:
            boy.image = idle[0]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            boy.image = idle[1]
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)


class WalkState:

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
        boy.timer = 1000

    def exit(boy, event):
        if event == FIRE_KEY:
            boy.fire_ball()

    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.timer -= 1
        # boy.x += 0.5 * boy.velocity
        boy.MovingX += 0.5 * boy.velocity
        boy.x = clamp(25, boy.x, 1600 - 25)
        if boy.timer <= 750:
            boy.add_event(DASH_TIMER)

    def draw(boy):
        if boy.velocity == 1:
            if boy.frame == 0:
                boy.image = load_image('res\walk\walk1.png')
            elif boy.frame == 1:
                boy.image = load_image('res\walk\walk2.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if boy.frame == 0:
                boy.image = load_image('res\walk\walkL1.png')
            elif boy.frame == 1:
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
        boy.frame = (boy.frame + 1) % 2
        boy.timer -= 1
        # boy.x += boy.velocity
        boy.MovingX += boy.velocity
        boy.x = clamp(25, boy.x, 1600 - 25)

    def draw(boy):
        if boy.velocity == 1:
            if boy.frame == 0:
                boy.image = load_image('res\\run\\run1.png')
            elif boy.frame == 1:
                boy.image = load_image('res\\run\\run2.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if boy.frame == 0:
                boy.image = load_image('res\\run\\runL1.png')
            elif boy.frame == 1:
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
        boy.frame = (boy.frame + 1) % 2
        boy.timer -= 1
        # boy.x += boy.dir
        boy.MovingX += boy.dir
        if boy.timer >= 800:
            boy.y += 2
        else:
            boy.y -= 2
            if boy.y <= 120:
                if boy.dir == 0:
                    boy.add_event(JUMP_TIMER2)
                else:
                    boy.add_event(JUMP_TIMER1)


        boy.x = clamp(25, boy.x, 1600 - 25)

    def draw(boy):
        if boy.dir == 1:
            if boy.frame == 0:
                boy.image = load_image('res\jump\jump1.png')
            elif boy.frame == 1:
                boy.image = load_image('res\jump\jump2.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)
        else:
            if boy.frame == 0:
                boy.image = load_image('res\jump\jumpL1.png')
            elif boy.frame == 1:
                boy.image = load_image('res\jump\jumpL2.png')
            boy.image.clip_draw(0, 0, 32, 32, boy.x, boy.y, 120, 120)

next_state_table = {
    RunState: {SHIFT_UP: WalkState, DASH_TIMER:WalkState, RIGHT_DOWN: IdleState, LEFT_DOWN:IdleState, RIGHT_UP:IdleState, LEFT_UP:IdleState, SPACE:JumpState},
    IdleState: {RIGHT_UP: WalkState, LEFT_UP: WalkState, RIGHT_DOWN: WalkState, LEFT_DOWN: WalkState, SHIFT_DOWN: IdleState, SHIFT_UP: IdleState, FIRE_KEY: IdleState, SPACE:JumpState},
    WalkState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SHIFT_DOWN:RunState, SHIFT_UP: WalkState, FIRE_KEY: WalkState, DASH_TIMER: RunState, SPACE:JumpState},
    JumpState: {JUMP_TIMER1: WalkState, JUMP_TIMER2: IdleState, RIGHT_UP:JumpState, LEFT_UP:JumpState, RIGHT_DOWN: JumpState, LEFT_DOWN:JumpState, SPACE:JumpState}
}


class Boy:

    def __init__(self):
        global idle
        self.x, self.y = 800 // 2, 120
        self.MovingX = 0
        self.image = load_image('res\idle\idle.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        idle.append(load_image('res\idle\idle.png'))
        idle.append(load_image('res\idle\idleL.png'))

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
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
    def fire_ball(self):
        ball = Ball(self.x, self.y, self.dir * 3)
        game_world.add_object(ball, 1)
    def draw(self):
        self.cur_state.draw(self)
        debug_print('Velocity :' + str(self.velocity) + '  Dir:' + str(self.dir))
        
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

