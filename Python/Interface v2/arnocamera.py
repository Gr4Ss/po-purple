import Controller
import lupa
from lupa import LuaRuntime
lua = LuaRuntime()
func = lua.eval("require('linerecog')")

func('L1,R1',Controller.get_engine_distance,Controller.start_commmand,Controller.stop_commmand,Controller.drive_distance)
