# tests/test_dual_lpp.py

import unittest
import numpy as np
import itertools

from dual_lpp_practice import solve_dual_simplex, NoSolutionError

# --- Разрешимые случаи (для которых прямая задача гарантированно имеет решение) ---
# Знаки ограничений в двойственной задаче задаются прямо в реализации,
# здесь они не используются при вызове solve_dual_simplex.
solvable_cases = [
    # 1 переменная – простая проверка
    {
        'objective': [1, 2],
        'constraints': [[1, 1]],
        'rhs': [10],
    },
    # точное равенство
    {
        'objective': [2, 3],
        'constraints': [[1, 1]],
        'rhs': [7],
    },
    # две переменные, два <=-ограничения
    {
        'objective': [3, 4],
        'constraints': [[2, 1], [1, 2]],
        'rhs': [8, 10],
    },
    # разные коэффициенты в функции
    {
        'objective': [5, 2],
        'constraints': [[1, 1], [3, 1]],
        'rhs': [6, 12],
    },
    # один =, один <=
    {
        'objective': [1, 3],
        'constraints': [[1, 1], [2, 1]],
        'rhs': [5, 8],
    },
    # обратная матрица
    {
        'objective': [4, 1],
        'constraints': [[1, 2], [2, 1]],
        'rhs': [10, 8],
    },
    # вырождена базисная матрица, но решается
    {
        'objective': [3, 2],
        'constraints': [[1, 1], [1, 0]],
        'rhs': [7, 4],
    },
    # дополнительный случай с = во втором ограничении
    {
        'objective': [2, 5],
        'constraints': [[1, 3], [2, 1]],
        'rhs': [12, 7],
    },
]

# --- Неразрешимые случаи (должно выбрасываться NoSolutionError) ---
unsolvable_cases = [
    # противоречивые <= и ≥
    {
        'objective': [1, 1],
        'constraints': [[1, 1], [1, 1]],
        'rhs': [1, 3],
    },
    # вырождена система равенств с нулевой колонкой
    {
        'objective': [1, 1, 1],
        'constraints': [[1, 0, 0], [0, 1, 0], [1, 1, 0]],
        'rhs': [1, 2, 0],
    },
    # противоречие 5 ≤ x₁+x₂ и x₁+x₂ ≥ 7 при rhs=5,7
    {
        'objective': [2, 1],
        'constraints': [[1, 1], [1, 1]],
        'rhs': [5, 7],
    },
    # два противоречивых ограничения на x₁
    {
        'objective': [1, 2],
        'constraints': [[1, 0], [1, 0]],
        'rhs': [10, 5],
    },
    # система точных равенств, некорректная правая часть
    {
        'objective': [3, 2],
        'constraints': [[1, 1], [2, 2]],
        'rhs': [4, 10],
    },
    # чередование ≥ и ≤ создаёт пустое пространство
    {
        'objective': [1, 3],
        'constraints': [[2, 1], [2, 1], [1, 2]],
        'rhs': [8, 4, 10],
    },
    # противоречие по x₂
    {
        'objective': [4, 1],
        'constraints': [[1, 1], [0, 1], [0, 1]],
        'rhs': [2, 5, 3],
    },
    # два ≥-ограничения, одно ≤
    {
        'objective': [2, 3],
        'constraints': [[1, 0], [0, 1], [1, 1]],
        'rhs': [6, 4, 8],
    },
]


class TestDualSimplex(unittest.TestCase):
    def test_has_solution(self):
        """
        Проверяется, что для разрешимых случаев метод:
        1) не выбрасывает исключение;
        2) возвращает корректную структуру (steps, словарь y, число W);
        3) удовлетворяет условиям двойственности A^T y >= c;
        4) прямая и двойственная целевые функции совпадают (брутфорс).
        """
        # Вспомогательная функция для brute-force прямой задачи (по базисам)
        def brute_primal(c, A, b):
            m, n = len(b), len(c)
            best = None
            M = np.hstack([np.array(A, float), np.eye(m)])
            for basis in itertools.combinations(range(n+m), m):
                cb = [c[j] if j < n else 0 for j in basis]
                try:
                    xB = np.linalg.solve(M[:, basis], b)
                except np.linalg.LinAlgError:
                    continue
                if np.all(xB >= -1e-8):
                    val = sum(cb[i] * xB[i] for i in range(m))
                    if best is None or val > best:
                        best = val
            return best

        for case in solvable_cases:
            with self.subTest(case=case):
                c = case['objective']
                A = case['constraints']
                b = case['rhs']

                # Запуск двойственного симплекс-метода
                steps, y_vals, W = solve_dual_simplex(c, A, b)

                # Типы
                self.assertIsInstance(steps, list)
                self.assertIsInstance(y_vals, dict)
                self.assertIsInstance(W, float)

                # Проверка двойственности A^T y >= c
                A_arr = np.array(A, float)
                for j, cj in enumerate(c):
                    lhs = sum(A_arr[i, j] * y_vals[f'y{i+1}'] for i in range(len(b)))
                    self.assertGreaterEqual(
                        lhs, cj,
                        msg=f"Нарушено A^T y >= c в столбце {j}: LHS={lhs}, c={cj}"
                    )

                # Проверка совпадения целевых функций
                Z = brute_primal(c, A, b)
                self.assertIsNotNone(Z, "Не удалось найти допустимое решение прямой задачи")
                F = -W
                self.assertAlmostEqual(
                    F, Z, places=6,
                    msg=f"Несовпадение прямой Z={Z} и двойственной F={F}"
                )

    def test_no_solution(self):
        """
        Проверяется, что для неразрешимых случаев вызывается NoSolutionError.
        """
        for case in unsolvable_cases:
            with self.subTest(case=case):
                with self.assertRaises(NoSolutionError,
                                       msg=f"Ожидалось NoSolutionError для {case}"):
                    solve_dual_simplex(case['objective'], case['constraints'], case['rhs'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
