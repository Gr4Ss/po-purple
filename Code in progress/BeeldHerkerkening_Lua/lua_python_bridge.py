import lupa
from lupa import LuaRuntime

func = lua_eval('linerecog')
def get_points():
    return_data = func()
    # In volgorde left,top, right, bottom
    return [[(point[0],point[1]) for point in row] for row in return_data]
