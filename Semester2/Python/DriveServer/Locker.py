import time
class Lock:
    def __init__(self,locktime):
        # Global variable storing wheter or not some one has a lock
        self.__lock = False
        # Global variable storing whether someone has a superlock
        self.__superlock = False
        # Global variable storing which ID has the lock
        self.__lock_id = None
        # Global variable storing since when the current ID has the lock as python time.time()
        self.__lock_time = None
        # Global variable storing the maximum time an ID can hold an lock without renewing it (in seconds)
        self.__max_lock_time = locktime
    # A method to claim a lock.
    # If the lock is already given to someone else, False is returned
    # Else the lock is given to this id and True is returned
    def claim_lock(self,identifier):
        if self.__lock:
            return False
        else:
            self.__lock = True
            self.__lock_id = identifier
            self.__lock_time = time.time()
            return True
    # A method to get a super lock
    # To claim a superlock a secret password is needed.
    # A superlock overrules a normal lock and don't expire over time
    def claim_super_lock(self,passw,identifier):
        if self.__superlock or passw != 'purplerain':
            return False
        else:
            self.__lock = True
            self.__superlock = True
            self.__lock_id = identifier
            self.__lock_time = None
            return True
    # A method to free the lock.
    # As the given id has the lock, the lock will be freed and True will be returned
    # Else the lock will remain and False will be returned
    def free_lock(self,identifier):
        if self.has_lock(identifier) and (not self.__superlock):
            self.__lock = False
            self.__lock_id = None
            self.__lock_time = None
            return True
        else:
            return False
    def free_super_lock(self,passw,identifier):
        if has_lock(identifier) and self.__superlock and passw == 'purplerain':
            self.__lock = False
            self.__superlock = False
            self.__lock_id = None
            self.__lock_time = None
            return True
        else:
            return False
    # A method to check wheter or not an id has the lock
    def has_lock(self,identifier):
        return self.__lock and self.__lock_id == identifier
    def has_super_lock(self,identifier):
        return self.__superlock and self.__lock_id = identifier
    # A method to check whether or not a lock is expired
    def check_expire(self):
        if (not self.__superlock) and self.__lock and (time.time() - self.__lock_time >= self.__max_lock_time):
            self.__lock = False
            self.__lock_id = None
            self.__lock_time = None
