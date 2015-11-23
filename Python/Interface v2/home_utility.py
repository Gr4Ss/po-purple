import random

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

def response_parser(response):
    result = '<h1> PIETER = LOSER </h1>'
    if response == 'ILLEGAL_MESSAGE':
        html_file = open('illegalmessage.html')
        result = html_file.read()
        html_file.close()
    elif response == 'LOCK_TRUE' or response == 'LOCK_ALREADY':
        html_file = open('lock.html')
        result = html_file.read()
        html_file.close()
    # if you get this message you got no l(u)(o)ck
    elif response == 'LOCK_FALSE':
        html_file = open('gotnolock.html')
        result = html_file.read()
        html_file.close()
    elif response == 'UNLOCK_TRUE':
        html_file = open('unlock.html')
        result = html_file.read()
        html_file.close()
    elif response == 'NO_LOCK' or response == 'UNLOCK_FALSE':
        html_file = open('nolock.html')
        result = html_file.read()
        html_file.close()
    elif response == 'SUCCES':
        html_file = open('succes.html')
        result = html_file.read()
        html_file.close()
    elif response == 'FAILURE':
        html_file = open('failure.html')
        result = html_file.read()
        html_file.close()
    return result
