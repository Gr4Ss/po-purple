import lupa
from lupa import LuaRuntime
lua = LuaRuntime()
func = lua.eval('require("linerecog.lua")')

def get_points():
    return_data = func()
    result = []
    # In volgorde left,top, right, bottom
    for row in return_data.values():
        t = []
        for point in row.values():
                t.append((point[1],point[2]))
        result.append(t)
    return result
