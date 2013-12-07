"""\
retry - a decorator that retries a function/method up to N times.

The wrapped function will exit with the return value of the first successful call, or
with the exception raised in the last attempt, if it failed N times.

>> @retry(3)
>> def foo(...)
"""
def retry(N):
    if N <= 0:
        print 'retries should be more than 0'
        raise ValueError
    def _deco_retry(func):
        def _wrapped(*args, **kw):
            for attempt in xrange(N):
                try:
                    return func(*args, **kw)
                except:
                    if attempt == N-1:
                        raise
        return _wrapped
    return _deco_retry

import random
@retry(3)
def failing(a,b=2):
    r = random.random()
    if r < 0.15:
        print 'success!'
        return True
    raise Exception(r)


failing(3,b=2)