import numpy as np

ratings = np.array([[8, 7, 9, 9],
					[5, 2, 7, 8],
					[5, 1, 4, 8],
					[2, 2, 2, 6]])

def hungarian_method(ratings: np.array):
	print("Ratings:")
	print(ratings)
	print()
	W, v, u = prep(ratings)
	print()
	print("W:")
	print(W)
	while (True):
		covered_rows, covered_cols = konig(W)
		if len(covered_rows) + len(covered_cols) == len(W):
			break
		W, v, u = egervary(W, covered_rows, covered_cols, v, u)
		print()
		print("W:")
		print(W)
	return W, v, u

def prep(ratings: np.array):
	x, y = ratings.shape
	# Let v_j = max(r_ij)
	v = np.zeros(x)
	for j in range(x):
		v[j] = max(ratings[:, j])
	# W_ij = v_j - r_ij
	W = np.zeros((x, y))
	for j in range(x):
		for i in range(y):
			W[i][j] = v[j] - ratings[i][j]
	# u_i = -min(W_i)
	print("W:")
	print(W)
	u = np.zeros(y)
	for i in range(y):
		u[i] = -min(W[i, :])
	for j in range(x):
		for i in range(y):
			W[i][j] += u[i]
	return W, v, u
	

def konig(W):
	return mark_matrix(W)

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
	zero_bool_mat = (cur_mat == 0)
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
	return(marked_rows, marked_cols)

def egervary(W, covered_rows, covered_cols, v, u):
	e = float("inf")
	for i in range(len(W)):
		for j in range(len(W)):
			row_covered = False
			col_covered = False
			for k in covered_rows:
				if k == i:
					row_covered = True
			for k in covered_cols:
				if k == j:
					col_covered = True
			if not (row_covered or col_covered):
				e = min(e, W[i][j])
	for j in covered_cols:
		v[j] += e
		W[:,j] += e
	for i in range(len(W)):
		row_covered = False
		for k in covered_rows:
			if k == i:
				row_covered = True
		if not row_covered:
			u[i] -= e
			W[i,:] -= e
	return W, u, v

W, u, v = hungarian_method(ratings)