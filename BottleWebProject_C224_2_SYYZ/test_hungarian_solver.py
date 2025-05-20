import unittest  # Модуль для написания юнит-тестов
from hungarian_solver import solve_assignment  # Импортируем твою функцию для решения задачи о назначениях

class TestHungarianSolver(unittest.TestCase):  # Класс, содержащий все тесты (наследуется от unittest.TestCase)

    def test_minimization_cases(self):
        # Тесты для задачи на минимум (минимизация общих затрат)
        test_cases = [
            # Каждый элемент: (матрица затрат, ожидаемая итоговая стоимость)
            ([[4, 2, 8], [2, 3, 7], [3, 1, 6]], 9),
            ([[1, 2, 3], [3, 2, 1], [2, 1, 3]], 3),
            ([[5, 9, 7], [8, 1, 4], [6, 3, 2]], 8),
            ([[7, 5, 9], [8, 2, 6], [3, 7, 4]], 9),
            ([[2, 4, 6], [5, 1, 7], [8, 3, 2]], 6),
        ]
        for matrix, expected_cost in test_cases:
            with self.subTest(matrix=matrix):  # Позволяет запускать каждый набор как отдельный сабтест
                result = solve_assignment(matrix)  # Решаем задачу для текущей матрицы
                self.assertEqual(result['total_cost'], expected_cost)  # Проверяем, что итоговая стоимость совпадает
                self.assertEqual(len(result['assignment']), len(matrix))  # Убедимся, что каждое задание распределено

    def test_maximization_cases(self):
        # Тесты для задачи на максимум (максимизация прибыли или эффективности)
        test_cases = [
            ([[4, 2, 8], [2, 3, 7], [3, 1, 6]], 14),
            ([[15, 30, 5], [20, 25, 10], [10, 35, 40]], 90),
            ([[10, 10, 10], [10, 10, 10], [10, 10, 10]], 30),
            ([[9, 7, 3], [4, 12, 6], [8, 5, 11]], 32),
            ([[20, 25, 30], [22, 27, 35], [24, 20, 28]], 90),
        ]
        for matrix, expected_cost in test_cases:
            with self.subTest(matrix=matrix):  # Сабтест — удобно дебажить конкретный кейс
                result = solve_assignment(matrix, maximize=True)  # Вызываем с параметром максимизации
                self.assertEqual(result['total_cost'], expected_cost)  # Проверка результата
                self.assertEqual(len(result['assignment']), len(matrix))  # Убедимся, что все распределено

    def test_invalid_input(self):
        # Тесты для обработки некорректных данных
        invalid_cases = [
            [["a", "b"], [3, 4]],  # Строки вместо чисел
            [[1, 2], [3]],  # Неравномерная вложенность
            [],  # Пустая матрица
            [[1, 2, 3], [4, 5]],  # Не квадратная
            [[None, 2], [3, 4]],  # None в матрице
        ]
        for case in invalid_cases:
            with self.subTest(case=case):  # Сабтест для каждого кейса
                with self.assertRaises((ValueError, TypeError)):  # Ожидаем, что будет ошибка (типовая или логическая)
                    solve_assignment(case)  # Пытаемся решить — должно упасть

# Если этот файл запускается напрямую — запустить все тесты
if __name__ == '__main__':
    unittest.main()
