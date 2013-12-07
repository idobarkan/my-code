class Base(object):
    
    @classmethod
    def foo(cls):
        print 'foo! in cls=%s' % cls
    
    def __init__(self, x=1):
        self.x = x
        
    def method(self):
        print 'method: self=%s calling foo' % self
        self.foo()

class C(Base):
    pass
    
b=Base()
print 'calling foo in b'
b.foo()
print 'calling method in b'
b.method()
c=C()
print 'calling foo in c'
c.foo()
print 'calling method in c'
c.method()