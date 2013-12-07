"""\
cache decorator.

If the wrapped function/method is called with the same arguments as a previous call, then 
the result is returned from cache, instead of computing it again.
This is only applicable to functions which have no side effect, and that are stateless, i.e. where
the result depends only on the call's arguments.

>> @cache
>> def foo(x,y): ...
>> ...
>> foo(1,2) # first call with args 1,2. calls wrapped function and remembers the result
>> foo(2,3) # first call with args 2,3. calls wrapped function and remembers the result
>> foo(1,2) # returns result from cache. doesn't call wrapped function.
"""
#def cache(func):

def cache(func):
    cache = {}
    def new_func(*args, **kw):
        key = (args, tuple(kw.items()))
        try:
            result = cache[key]
            print 'cache hit!'
            return result
        except KeyError:
            print 'cache miss for {0}'.format(args)
            cache[key] = func(*args, **kw)
            return cache[key]
    return new_func

@cache
def sum(a,b=2):
    result = a+b
    print "working hard. sum:", result
    return result
    

print sum(1,b=2)
print sum(1,b=2)
print sum(2,b=3)
print sum(2,b=3)