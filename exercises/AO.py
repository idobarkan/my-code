"""\
AO - Implements the ActiveObject pattern.
Wraps a standard object, so that calls to it are executed asyncronously in a separate thread or threads
owned by the active object, making the object an in-process "server".

For calls that return a result, a Future (see future.py) is returned instead, and the result
can be obtained from the future object when it's ready.

Simple usage:
>> class A(object):
>>    ...
>> a = A(...) # create passive object
>> ao = AO(a) # wrap it with AO
>> ao.start() # start the AO's thread
>> ...
>> f = ao.foo(1,2,3) # calls a.foo in AO's thread
>> ...
>> result = f.get() # block until result is ready and get it (in real life scenarios we'd use an observer instead of blocking)

For more detailed description of the interface, see the unit tests.
"""

from dynamic_proxy import DynamicProxy
import Queue
import threading
import traceback

class AO(DynamicProxy):
    def __init__(self, obj):
        self.obj = obj
        self.q = Queue.Queue()
        
    class Procedure(object):
        def __init__(self,ao, attr_name, a, kw):
            self.attr_name = attr_name
            self.a = a
            self.kw = kw
            self.ao = ao
            print 'Procedure created. name={0}, a={1}, kw={2}'.format(self.attr_name, self.a, self.kw)
        
        def __call__(self):
            meth = getattr(self.ao.obj, self.attr_name)
            print 'Procedure called. name={0}, a={1}, kw={2}'.format(self.attr_name, self.a, self.kw)
            return meth(*self.a, **self.kw)

    def start(self):
        self.worker = threading.Thread(target=self._run, name='worker_thread')
        self.worker.start()
        print 'worker thread started'

    def _dispatch(self, name, *a, **kw):
        procedure = AO.Procedure(self, name, a, kw)
        self.q.put(procedure)
    
    def _run(self):
        '''the worker thread method'''
        while True:
            p = self.q.get()
            try:
                exit_vlaue = p() # to signal the thread to end
                if exit_vlaue == 1:
                    print 'worker thread exiting'
                    break #end thread
            except Exception as e:
                print 'ERROR- procedure run failed. %s' %(traceback.format_exc(e))
    
    def quit(self):
        print 'Quitting'
        def finish(): return 1
        self.q.put(finish)
        self.worker.join()# wait 
        print 'Quitting finished'


class A(object):
    def __init__(self,x=0):
        self.x=x
    def add(self,y, kw='kw'):
        self.x+=y