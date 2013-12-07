symbols = ['10', '9', '8', '7', '6', '5', '4', '3', '2', '1']
operators = ['', '+', '-', '*', '/']
joiners_indeices = [0,0,0,0,0,0,0,0,0]
joiners = []

import string
digs = string.digits + string.lowercase

def int2base(x, base):
    if x < 0: sign = -1
    elif x==0: return '0'
    else: sign = 1
    x *= sign
    digits = []
    while x:
        digits.append(digs[x % base])
        x /= base
    if sign < 0:
        digits.append('-')
    digits.reverse()
    return ''.join(digits)
    
    
print int2base(15,2)
