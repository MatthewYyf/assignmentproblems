import numpy as np

ratings = np.array([[8, 7, 9, 9],
                    [5, 2, 7, 8],
                    [5, 1, 4, 8],
                    [2, 2, 2, 6]])

underline = np.zeros((len(ratings), len(ratings)))
def jacobi():
    print("Initial Ratings:")
    print(ratings)
    print()
    prep()
    print("Prepped Ratings:")
    print(ratings)
    while True:
        for j in range(len(ratings)):
            get_col_max(j)
        jacobi_konig()
        print()
        print("Underlines:")
        print(underline)
        if len(covered_rows) + len(covered_cols) == len(ratings):
            break
        print()
        print("Ratings:")
        jacobi_egervary()
        print(ratings)

def prep():
    for j in range(len(ratings)):
        col_max, col_max_i = get_col_max(j)
        underline[col_max_i][j] = 1
    for i in range(len(ratings)):
        contains_underline = False
        for j in range(len(ratings)):
            if underline[i][j] == 1:
                contains_underline = True
        if not contains_underline:
            row_max, row_max_j = get_row_max(i)
            col_max, col_max_i = get_col_max(row_max_j)
            underline[i][row_max_j] = 1
            difference = col_max - row_max
            for j in range(len(ratings)):
                ratings[i][j] += difference

def jacobi_konig():
    marked_rows, marked_cols = mark_matrix(underline)
    global covered_rows, covered_cols
    covered_rows = marked_rows
    covered_cols = marked_cols
    
def jacobi_egervary():
    target = 0
    target_j = 0
    for i in range(len(ratings)):
        for j in range(len(ratings)):
            if j not in covered_cols and i not in covered_rows:
                col_max = get_col_max(j)[1]
                if (col_max - ratings[i][j]) < (col_max - target):
                    target = ratings[i][j]
                    target_j = j
    t = get_col_max(target_j)[0] - target
    for i in range(len(ratings)):
        if i not in covered_rows:
            ratings[i,:] += t


def get_row_max(i):
    row_max = float("-inf")
    row_max_j = 0
    for j in range(len(ratings)):
        if row_max < ratings[i][j]:
            row_max = ratings[i][j]
            row_max_j = j
    return row_max, row_max_j


def get_col_max(j):
    col_max = float("-inf")
    col_max_i = 0
    for i in range(len(ratings)):
        if col_max < ratings[i][j]:
            col_max = ratings[i][j]
            col_max_i = i
    for i in range(len(ratings)):
        if col_max == ratings[i][j]:
            underline[i][j] = 1
        else:
            underline[i][j] = 0
    return col_max, col_max_i

# algorithm to find minimum covering
# min_zero_row function from python plain english


def min_zero_row(zero_mat, mark_zero):
    min_row = [99999, -1]
    for row_num in range(zero_mat.shape[0]):
        if np.sum(zero_mat[row_num] == True) > 0 and min_row[0] > np.sum(zero_mat[row_num] == True):
            min_row = [np.sum(zero_mat[row_num] == True), row_num]
    zero_index = np.where(zero_mat[min_row[1]] == True)[0][0]
    mark_zero.append((min_row[1], zero_index))
    zero_mat[min_row[1], :] = False
    zero_mat[:, zero_index] = False

# mark_matrix function from python plain english


def mark_matrix(mat):
    cur_mat = mat
    zero_bool_mat = (cur_mat == 1)
    zero_bool_mat_copy = zero_bool_mat.copy()
    marked_zero = []
    while (True in zero_bool_mat_copy):
        min_zero_row(zero_bool_mat_copy, marked_zero)
    marked_zero_row = []
    marked_zero_col = []
    for i in range(len(marked_zero)):
        marked_zero_row.append(marked_zero[i][0])
        marked_zero_col.append(marked_zero[i][1])
    non_marked_row = list(set(range(cur_mat.shape[0])) - set(marked_zero_row))
    marked_cols = []
    check_switch = True
    while check_switch:
        check_switch = False
        for i in range(len(non_marked_row)):
            row_array = zero_bool_mat[non_marked_row[i], :]
            for j in range(row_array.shape[0]):
                if row_array[j] == True and j not in marked_cols:
                    marked_cols.append(j)
                    check_switch = True
        for row_num, col_num in marked_zero:
            if row_num not in non_marked_row and col_num in marked_cols:
                non_marked_row.append(row_num)
                check_switch = True
    marked_rows = list(set(range(mat.shape[0])) - set(non_marked_row))
    return (marked_rows, marked_cols)


jacobi()
