def sign(x):
    return -1 if x < 0 else 1

def maxabspos(lst):
    if len(lst) == 0:
        return False
    maxi = abs(lst[0])
    pos = 0
    k = 1
    while k < len(lst):
        if abs(lst[k]) > maxi:
            pos = k
            maxi = abs(lst[k])
        k += 1
    return pos
