"""\
reset_state - a class decorator that lets you return the instance to its state as it was 
just after construction.

>> @reset_state
>> class X(object):
>>    ...
>> ...
>> x = X(...)
>> ... # use x. change its state
>> x.reset_state() # this method was added by the decorator. calling it returns x to original state

NOTE: Requires that class X's members can be deep copied (using copy.deepcopy)
"""
from copy import deepcopy

def reset_state(obj):
    #change obj.__init__ to save value of self.__dict__
    org_init = obj.__init__
    def _new_init(self,*args,**kw):
        org_init(self, *args, **kw)
        self._orig_state = deepcopy(self.__dict__)
    obj.__init__ = _new_init
    
    #create reset_state() so that it copies old state to new state
    def reset_state(self):
        print 'reseting state...'
        self.__dict__ = deepcopy(self._orig_state)
    obj.reset_state = reset_state
    
    return obj
        
@reset_state
class X(object):
    def __init__(self,i):
        self.i = i
        self.j = i+i

x = X(2)
print x.i, x.j
x.i = 3
print x.i, x.j
x.reset_state()
print x.i, x.j