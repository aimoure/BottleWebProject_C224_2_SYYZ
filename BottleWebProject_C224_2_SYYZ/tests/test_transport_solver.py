import unittest
from transport_solver import optimize_transportation  

class TestTransportationProblem(unittest.TestCase):
    def test_solvable_cases(self):
        """Тесты корректных задач (ожидается валидное решение и стоимость)"""
        test_cases = [
            # 1. Простая 2x2 задача с точным балансом
            {
                'cost_matrix': [[4, 8], [6, 5]],
                'supply': [30, 30],
                'demand': [20, 40],
                'expected_cost': 310,
                'description': 'Базовый случай 2x2 с балансом'
            },
            # 2. Стоимости с нулями
            {
                'cost_matrix': [[0, 2], [3, 0]],
                'supply': [25, 25],
                'demand': [30, 20],
                'expected_cost': 15,
                'description': 'Нули в матрице стоимости'
            },
            # 3. Избыточное предложение — авто-добавление фиктивного спроса
            {
                'cost_matrix': [[2, 3], [5, 4]],
                'supply': [40, 30],
                'demand': [30, 30],
                'expected_cost': 170,
                'description': 'Избыточное предложение'
            },
            # 4. Избыточный спрос — авто-добавление фиктивного поставщика
            {
                'cost_matrix': [[3, 1], [4, 2]],
                'supply': [20, 30],
                'demand': [10, 50],
                'expected_cost': 80,
                'description': 'Избыточный спрос'
            },
            # 5. Сложная 2x3 задача
            {
                'cost_matrix': [[2, 3, 1], [5, 4, 8]],
                'supply': [60, 10],
                'demand': [30, 20, 20],
                'expected_cost': 150,
                'description': '2x3 задача с балансом'
            },
            # 6. Сложная 3x3 задача с нулями
            {
                'cost_matrix': [[0, 3, 1], [4, 0, 2], [3, 1, 0]],
                'supply': [30, 25, 15],
                'demand': [20, 20, 30],
                'expected_cost': 20,
                'description': '3x3 с нулевыми стоимостями'
            },
        ]

        for case in test_cases:
            with self.subTest(msg=case['description']):
                plan, total_cost = optimize_transportation(
                    case['cost_matrix'],
                    case['supply'],
                    case['demand']
                )
                self.assertIsInstance(plan, list, "Ожидался список списков (план)")
                self.assertEqual(total_cost, case['expected_cost'],
                                 f"Неверная стоимость: ожидалась {case['expected_cost']}, получена {total_cost}")

    def test_unsolvable_cases(self):
        """Тесты задач, где решение невозможно (ожидается исключение)"""
        test_cases = [
            # 1. Размеры не совпадают: больше потребителей
            {
                'cost_matrix': [[4, 5]],
                'supply': [30],
                'demand': [10, 30],
                'description': 'Больше потребителей, чем строк в матрице'
            },
            # 2. Размеры не совпадают: больше поставщиков
            {
                'cost_matrix': [[2], [3]],
                'supply': [20, 30],
                'demand': [40],
                'description': 'Больше поставщиков, чем столбцов в матрице'
            },
            # 3. Отрицательная стоимость
            {
                'cost_matrix': [[-1, 2], [3, 4]],
                'supply': [30, 20],
                'demand': [25, 25],
                'description': 'Отрицательная стоимость'
            },
            # 4. Отрицательная поставка
            {
                'cost_matrix': [[1, 2], [3, 4]],
                'supply': [-10, 30],
                'demand': [20, 0],
                'description': 'Отрицательная поставка'
            },
            # 5. Отрицательный спрос
            {
                'cost_matrix': [[1, 2], [3, 4]],
                'supply': [20, 10],
                'demand': [30, -5],
                'description': 'Отрицательный спрос'
            },
            # 6. Несовпадение размерности матрицы (3 supply, 2 demand)
            {
                'cost_matrix': [[1, 2], [3, 4], [5, 6]],
                'supply': [10, 10, 10],
                'demand': [10, 10],
                'description': 'Матрица больше чем supply/demand'
            },
        ]

        for case in test_cases:
            with self.subTest(msg=case['description']):
                with self.assertRaises(Exception, msg=f"Ожидалось исключение для случая: {case['description']}"):
                    optimize_transportation(
                        case['cost_matrix'],
                        case['supply'],
                        case['demand']
                    )


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test*.py')
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)
