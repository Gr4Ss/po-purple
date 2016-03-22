import random
# Storing the location of the html files
DIRECTORY = ''
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
# A parser for commands:
# ex Left(4),Right(5),Distance(37),
def parse_command(command):
    # List of valid commands
    valid_commands = {'Left':'L','Right':'R','Distance':'D'}
    result = '['
    try:
        # split commands on comma's, last empty tuple is thrown away
        splitted_command = command.split(',')[:-1]
        # Parse each command
        for splitted in splitted_command:
            # Split the command and the value between the brackets
            split = splitted.split('(')
            # Command
            com = split[0]
            # If not in the valid commands return False
            if not com in valid_commands:
                return False
            # Value and throw away the )
            value = int(split[1][:-1])
            # add a new item to the list (L/4)
            result += '('+ str(valid_commands[com]) + '/' + str(value) + '),'
        # if no valid commands are found return false
        if len(result) == 0:
            return False
        # Throw away the last overbodige ',' and add a ']'
        return result[:-1] + ']'
    except:
        return False
# Response parser
def response_parser(response):
    global DIRECTORY
    result = '<h1> Ooh </h1>'
    if response == 'ILLEGAL_MESSAGE':
        html_file = open(DIRECTORY + 'illegalmessage.html')
        result = html_file.read()
        html_file.close()
    elif response == 'LOCK_TRUE' or response == 'LOCK_ALREADY':
        html_file = open(DIRECTORY + 'lock.html')
        result = html_file.read()
        html_file.close()
    # if you get this message you got no l(u)(o)ck
    elif response == 'LOCK_FALSE':
        html_file = open(DIRECTORY + 'gotnolock.html')
        result = html_file.read()
        html_file.close()
    elif response == 'UNLOCK_TRUE':
        html_file = open(DIRECTORY + 'unlock.html')
        result = html_file.read()
        html_file.close()
    elif response == 'NO_LOCK' or response == 'UNLOCK_FALSE':
        html_file = open(DIRECTORY + 'nolock.html')
        result = html_file.read()
        html_file.close()
    elif response == 'SUCCES':
        html_file = open(DIRECTORY + 'succes.html')
        result = html_file.read()
        html_file.close()
    elif response == 'FAILURE':
        html_file = open(DIRECTORY + 'failure.html')
        result = html_file.read()
        html_file.close()
    elif response == 'SERVERDOWN':
        html_file = open(DIRECTORY + 'server_down.html')
        result = html_file.read()
        html_file.close()
    return result
