import unittest
from direct_lpp import LinearProgrammingProblem

# Наборы задач с решениями — проверка корректности оптимизации — "максимум"
solvable_cases = [
    {
        # Двухпеременная, простое ≤-ограничение: x + y ≤ 10, максимум по y (0,10)
        'objective': [1, 2],
        'constraints': [[1, 1]],
        'signs': ['≤'],
        'rhs': [10],
        'expected_x': [0.0, 10.0],
        'expected_obj': 20.0,
    },
    {
        # Двухпеременная, равенство: x + y = 7, максимум при (0,7) из-за большего веса y
        'objective': [2, 3],
        'constraints': [[1, 1]],
        'signs': ['='],
        'rhs': [7],
        'expected_x': [0.0, 7.0],
        'expected_obj': 21.0,
    },
    {
        # Пересечение двух ограничений 2x+y≤8, x+2y≤10, острые углы: проверяем вершину (2,4)
        'objective': [3, 4],
        'constraints': [[2, 1], [1, 2]],
        'signs': ['≤', '≤'],
        'rhs': [8, 10],
        'expected_x': [2.0, 4.0],
        'expected_obj': 22.0,
    },
    {
        # x+y≤6 и 3x+y≤12, перегруппировка ограничений, оптимум в (3,3)
        'objective': [5, 2],
        'constraints': [[1, 1], [3, 1]],
        'signs': ['≤', '≤'],
        'rhs': [6, 12],
        'expected_x': [3.0, 3.0],
        'expected_obj': 21.0,
    },
    {
        # x+y=5 и 2x+y≤8, максимум при (0,5) на границе равенства и ≤
        'objective': [1, 3],
        'constraints': [[1, 1], [2, 1]],
        'signs': ['=', '≤'],
        'rhs': [5, 8],
        'expected_x': [0.0, 5.0],
        'expected_obj': 15.0,
    },
    {
        # Пересечение x+2y≤4 и 2x+y≤4, оптимальное дробное решение (1.33,1.33)
        'objective': [3, 2],
        'constraints': [[1, 2], [2, 1]],
        'signs': ['≤', '≤'],
        'rhs': [4, 4],
        'expected_x': [1.33, 1.33],
        'expected_obj': 6.67,
    },
    {
        # x+y≤7 и x≤4, две вершины (0,7) и (4,3) — выбираем (4,3)
        'objective': [3, 2],
        'constraints': [[1, 1], [1, 0]],
        'signs': ['≤', '≤'],
        'rhs': [7, 4],
        'expected_x': [4.0, 3.0],
        'expected_obj': 18.0,
    },
    {
        # Трехпеременная, простое ≤-ограничение x+y+z≤6, максимум по z (0,0,6)
        'objective': [1, 2, 3],
        'constraints': [[1, 1, 1]],
        'signs': ['≤'],
        'rhs': [6],
        'expected_x': [0.0, 0.0, 6.0],
        'expected_obj': 18.0,
    },
    {
        # Двухпеременная с ≥-ограничением: x≥2, y≥3, x+y≤10, максимум при (7,3)
        'objective': [1, 1],
        'constraints': [[1, 0], [0, 1], [1, 1]],
        'signs': ['≥', '≥', '≤'],
        'rhs': [2, 3, 10],
        'expected_x': [7.0, 3.0],
        'expected_obj': 10.0,
    },
    {
        # Дегерересированное решение: коэффициенты цели [0,1], x+y≤5, x≤2 — максимум по y при (0,5)
        'objective': [0, 1],
        'constraints': [[1, 1], [1, 0]],
        'signs': ['≤', '≤'],
        'rhs': [5, 2],
        'expected_x': [0.0, 5.0],
        'expected_obj': 5.0,
    },
]

# Несовместные случаи — проверяем возврат None и неограниченность
unsolvable_cases = [
    {
        # Противоречие: x+y≤1 и x+y≥3
        'objective': [1, 1],
        'constraints': [[1, 1], [1, 1]],
        'signs': ['≤', '≥'],
        'rhs': [1, 3],
    },
    {
        # Нет ограничений (неограниченная задача)
        'objective': [1, 1],
        'constraints': [],
        'signs': [],
        'rhs': [],
    },
    {
        # Дублирование x≥10 и x≤5
        'objective': [1, 2],
        'constraints': [[1, 0], [1, 0]],
        'signs': ['≥', '≤'],
        'rhs': [10, 5],
    },
    {
        # Несовместимые равенства x+y=4 и 2x+2y=10
        'objective': [3, 2],
        'constraints': [[1, 1], [2, 2]],
        'signs': ['=', '='],
        'rhs': [4, 10],
    },
    {
        # Противоречие: x≥1, y≥1 и x+y≤1
        'objective': [1, 1],
        'constraints': [[1, 0], [0, 1], [1, 1]],
        'signs': ['≥', '≥', '≤'],
        'rhs': [1, 1, 1],
    }
]

class TestLinearProgrammingProblem(unittest.TestCase):
    def test_has_solution(self):
        for case in solvable_cases:
            with self.subTest(case=case):
                prob = LinearProgrammingProblem(
                    objective=case['objective'],
                    constraints=case['constraints'],
                    signs=case['signs'],
                    rhs=case['rhs'],
                )
                result = prob.solve()
                # Проверка что решение существует
                self.assertIsNotNone(result, "Ожидалось, что решение существует для кейса {case}")
                # Проверка значения переменных и целевой функции
                self.assertEqual(result['x'], case['expected_x'],
                                 f"Неверное решение для кейса {case}")
                self.assertEqual(result['objective_value'], case['expected_obj'],
                                 f"Неверное значение целевой функции для кейса {case}")

    def test_no_solution(self):
        for case in unsolvable_cases:
            with self.subTest(case=case):
                prob = LinearProgrammingProblem(
                    objective=case['objective'],
                    constraints=case['constraints'],
                    signs=case['signs'],
                    rhs=case['rhs'],
                )
                result = prob.solve()
                # Проверка что решения нет
                self.assertIsNone(result, f"Ожидалось отсутствие решения для кейса {case}")

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test*.py')
    # Более подробное описание каждого теста
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)