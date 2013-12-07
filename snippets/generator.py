def jumps(n,start,jump):
    x = start
    for _ in xrange(n):
        yield x
        x += jump
        