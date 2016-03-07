#import zmq
import sockets_server
import Locker
import constraints as c
import cPickle
from commands import *

# The port to which this server will listen
#PORT = '5060'
# Setting up 0mq to work as socket server
#context = zmq.Context()
#socket = context.socket(zmq.REP)
#socket.bind("tcp://0.0.0.0:%s" % PORT)
socket = sockets_server.CustomSocketServer(5064)


lock = Locker.Lock(300)
# In testing mode no drive commands are executed
TESTING_MODE = True
import Controller
import ControllerCommands
from ManualDrive import *
# create controller entity
controller = Controller.Controller()
manualDrive = ManualDrive(controller.start_command,ControllerCommands.forward,
ControllerCommands.backward,ControllerCommands.left,ControllerCommands.right,ControllerCommands.stop,
ControllerCommands.stop,ControllerCommands.stop,ControllerCommands.stop,ControllerCommands.stop)



# A dictionnary containing the possible commands (keys)
# Correct formated command : {'command':'NameCommand',ID:{}}
commands = {
'LOCK':{'nb_of_arguments':0,'function':func_lock},
'UNLOCK':{'nb_of_arguments':0,'function':func_unlock},
'STRAIGHT':{'nb_of_arguments':1,'constraint':c.constraint_strait},
'CIRC':{'nb_of_arguments':1,'constraint':c.constraint_circ},
'SQUARE':{'nb_of_arguments':1,'constraint':c.constraint_square},
'SUPERLOCK':{'nb_of_arguments':1,'function':func_superlock},
'SUPERUNLOCK':{'nb_of_arguments':1,'function':func_superunlock},
'FStart':{'nb_of_arguments':0,'function':func_add_direction,'optional_arguments':[manualDrive,'forward']},
'FStop':{'nb_of_arguments':0,'function':func_delete_direction,'optional_arguments':[manualDrive,'forward']},
'RStart':{'nb_of_arguments':0,'function':func_add_direction,'optional_arguments':[manualDrive,'right']},
'RStop':{'nb_of_arguments':0,'function':func_delete_direction,'optional_arguments':[manualDrive,'right']},
'LStart':{'nb_of_arguments':0,'function':func_add_direction,'optional_arguments':[manualDrive,'left']},
'LStop':{'nb_of_arguments':0,'function':func_delete_direction,'optional_arguments':[manualDrive,'left']},
'BStart':{'nb_of_arguments':0,'function':func_add_direction,'optional_arguments':[manualDrive,'backward']},
'BStop':{'nb_of_arguments':0,'function':func_delete_direction,'optional_arguments':[manualDrive,'backward']},
'STOP':{'nb_of_arguments':0,'function':func_stop,'optional_arguments':[manualDrive]},
'PARCOURS':{'nb_of_arguments':1,'constraint':c.constraint_parcours}}

# A method to parse the message
# If the message isn't valid, False will be returned
# else a tupple is returned  with as elements, each element in the message seperated by underscores.
def check_message(message):
    global commands
    if isinstance(message,dict):
        command = message.get('command',None)
        print command
        if (command not in commands.keys()):
            return False
        ID = message.get('ID',None)
        if not ID:
            return False
        arguments = message.get('arguments',None)
        nb_of_arguments = commands[command].get('nb_of_arguments',0)
        if not arguments and nb_of_arguments == 0:
            return True
        elif not arguments and nb_of_arguments != 0:
            return False
        else:
            # Check if the message has the valid number of arguments
            if len(arguments) != nb_of_arguments:
                return False
            # Check if there is any constraint
            constraint = commands[command].get('constraint',False)
            if constraint != False:
                print constraint(arguments)
                if constraint(arguments):
                    return True
                else:
                    return False
            else:
                return True
    else:
        return False

if __name__ == '__main__':
    while True:
        conn,message = socket.get_data()
        lock.check_expire()
        print "Received request: ", message
        messageOK = check_message(message)
        return_message = 'SORRY'
        if (messageOK):
            command = str(message['command'])
            identifier = message['ID']
            argument = message.get('arguments',[])
            opt_arguments = commands[command].get('optional_arguments',None)
            if opt_arguments != None:
                argument = opt_arguments + argument
            f = commands[command]['function']
            return_message = f(identifier,argument,lock)
        else:
            return_message = 'ILLEGAL_MESSAGE'
        print 'Return message: ', return_message
        socket.send(conn,return_message)
