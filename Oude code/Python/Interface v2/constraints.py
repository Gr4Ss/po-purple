# The distance for a straight must be at least 20 (otherwise big proportional error)
# The distance for a straight is at max 600 (not sure when overflow of encoders happen)
def constraint_strait(distance):
    try:
         distance = int(distance)
         return distance >= 20 and distance <= 600
    except:
        return False
# The innerradius must be at least 20 and as max 200
def constraint_circ(radius):
    try:
         distance = int(distance)
         return radius >= 20 and radius <= 200
    except:
        return False
# Sides must be at least 20 cm long and at max 200 cm
def constraint_square(side):
    try:
         distance = int(distance)
         return side >= 20 and side <= 200
    except:
        return False
# input form is [(L/2),(R/5),(D/100)]
# the only valid commands are L,R,D followed by an int
def constraint_command(commands):
    valid_commands = ['L','R','D']
    # Throw away the [] and split on commas
    cleaned_commands = commands[1:-1].split(',')
    for command in cleaned_commands:
        #Throw away the () and split on /
        splitting = command[1:-1].split('/')
        # first part is the command
        comm = splitting[0]
        # second part is value
        valu = splitting[1]
        # the command must be in the valid commands
        if not comm in valid_commands:
            return False
        # The value must cast in an int elsewise not a valid command
        try:
            int(valu)
        except:
            return False
    return True

# some tests
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
    assert constraint_command('[(L/2),(R/5),(D/100)]')
    print 'Testing done'
