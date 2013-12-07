class Useless(object):
    def __getattr__(self,name):
        print 'Attribute %s not found' % (name,)
        return 2*name
    
    def __setattr__(self,name,val):
        print 'Setting %s = %s' % (name,val)
        self.__dict__[name] = val # don't use setattr, since we'll get an infinite loop        
        
    def __delattr__(self,name):
        print 'Deleting %s' % (name,)
        del self.__dict__[name]