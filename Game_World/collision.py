import server


def collide(a, b):
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def collideUpDown(a, b):
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_b < left_a < right_b or left_b < right_a < right_b:
        if bottom_a < top_b:
            return True
        else: return False
    else: return False

def collideUpDown_false(a, b):
    global bool_all_tile
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_b < left_a < right_b or left_b < right_a < right_b:
        if bottom_a < top_b:
            bool_all_tile = True
        else: bool_all_tile = bool_all_tile or False
    else: bool_all_tile = bool_all_tile or False

def collidejump(a, b):
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_b < left_a < right_b or left_b < right_a < right_b:
        if top_a > bottom_b:
            return True
        else: return False
    else: return False

def collide_left(a, b):
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if bottom_b < top_a < top_b or bottom_b < bottom_b < top_b:
        if right_a > left_b:
            return True
        else: return False
    else: return False

def collide_leftright(a, b):
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if bottom_b < top_a < top_b or bottom_b < bottom_a< top_b:
        if left_b < right_a < right_b or left_b < left_a < right_b :
            return True
        else: return False
    else: return False

def collide_all(a, b):
    left_a , bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_b < right_a < right_b:
        return 1
    elif left_b < left_a < right_b:
        return 2