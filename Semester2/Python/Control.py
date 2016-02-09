import Engine
import PID


class Control:
    def __init__(self):
        self.__previous_left = 0
        self.__previous_right = 0
        self.__engine_left = Engine.Engine('A')
        self.__engine_right = Engine.Engine('B')
        self.__pidleft = PID.PID(1.,0.5,0.6,.1)
        self.__pidright = PID.PID(1.,0.5,0.6,.1)
    def drive(left,right,dt):
        error_left = self.__previous_left - self.__engine_left.get_count()*self.__engine_left.get_perimeter()
        error_right = self.__previous_right - self.__engine_right.get_count()*self.__engine_right.get_perimeter()
        self.__engine_left.reset_count()
        self.__engine_right.reset_count()
        self.__previous_left = left
        self.__previous_right = right
        value_left = pidleft.value(error_left,dt)
        value_right = pidright.value(error_right,dt)
        engine_left.set_speed(left/dt+value_left)
        engine_right.set_speed(right/dt+value_right)
