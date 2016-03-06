class ManualDrive:
    def __init__(self,command_starter,forward,backward,left,right,forwardleft,forwardright,backwardleft,backwardright,stop):
        self.__commands = []
        self.__command_starter = command_starter
        self.__stop = stop
        self.__valid_commands = {'forward':forward,'backward':backward,'left':left,'right':right}
        self.__duo_commands = {'forwardleft':forwardleft,'forwardright':forwardright,'backwardleft':backwardleft,'backwardright',backwardright}
    def add_command(self,command):
        if (not command in self.__commands) and (command in self.__valid_commands.keys()):
            self.__commands.append(command)
    def delete_command(self,command):
        if command in self.__commands:
            self.__commands.remove(command)
    def clear(self):
        self.__commands = []
    def run(self):
        if len(self.__commands) > 1:
            if 'left' in self.__commands and 'forward' in self.__commands:
                self.__command_starter(self.__duo_commands['forwardleft'])
            elif 'right' in self.__commands and 'forward' in self.__commands:
                self.__command_starter(self.__duo_commands['forwardright'])
            elif 'left' in self.__commands and 'backward' in self.__commands:  
                self.__command_starter(self.__duo_commands['backwardleft'])
            elif 'right' in self.__commands and 'backward' in self.__commands:
                self.__command_starter(self.__duo_commands['backwardright'])
            else:
                self.__command_starter(self.__valid_commands.get(self.__commands[0],None))
        elif len(self.__commands) == 1:
            self.__command_starter(self.__valid_commands.get(self.__commands[0],None))
        else:
            self.__command_starter(self.__stop)
