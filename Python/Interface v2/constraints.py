# The distance for a straight must be at least 20 (otherwise big proportional error)
# The distance for a straight is at max (not sure when overflow of encoders happen)
def constraint_strait(distance):
    try:
         distance = int(distance)
         return distance >= 20 and distance <= 600
    except:
        return False

def constraint_circ(radius):
    try:
         distance = int(distance)
         return radius >= 20 and radius <= 200
    except:
        return False

def constraint_square(side):
    try:
         distance = int(distance)
         return side >= 20 and side <= 200
    except:
        return False
def constraint_command(commands):
    valid_commands = ['L','R','D']
    cleaned_commands = commands[1:-1].split(',')
    for command in cleaned_commands:
        splitting = command[1:-1].split('/')
        comm = splitting[0]
        valu = splitting[1]
        if not comm in valid_commands:
            return False
        try:
            int(valu)
        except:
            return False
    return True

def return_True(argument):
    return True



if __name__ == '__main__':
    print 'Testing done'
    assert constraint_strait(150)
    assert not constraint_strait(10)
    assert not constraint_strait(620)
    assert constraint_circ(50)
    assert not constraint_circ(10)
    assert not constraint_circ(246)
    assert constraint_square(50)
    assert not constraint_square(10)
    assert not constraint_square(300)
    print 'Testing done'
