from scipy.optimize import linear_sum_assignment
import numpy as np

def solve_assignment(cost_matrix):
    cost_matrix = np.array(cost_matrix, dtype=int)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    total_cost = cost_matrix[row_ind, col_ind].sum()
    assignment = [None] * len(cost_matrix)
    for r, c in zip(row_ind, col_ind):
        assignment[r] = c
    return {
        'assignment': assignment,
        'total_cost': total_cost
    }
