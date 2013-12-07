class S(object):
    def __init__(self, b_empty=False, b_exit=False):
        self.b_empty = b_empty
        self.visited = False
        self.b_exit = b_exit
maze = [
[S(),    S(True),    S(),    S(),    S(),    S(),],
[S(),    S(True),    S(True),S(True),S(True),S(True),],
[S(),    S(),        S(),    S(True),S(),    S(True),],
[S(),    S(True),    S(True),S(True),S(),    S(True,True),],
[S(True),S(True),    S(),    S(True),S(),    S(),],
[S(True),S(),        S(True),S(True),S(True),S(),],
]

def get_out(i, j):
    if not i>=0 or not j>=0:
        return False
    try:
        s = maze[i][j]
    except:
        return False
    if not s.b_empty:
        return False
    if s.visited:
        return False
    maze[i][j].visited = True
    print '(%s,%s)' %(i,j)
    if maze[i][j].b_exit:
        print 'exit'
        return True
    return get_out(i, j-1) or get_out(i-1, j) or get_out(i, j+1) or get_out(i+1, j)
    
get_out(5,0)
