def lcs(s,t):
    L = [[0 for __ in xrange(len(t))] for _ in xrange(len(s))]
    Z = 0
    result = set([])
    for i in xrange(len(s)):
        for j in xrange(len(t)):
            if s[i] == t[j]:
                if i == 0 or j == 0:
                    L[i][j] = 1
                else:
                    L[i][j] = L[i-1][j-1] + 1
                if L[i][j] > Z:
                    Z = L[i][j]
                    result = set([])
                    print 'result=%s'%(result,)
                if L[i][j] == Z:
                    result.add(s[i-Z+1:Z])
                    print 'result=%s'%(result,)
        printmat(L)
    return result
    
def printmat(mat):
    for x in xrange(len(mat)):
        print mat[x]
    print '--------------'