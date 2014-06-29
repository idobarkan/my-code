def zeroize_rows_or_columns_with_0(mat, N):
    set_rows_with_0 = set()
    set_cols_with_0 = set()
    for row in range(N):
        for col in range(N):
            if mat[row][col] == 0:
                set_cols_with_0.add(col)
                set_rows_with_0.add(row)
    for row in range(N):
        for col in range(N):
            if row in set_rows_with_0 or col in set_cols_with_0:
                mat[row][col] = 0
    return mat

N=3
mat = list(list(j*N+i for i in range(N)) for j in range(N))
print(mat)
print('-------------')
print(zeroize_rows_or_columns_with_0(mat, N))