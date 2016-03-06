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

valid_parcours_steps = ['L','R','D']
def constraint_parcours(arguments):
    global valid_parcours_steps
    parcours = arguments[0]
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
    print 'Testing done'
