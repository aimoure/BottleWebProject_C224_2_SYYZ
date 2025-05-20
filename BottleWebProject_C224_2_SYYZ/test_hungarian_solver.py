import unittest  # ������ ��� ��������� ����-������
from hungarian_solver import solve_assignment  # ����������� ���� ������� ��� ������� ������ � �����������

class TestHungarianSolver(unittest.TestCase):  # �����, ���������� ��� ����� (����������� �� unittest.TestCase)

    def test_minimization_cases(self):
        # ����� ��� ������ �� ������� (����������� ����� ������)
        test_cases = [
            # ������ �������: (������� ������, ��������� �������� ���������)
            ([[4, 2, 8], [2, 3, 7], [3, 1, 6]], 9),
            ([[1, 2, 3], [3, 2, 1], [2, 1, 3]], 3),
            ([[5, 9, 7], [8, 1, 4], [6, 3, 2]], 8),
            ([[7, 5, 9], [8, 2, 6], [3, 7, 4]], 9),
            ([[2, 4, 6], [5, 1, 7], [8, 3, 2]], 6),
        ]
        for matrix, expected_cost in test_cases:
            with self.subTest(matrix=matrix):  # ��������� ��������� ������ ����� ��� ��������� �������
                result = solve_assignment(matrix)  # ������ ������ ��� ������� �������
                self.assertEqual(result['total_cost'], expected_cost)  # ���������, ��� �������� ��������� ���������
                self.assertEqual(len(result['assignment']), len(matrix))  # ��������, ��� ������ ������� ������������

    def test_maximization_cases(self):
        # ����� ��� ������ �� �������� (������������ ������� ��� �������������)
        test_cases = [
            ([[4, 2, 8], [2, 3, 7], [3, 1, 6]], 14),
            ([[15, 30, 5], [20, 25, 10], [10, 35, 40]], 90),
            ([[10, 10, 10], [10, 10, 10], [10, 10, 10]], 30),
            ([[9, 7, 3], [4, 12, 6], [8, 5, 11]], 32),
            ([[20, 25, 30], [22, 27, 35], [24, 20, 28]], 90),
        ]
        for matrix, expected_cost in test_cases:
            with self.subTest(matrix=matrix):  # ������� � ������ �������� ���������� ����
                result = solve_assignment(matrix, maximize=True)  # �������� � ���������� ������������
                self.assertEqual(result['total_cost'], expected_cost)  # �������� ����������
                self.assertEqual(len(result['assignment']), len(matrix))  # ��������, ��� ��� ������������

    def test_invalid_input(self):
        # ����� ��� ��������� ������������ ������
        invalid_cases = [
            [["a", "b"], [3, 4]],  # ������ ������ �����
            [[1, 2], [3]],  # ������������� �����������
            [],  # ������ �������
            [[1, 2, 3], [4, 5]],  # �� ����������
            [[None, 2], [3, 4]],  # None � �������
        ]
        for case in invalid_cases:
            with self.subTest(case=case):  # ������� ��� ������� �����
                with self.assertRaises((ValueError, TypeError)):  # �������, ��� ����� ������ (������� ��� ����������)
                    solve_assignment(case)  # �������� ������ � ������ ������

# ���� ���� ���� ����������� �������� � ��������� ��� �����
if __name__ == '__main__':
    unittest.main()
