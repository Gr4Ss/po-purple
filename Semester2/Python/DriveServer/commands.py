def func_lock(identifier,argument=None,lock):
    lock_acquired =lock.claim_lock(identifier)
    return 'OK' if lock.has_lock(identifier) else 'SORRY'

def func_unlock(identifier,argument=None,lock):
    unlock_aquired = lock.free_lock(identifier)
    return 'OK' if unlock_aquired else 'SORRY'

def func_superlock(identifier,passw,lock):
    lock_acquired = lock.claim_super_lock(passw,identifier)
    return 'OK' if has_super_lock(identifier) else 'SORRY'

def func_superunlock(identifier,passw,lock):
    unlock_acquired = lock.free_super_lock(passw,identifier)
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
def func_stop(identifier,argument,lock)):
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

def follow_path(identifier,argument,lock):
    return 'OK'
