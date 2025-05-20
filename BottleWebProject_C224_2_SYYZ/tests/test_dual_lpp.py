# tests/test_dual_lpp.py

import unittest
import numpy as np

from dual_lpp_practice import solve_dual_simplex, NoSolutionError

# Только те случаи, в которых прямая задача гарантированно разрешима:
solvable_cases = [
    {
        'objective': [1, 2],
        'constraints': [[1, 1]],
        'rhs': [10],
    },
    {
        'objective': [2, 3],
        'constraints': [[1, 1]],
        'rhs': [7],
    },
    {
        'objective': [3, 4],
        'constraints': [[2, 1], [1, 2]],
        'rhs': [8, 10],
    },
    {
        'objective': [5, 2],
        'constraints': [[1, 1], [3, 1]],
        'rhs': [6, 12],
    },
    {
        'objective': [1, 3],
        'constraints': [[1, 1], [2, 1]],
        'rhs': [5, 8],
    },
    {
        'objective': [4, 1],
        'constraints': [[1, 2], [2, 1]],
        'rhs': [10, 8],
    },
    {
        'objective': [3, 2],
        'constraints': [[1, 1], [1, 0]],
        'rhs': [7, 4],
    },
]

class TestDualSimplex(unittest.TestCase):
    def test_dual_returns_valid_solution(self):
        """
        Для каждого разрешимого случая:
        1) метод не выбрасывает исключение;
        2) возвращает шаги, словарь значений y и W;
        3) для всех i: (A^T y)_i >= c_i (условие двойственности).
        """
        for case in solvable_cases:
            with self.subTest(case=case):
                c = case['objective']
                A = case['constraints']
                b = case['rhs']

                # Запуск двойственного симплекс-метода
                steps, y_vals, W = solve_dual_simplex(c, A, b)

                # Проверка структуры возвращаемых данных
                self.assertIsInstance(steps, list)
                self.assertIsInstance(y_vals, dict)
                self.assertIsInstance(W, float)

                # Проверка условия двойственности: A^T y ≥ c
                A_arr = np.array(A, float)
                for j, cj in enumerate(c):
                    lhs = sum(A_arr[i, j] * y_vals[f'y{i+1}'] for i in range(len(b)))
                    self.assertGreaterEqual(
                        lhs, cj,
                        msg=f"A^T y >= c нарушено для столбца {j}, LHS={lhs}, c={cj}"
                    )

    def test_primal_dual_objectives_match(self):
        """
        Для каждого разрешимого случая проверяется равенство 
        прямой и двойственной целевых функций.
        """
        # Простейший вычислитель прямой задачи: проверка перебором базисов
        def brute_primal(c, A, b):
            # ограничимся малыми размерами
            from itertools import combinations
            m, n = len(b), len(c)
            best = None
            for basis in combinations(range(n + m), m):
                # собираем расширенную матрицу [A|I] и вектор c|0
                M = np.hstack([np.array(A, float), np.eye(m)])
                cb = [c[j] if j < n else 0 for j in basis]
                try:
                    xB = np.linalg.solve(M[:, basis], b)
                except np.linalg.LinAlgError:
                    continue
                if np.all(xB >= -1e-8):
                    obj = sum(cb[i] * xB_i for i, xB_i in enumerate(xB))
                    if best is None or obj > best:
                        best = obj
            return best

        for case in solvable_cases:
            with self.subTest(case=case):
                c = case['objective']
                A = case['constraints']
                b = case['rhs']

                # прямой максимум
                Z = brute_primal(c, A, b)
                self.assertIsNotNone(Z, "Не удалось найти допустимое решение прямой задачи")

                # двойственная целевая W
                _, _, W = solve_dual_simplex(c, A, b)
                F = -W

                self.assertAlmostEqual(
                    F, Z, places=6,
                    msg=f"Прямая Z={Z} и двойственная F={F} не совпадают"
                )

if __name__ == '__main__':
    unittest.main(verbosity=2)
