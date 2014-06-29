def rotate_right(mat, N):
    mat2 = list(list(0 for i in range(N)) for j in range(N))
    for i in range(N):
        for j in range(N):
            mat2[j][N - 1 - i] = mat[i][j]
    return mat2
    
def rotate_right_in_place(mat, N):
    for i in range(N):
        for j in range(N):
            new_i = j
            new_j = N - 1 - i
    return mat
    
N=4
mat = list(list((i*N)+j for j in range(N)) for i in range(N))

print(mat)
print('-----------------')
print(rotate_right(mat, N))
print('-----------------')
print(rotate_right_in_place(mat, N))