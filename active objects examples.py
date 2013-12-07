class X(AO):
    def __init__(self):
        sat_y = sattelite(Y(),self)
        ao_y = AO(Y())

    def foo(self):
        return 1
        
    @isSync
    def sync(self)
        return 1
    
    @async_coroutine
    def a_sync(self)
    #a generator
        yield f #returns f.get()
        yield AsyncWaitForFuture(f,progress=(0,50))#to control progress
        yield AsyncWaitForFuture(f,progress=(51,70))#to control progress
        yield AsyncWaitForFuture(f,)#to control progress
        yield self._ao._other()
        yield AsyncRV(return_value)
        
    @async_coroutine
    def other(self)
    #a generator
        yield f #returns f.get()
        yield AsyncRV(return_value)
        
#in client   
ax=AO(X)

f=ax.foo() #returns a future and runs in other thread
v=f.get() #will wait
