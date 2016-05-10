import random
import re
def create_hash(length):
    result = ''
    for i in range(0,length):
        rnd = random.randint(0,61)
        # if rnd < 10, a number between 0 and 9 is added to the result
        if rnd < 10:
            new = chr(48+rnd)
        # if 10<= rnd < 36, a letter between A and Z is added to the result
        elif rnd < 36:
            new = chr(65+rnd-10)
        # if  36 <= rnd < 62, a letter between a and z is added to the result.
        else:
            new = chr(97+rnd-36)
        result += str(new)
    return result
valid_parcours_steps = ['left','right','straight']
def check_parcours(parcours):
    global valid_parcours_steps
    if isinstance(parcours,list):
        for item in parcours:
            if not (item in valid_parcours_steps):
                return False
            return True
    else:
        return False
def parse_parcours(commands):
    result = []
    for command in commands:
        direction = str(command["direction"])
        count = int(command["count"])
        for i in range(0,count-1):
            result.append('straight')
        result.append(direction)
    # Throw away the last ,
    return result
