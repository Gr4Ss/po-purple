import Controller
import lupa
from lupa import LuaRuntime
lua = LuaRuntime()
func = lua.eval("require('linerecog')")
def execute(commands,get_distance,start_command,stop_command,drive_distance):
    func('L1,R1',Controller.get_engine_distance,Controller.start_commmand,Controller.stop_commmand,Controller.drive_distance)
