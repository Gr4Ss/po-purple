import os,sys,inspect
import Locker
import constraints as c
import cPickle
from commands import *

scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
#append the relative location you want to import from
sys.path.append("../Socket")
import sockets_server

# Setting up a new a new socket server
socket = sockets_server.SocketServer(6000)
socket.start()
# Create a lock entity with a lock time of 20 minutes
lock = Locker.Lock(1200)
# Import controller, entity responsible for starting and stopping controller commands
import Controller
# Import commands that the controller can start
import ControllerCommands
# Import manual drive is entity to select the right controller command given the chosen keys
from ManualDrive import *
# create controller entity

controller = Controller.Controller()
manualDrive = ManualDrive(controller.start_command,ControllerCommands.forward,
ControllerCommands.backward,ControllerCommands.left,ControllerCommands.right,
ControllerCommands.forward_leftforward_left,ControllerCommands.forward_right,
ControllerCommands.backward_left,ControllerCommands.backward_right,
ControllerCommands.stop)

controller = None
manualDrive = None

# A dictionnary containing the possible commands (keys)
# Correct formated command : {'command':'NameCommand','ID':ID,'arguments':[list of arguments]}
# nb_of_arguments reflects the number of arguments expected
# function contain the func that must be started when a given command is Received
# optional arguments contain a list of optional arguments to give to the function
# constraint contain a function that checks if the given arguments are valid
commands = {
'LOCK':{'nb_of_arguments':0,'function':func_lock},
'UNLOCK':{'nb_of_arguments':0,'function':func_unlock},
'STRAIGHT':{'nb_of_arguments':1,'function':func_command,'optional_arguments':[controller,ControllerCommands.ride_distance],'constraint':c.constraint_straight},
'CIRC':{'nb_of_arguments':1,'function':func_command,'optional_arguments':[controller,ControllerCommands.ride_circ],'constraint':c.constraint_circ},
'SQUARE':{'nb_of_arguments':1,'function':func_command,'optional_arguments':[controller,ControllerCommands.ride_polygon],'constraint':c.constraint_square},
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
'PARCOURS':{'nb_of_arguments':1,'function':func_parcours,'constraint':c.constraint_parcours,'optional_arguments':[controller,ControllerCommand.follow_parcours]},
'PAUSEPARCOURS':{'nb_of_arguments':1,'function':func_pause_parcours,'constraint':c.constraint_boolean,'optional_arguments':[controller,ControllerCommand.restart_parcours]},
'PACKETDELIVERY':{'nb_of_arguments':1,'function':func_packet_delivery,'constraint':c.constraint_boolean,'optional_arguments':[controller,ControllerCommand.packet_delivery]}
'UPDATEOWNPOSITION':{'nb_of_arguments':1,'function':func_update_own_position,'constraint':c.constraint_position},
}

# A method to chek the message
# If the message isn't valid, False will be returned
# a valid message is a dictionnary with keys command,ID, arguments
# The value of command must be in commands.keys()
# The value of ID has no constraints
# The value of arguments must be null if commands[command][nb_of_arguments] == 0
# else it must be an array with lenght nb_of_arguments and it must fullify it constraints if
# any given by commands[command][constraint]
def check_message(message):
    global commands
    if isinstance(message,dict):
        command = message.get('command',None)
        try:
            command = str(command)
        except:
            return False
        if (command not in commands.keys()):
            return False
        ID = message.get('ID',None)
        if not ID:
            return False
        arguments = message.get('arguments',None)
        nb_of_arguments = commands[command].get('nb_of_arguments',0)
        print 'Arguments',arguments
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
                return constraint(arguments)
            else:
                return True
    else:
        return False

if __name__ == '__main__':
    while True:
        # check if any new data is available
        conn,message = socket.get_data()
        # Check if the current lock has expired
        lock.check_expire()
        print "Received request: ", message
        # Check if the incomming message is valid
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
            # return_message = f(identifier,argument,lock)
            return_message =  'OK'
        else:
            return_message = 'ILLEGAL_MESSAGE'
        print 'Return message: ', return_message
        socket.send(conn,return_message)
