closing_counter = 0
close_counter = 0
previous_distance = 400

def distance_detection(distance):
    global previous_distance,close_counter,closing_counter
    too_close = False
    getting_closer = False
    if previous_distance - distance > 2:
        closing_counter += 1
    elif previous_distance - distance < -2:
        closing_counter = 0
    if closing_counter >= 3:
        getting_closer = True

    if distance < 40:
        close_counter += 1
    else:
        close_counter = 0
    if close_counter >= 3:
        too_close = True
    opd = previous_distance
    previous_distance = distance
    if too_close:
        return 255
    #elif getting_closer and distance <40:
    #    print 'Getting closer'
    #    return 2*(opd - distance)**2
    else:
        return 0
