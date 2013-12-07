#[1, 3, 7, 12, 18, 26, 35, 45, 56, 69...]
#   2  4  5   6   8   9  10  11   13



def hofstadter(n):
    elem = 1
    diff = 1
    st_yielded = set()
    while n > 0:
        yield elem
        st_yielded.add(elem)
        n -= 1
        diff += 1
        if diff in st_yielded:
            diff += 1
        elem += diff   

for i in hoff(50): print i,
print ''
for i in hoff(5): print i,     
