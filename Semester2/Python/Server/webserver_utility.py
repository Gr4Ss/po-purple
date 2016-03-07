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
valid_parcours_steps = ['L','R','D']
def check_parcours(parcours):
    global valid_parcours_steps
    if isinstance(parcours,list):
        for step in parcours:
            if isinstance(step,list):
                if len(step) ==2 and step[0] in valid_parcours_steps and isinstance(step[1],int) :
                    return True
                else:
                    return False
            else:
                return False
    else:
        return False
def parse_parcours(commands):
    print commands
    # Throw away the [ ] and split on ,
    cleaned_commands = commands.split(',')[:-1]
    result = []
    for command in cleaned_commands:
        parse1 = re.search('\(([^)]+)\)', command)
        parse2 = re.search('(.*)\(',command)
        if parse1 != None and parse2 != None:
            number = parse1.group(1)
            step = parse2.group(1)
            try:
                number = int(number)
                step = str(step)[0]
            except:
                number = None
                step = None
            result.append([step,number])
    # Throw away the last ,
    return result
