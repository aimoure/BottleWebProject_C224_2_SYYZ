from scipy.optimize import linear_sum_assignment
import numpy as np

def solve_assignment(cost_matrix, maximize=False):
    """
    Решает задачу о назначениях с помощью венгерского алгоритма.
    
    :param cost_matrix: двумерный список с затратами или прибылью
    :param maximize: если True — решается задача на максимум
    :return: словарь с результатом — {'assignment': [...], 'total_cost': ...}
    """

    # Преобразуем входную матрицу в numpy-массив с типом int
    cost_matrix = np.array(cost_matrix, dtype=int)

    if maximize:
        # Для задачи на максимум — инвертируем матрицу
        max_val = cost_matrix.max()
        cost_matrix = max_val - cost_matrix

    # Используем венгерский алгоритм
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Вычисляем итоговую стоимость (по оригинальной матрице!)
    if maximize:
        original_matrix = np.array(cost_matrix)
        total_cost = sum(
            (max_val - cost_matrix[r, c]) for r, c in zip(row_ind, col_ind)
        )
    else:
        total_cost = cost_matrix[row_ind, col_ind].sum()

    # Создаём список назначений: индексы задач для каждого работника
    assignment = [None] * len(cost_matrix)
    for r, c in zip(row_ind, col_ind):
        assignment[r] = c

    return {
        'assignment': assignment,
        'total_cost': int(total_cost)  # вдруг numpy int, лучше привести к обычному
    }
