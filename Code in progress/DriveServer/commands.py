def func_lock(identifier,argument,lock):
    lock_acquired = lock.claim_lock(identifier)
    return 'OK' if lock.has_lock(identifier) else 'SORRY'

def func_unlock(identifier,argument,lock):
    unlock_aquired = lock.free_lock(identifier)
    return 'OK' if unlock_aquired else 'SORRY'

def func_superlock(identifier,passw,lock):
    lock_acquired = lock.claim_super_lock(passw[0],identifier)
    return 'OK' if has_super_lock(identifier) else 'SORRY'

def func_superunlock(identifier,passw,lock):
    unlock_acquired = lock.free_super_lock(passw[0],identifier)
    return 'OK' if unlock_acquired else 'SORRY'

def func_add_direction(identifier,argument,lock):
    manualDrive = argument[0]
    direction = argument[1]
    if not lock.has_lock(identifier):
        return 'SORRY'
    else:
        try:
            manualDrive.add_command(direction)
            manual = manualDrive.run()
            return 'OK'
        except:
            return 'FAILURE'
def func_delete_direction(identifier,argument,lock):
    manualDrive = argument[0]
    direction = argument[1]
    if not lock.has_lock(identifier):
            return 'SORRY'
    else:
        try:
            manualDrive.delete_command(direction)
            manual = manualDrive.run()
            return 'OK'
        except:
            return 'FAILURE'
def func_stop(identifier,argument,lock):
    manualDrive = argument[0]
    if not lock.has_lock(identifier):
        return 'SORRY'
    else:
        try:
            manualDrive.clear()
            manualDrive.run()
            return 'OK'
        except:
            return 'FAILURE'

def func_command(identifier,argument,lock):
    controller = argument[0]
    command = argument[1]
    arg = argument[2]
    if not lock.has_lock(identifier):
        return 'SORRY'
    else:
        try:
            controller.start_command(command,arg)
            return 'OK'
        except:
            return 'FAILURE'
def func_pause_parcours(identifier,argument,lock):
    pass
def func_parcours(identifier,argument,lock):
    pass
def func_packet_delivery(identifier,argument,lock):
    pass
