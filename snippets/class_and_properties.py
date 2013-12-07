import random

class Silly(object):
    def __init__(self,x,fuzz_factor=0.1):
        self._x = x
        self._fuzz_factor = fuzz_factor
        
    @property
    def x(self):
        factor = 1 + self._fuzz_factor*(2*random.random() - 1) # return number in (1-fuzz,1+fuzz)
        return self._x * factor
    
    @x.setter
    def x(self,val):
        self._x = val
        
class C(object):
    def __init__(self):
        self._x = None
    def getx(self):
        return self._x
    def setx(self, value):
        self._x = value
    def delx(self):
        del self._x
    x = property(getx, setx, delx, "I'm the 'x' property.")
    
class C(object):
    def __init__(self):
        self._x = None
    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
    @x.deleter
    def x(self):
        del self._x