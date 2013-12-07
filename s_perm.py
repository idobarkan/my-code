def permute(s):
    res = []
    if len(s) == 1:
        res = [s]
    else:
        for i, c in enumerate(s):
            for perm in permute(s[:i] + s[i+1:]):
                res += [c + perm]

    return res

def count_perm(a,b):
    total=0
    for p in permute(a):
        if p in b:
            total += 1
            print p
    return total

print count_perm('ido','idoidodi')

