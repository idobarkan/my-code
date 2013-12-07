class trace(object):
    """A trivial context manager which prints a message before and after the context is entered"""
    def __init__(self,name):
        self.name = name

    def __enter__(self):
        print 'Entering scope %s' % (self.name,)
           
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            print 'Existing scope %s normally' % (self.name,)
        else:
            print 'Exiting scope %s with exception' % (self.name,)
    
# same as above, but implement with contextmanager decorator - a helper for 
# creating context managers from generators
from contextlib import contextmanager        
@contextmanager
def trace2(name):
    print 'Entering scope %s' % (name,)
    try:
        yield
    except Exception,e:
        print 'Exiting scope %s with exception' % (name,)
    else:
        print 'Exiting scope %s normally' % (name,)
        