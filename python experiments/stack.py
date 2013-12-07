import random

class Stack(object):
    def __init__(self):
        self.data = []
    
    def is_empty(self):
        return not self.data
    
    def is_full(self):
        return not self.is_empty()
    
    def push(self, item):
        self.data.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.data.pop()
    
    def top(self):
        if not self.is_empty():
            return self.data[-1] 
    
    def __repr__(self):
        return str(self.data)
        
random.seed(0)        
s=Stack()
for i in range(4):
    s.push([random.randint(0, 9)])
print "before", s

def push(s, node):
    if node == (None,None):
        return
    push(s, node[1])
    s.push(node[0])
    
def reverse(s, item):
    if not s.is_empty():
        node = (s.top(), item)
        s.pop()
        reverse(s, node)
    else:
        push(s, item)

reverse(s, (None,None))
print "after", s