# The distance for a straight must be at least 20 (otherwise big proportional error)
# The distance for a straight is at max 600 (not sure when overflow of encoders happen)
def constraint_straight(arguments):
    distance = arguments[0]
    try:
         distance = int(distance)
         return distance >= 20 and distance <= 600
    except:
        return False
# The innerradius must be at least 20 and as max 200
def constraint_circ(arguments):
    radius = arguments[0]
    try:
         distance = int(distance)
         return radius >= 20 and radius <= 200
    except:
        return False
# Sides must be at least 20 cm long and at max 200 cm
def constraint_square(arguments):
    side = arguments[0]
    try:
         distance = int(distance)
         return side >= 20 and side <= 200
    except:
        return False

valid_parcours_steps = ['left','right','straight']
def constraint_parcours(arguments):
    global valid_parcours_steps
    parcours = arguments[0]
    if isinstance(parcours,list):
        for step in parcours:
            if not step in valid_parcours_steps:
                return False
        return True
    else:
        return False
def constraint_boolean(arguments):
    argument = arguments[0]
    print argument
    return (argument==True or argument == False)
def constraint_position(argument):
    return True
