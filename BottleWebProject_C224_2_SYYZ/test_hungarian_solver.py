import unittest
from hungarian_solver import solve_assignment


class TestHungarianSolver(unittest.TestCase):

    def test_minimization_cases(self):
        matrix1 = [
            [4, 2, 8],
            [2, 3, 7],
            [3, 1, 6]
        ]
        result = solve_assignment(matrix1)
        self.assertEqual(result['total_cost'], 10)
        self.assertEqual(len(result['assignment']), 3)

        matrix2 = [
            [1, 2, 3],
            [3, 2, 1],
            [2, 1, 3]
        ]
        result = solve_assignment(matrix2)
        self.assertEqual(result['total_cost'], 3)

        matrix3 = [
            [5, 9, 7],
            [8, 1, 4],
            [6, 3, 2]
        ]
        result = solve_assignment(matrix3)
        self.assertEqual(result['total_cost'], 8)

    def test_maximization_cases(self):
        matrix4 = [
            [4, 2, 8],
            [2, 3, 7],
            [3, 1, 6]
        ]
        result = solve_assignment(matrix4, maximize=True)
        self.assertEqual(result['total_cost'], 14)

        matrix5 = [
            [15, 30, 5],
            [20, 25, 10],
            [10, 35, 40]
        ]
        result = solve_assignment(matrix5, maximize=True)
        self.assertEqual(result['total_cost'], 90)

        matrix6 = [
            [10, 10, 10],
            [10, 10, 10],
            [10, 10, 10]
        ]
        result = solve_assignment(matrix6, maximize=True)
        self.assertEqual(result['total_cost'], 30)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            solve_assignment([["a", "b"], [3, 4]])

        with self.assertRaises(ValueError):
            solve_assignment([[1, 2], [3]])

        with self.assertRaises(ValueError):
            solve_assignment([])

if __name__ == '__main__':
    unittest.main()
