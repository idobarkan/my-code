# from inspect import stack
# class T(object):
    # def f(self,*a,**kw):
        # #print 'args:',formatargvalues(*getargvalues(currentframe()))
        # #print 'currentframe:',currentframe()
        # #print 'stack:',stack()
        # # #print 'source:',getsource(currentframe())
        # pass
    # def g(self,*a,**kw):
        # self.f(a,kw)


# t=T()
# t.g(6,1)
from inspect import formatargvalues
# from inspect import formatargvalues, getargvalues, currentframe, stack, getsource
# def f(*a,**kw):
    # print 'args:',formatargvalues(*getargvalues(currentframe()))
    # print 'currentframe:',currentframe()
    # print 'stack:',stack()
    # print 'source:',getsource(currentframe())
    
# f()