import unittest
from direct_lpp import LinearProgrammingProblem

solvable_cases = [
    {
        'objective': [1, 2],
        'constraints': [[1, 1]],
        'signs': ['≤'],
        'rhs': [10],
        'expected_x': [0.0, 10.0],
        'expected_obj': 20.0,
    },
    {
        'objective': [2, 3],
        'constraints': [[1, 1]],
        'signs': ['='],
        'rhs': [7],
        'expected_x': [0.0, 7.0],
        'expected_obj': 21.0,
    },
    {
        'objective': [3, 4],
        'constraints': [[2, 1], [1, 2]],
        'signs': ['≤', '≤'],
        'rhs': [8, 10],
        'expected_x': [2.0, 4.0],
        'expected_obj': 22.0,
    },
    {
        'objective': [5, 2],
        'constraints': [[1, 1], [3, 1]],
        'signs': ['≤', '≤'],
        'rhs': [6, 12],
        'expected_x': [3.0, 3.0],
        'expected_obj': 21.0,
    },
    {
        'objective': [1, 3],
        'constraints': [[1, 1], [2, 1]],
        'signs': ['=', '≤'],
        'rhs': [5, 8],
        'expected_x': [2.0, 3.0],
        'expected_obj': 11.0,
    },
    {
        'objective': [4, 1],
        'constraints': [[1, 2], [2, 1]],
        'signs': ['≤', '≤'],
        'rhs': [10, 8],
        'expected_x': [4.0, 2.0],
        'expected_obj': 18.0,
    },
    {
        'objective': [2, 5],
        'constraints': [[1, 3], [2, 1]],
        'signs': ['≤', '='],
        'rhs': [12, 7],
        'expected_x': [3.0, 4.0],
        'expected_obj': 26.0,
    },
    {
        'objective': [3, 2],
        'constraints': [[1, 1], [1, 0]],
        'signs': ['≤', '≤'],
        'rhs': [7, 4],
        'expected_x': [4.0, 3.0],
        'expected_obj': 18.0,
    },
]

unsolvable_cases = [
    {
        'objective': [1, 1],
        'constraints': [[1, 1], [1, 1]],
        'signs': ['≤', '≥'],
        'rhs': [1, 3],
    },
    {
        'objective': [1, 1, 1],
        'constraints': [[1, 0, 0], [0, 1, 0], [1, 1, 0]],
        'signs': ['=', '=', '≤'],
        'rhs': [1, 2, 0],
    },
    {
        'objective': [2, 1],
        'constraints': [[1, 1], [1, 1]],
        'signs': ['≤', '≥'],
        'rhs': [5, 7],
    },
    {
        'objective': [1, 2],
        'constraints': [[1, 0], [1, 0]],
        'signs': ['≥', '≤'],
        'rhs': [10, 5],
    },
    {
        'objective': [3, 2],
        'constraints': [[1, 1], [2, 2]],
        'signs': ['=', '='],
        'rhs': [4, 10],
    },
    {
        'objective': [1, 3],
        'constraints': [[2, 1], [2, 1], [1, 2]],
        'signs': ['≥', '≤', '≥'],
        'rhs': [8, 4, 10],
    },
    {
        'objective': [4, 1],
        'constraints': [[1, 1], [0, 1], [0, 1]],
        'signs': ['≤', '≥', '≤'],
        'rhs': [2, 5, 3],
    },
    {
        'objective': [2, 3],
        'constraints': [[1, 0], [0, 1], [1, 1]],
        'signs': ['≥', '≥', '≤'],
        'rhs': [6, 4, 8],
    },
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