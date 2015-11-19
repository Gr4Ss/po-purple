# The distance for a straight must be at least 20 (otherwise big proportional error)
# The distance for a straight is at max (not sure when overflow of encoders happen)
def constraint_strait(distance):
    return distance >= 20 and distance <= 600

def constraint_circ(radius):
    return radius >= 20 and radius <= 200

def constraint_square(side):
    return side >= 20 and side <= 200

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
