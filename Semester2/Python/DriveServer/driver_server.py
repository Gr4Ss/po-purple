import zmq
import Locker
import constraints as c
import cPickle
import commands

# The port to which this server will listen
PORT = '5060'
# Setting up 0mq to work as socket server
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://0.0.0.0:%s" % PORT)


lock = Locker.lock(300)
# In testing mode no drive commands are executed
TESTING_MODE = True

if not TESTING_MODE:
# Import the controller
    import Controller
    from Manual_Drive import *
# create controller entity
    controller = Controller.Controller()
    manualDrive = ManualDrive(controller.start_command,controller.forward,controller.backward,controller.left,controller.right,controller.stop)



# A dictionnary containing the possible commands (keys)
# Correct formated command : {'command':'NameCommand',ID:{}}
commands = {'LOCK':{'function':None},'UNLOCK':None,
'STRAIGHT':{'nb_of_arguments':1,'constraint':c.constraint_strait}
,'CIRC':{'nb_of_arguments':1,'constraint':c.constraint_circ},
'SQUARE':{'nb_of_arguments':1,'constraint':c.constraint_square},
'SUPERLOCK':{'nb_of_arguments':1},
'SUPERUNLOCK':{'nb_of_arguments':1},'FStart':{function},
'FStop':None,'RStart':None,'RStop':None,'LStart':None,
'LStop':None, 'BStop':None,'BStart':None, 'STOP':None,
'COMMAND':{'nb_of_arguments':1,'constraint':c.constraint_command}}

# A method to parse the message
# If the message isn't valid, False will be returned
# else a tupple is returned  with as elements, each element in the message seperated by underscores.
def check_message(message):
    global commands
    if isinstance(message,dict):
        command = message.get('command',None)[0]
        if (key not in commands.keys()):
            return False
        ID = message.get('ID',None)
        if not ID:
            return False
        arguments = message.get('argument',None)
        if not arguments:
            return True
        else:
            nb_of_arguments = commands[key].get('nb_of_arguments',0)
            # Check if the message has the valid number of arguments
            if len(arguments) != nb_of_arguments:
                return False
            # Check if there is any constraint
            constraint = commands[key].get('constraint',False)
            if constraint != False:
                to_be_checked = arguments[0]
                temp = constraint(to_be_checked)
                if temp:
                    return True
                else:
                    return False
            else:
                return True
    else:
        return False

if __name__ == '__main__':
    while True:
        message = socket.recv()
        message = cPickle.loads(message)
        lock.check_expire()
        print "Received request: ", message
        messageOK = check_message(message)
        return_message = 'SORRY'
        if (messageOK):
            command = message['command']
            id_ = message['ID']
            argument = message.get('argument',None)
            opt_arguments = commands[command].get('optional_arguments',None)
            if opt_arguments != None:
                argument = opt_arguments + [argument]
            f = commands[command][function]
            return_message = f(identifier,argument,lock)
        else:
            return_message = 'ILLEGAL_MESSAGE'
        print 'Return message: ', return_message
        socket.send(return_message)
