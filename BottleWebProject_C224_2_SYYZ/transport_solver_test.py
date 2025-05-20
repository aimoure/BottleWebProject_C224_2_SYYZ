import unittest
import numpy as np
from transport_solver import northwest_corner_method, has_cycle, get_basis, calculate_potentials, find_cycle, optimize_transportation

class TestTransportation(unittest.TestCase):

    def test_northwest_corner_method(self):
        # Test case 1: Basic case
        cost_matrix = np.array([[1, 2, 3], [4, 5, 6]])
        supply = np.array([10, 20])
        demand = np.array([5, 10, 15])
        expected_plan = np.array([[5, 5, 0], [0, 5, 15]])
        result = northwest_corner_method(cost_matrix, supply, demand)
        np.testing.assert_array_equal(result, expected_plan)

        # Test case 2: Equal supply and demand
        cost_matrix = np.array([[1, 2], [3, 4]])
        supply = np.array([10, 10])
        demand = np.array([10, 10])
        expected_plan = np.array([[10, 0], [0, 10]])
        result = northwest_corner_method(cost_matrix, supply, demand)
        np.testing.assert_array_equal(result, expected_plan)

        # Test case 3: Single supplier and consumer
        cost_matrix = np.array([[5]])
        supply = np.array([10])
        demand = np.array([10])
        expected_plan = np.array([[10]])
        result = northwest_corner_method(cost_matrix, supply, demand)
        np.testing.assert_array_equal(result, expected_plan)

    def test_has_cycle(self):
        # Test case 1: Basis with a cycle
        basis = [(0, 0), (0, 1), (1, 0), (1, 1)]
        self.assertTrue(has_cycle(basis))

        # Test case 2: Basis without a cycle
        basis = [(0, 0), (0, 1), (1, 1)]
        self.assertFalse(has_cycle(basis))

        # Test case 3: Empty basis
        basis = []
        self.assertFalse(has_cycle(basis))

    def test_get_basis(self):
        # Test case 1: Basic plan with enough basis cells
        plan = np.array([[5, 0], [0, 5]])
        cost_matrix = np.array([[1, 2], [3, 4]])
        expected_basis = [(0, 0), (1, 1)]
        result = get_basis(plan, cost_matrix)
        self.assertEqual(set(result), set(expected_basis))

        # Test case 2: Plan needing additional zero cells
        plan = np.array([[10, 0], [0, 0]])
        cost_matrix = np.array([[1, 2], [3, 4]])
        expected_basis = [(0, 0), (1, 0)]  # Adds (1, 0) due to lower cost
        result = get_basis(plan, cost_matrix)
        self.assertEqual(set(result), set(expected_basis))

    def test_calculate_potentials(self):
        # Test case 1: Basic basis
        cost_matrix = np.array([[1, 2], [3, 4]])
        basis = [(0, 0), (0, 1), (1, 1)]
        u, v = calculate_potentials(cost_matrix, basis)
        expected_u = [0, 2]
        expected_v = [1, 2]
        np.testing.assert_array_almost_equal(u, expected_u)
        np.testing.assert_array_almost_equal(v, expected_v)

        # Test case 2: Single cell basis
        cost_matrix = np.array([[5]])
        basis = [(0, 0)]
        u, v = calculate_potentials(cost_matrix, basis)
        expected_u = [0]
        expected_v = [5]
        np.testing.assert_array_almost_equal(u, expected_u)
        np.testing.assert_array_almost_equal(v, expected_v)

    def test_find_cycle(self):
        # Test case 1: Basis with a cycle
        basis = [(0, 0), (0, 1), (1, 0), (1, 1)]
        start = (0, 0)
        result = find_cycle(basis, start)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 4)

        # Test case 2: Basis without forming a cycle with start
        basis = [(0, 0), (0, 1), (1, 1)]
        start = (1, 0)
        result = find_cycle(basis, start)
        self.assertIsNone(result)

    def test_optimize_transportation(self):
        # Test case 1: Basic optimization
        cost_matrix = [[1, 2, 3], [4, 5, 6]]
        supply = [10, 20]
        demand = [5, 10, 15]
        plan, total_cost = optimize_transportation(cost_matrix, supply, demand)
        expected_plan = [[5, 5, 0], [0, 5, 15]]
        expected_cost = 100  # 5*1 + 5*2 + 5*5 + 15*6
        np.testing.assert_array_almost_equal(plan, expected_plan)
        self.assertAlmostEqual(total_cost, expected_cost)

        # Test case 2: Optimal from start
        cost_matrix = [[1, 2], [3, 4]]
        supply = [10, 10]
        demand = [10, 10]
        plan, total_cost = optimize_transportation(cost_matrix, supply, demand)
        expected_plan = [[10, 0], [0, 10]]
        expected_cost = 50  # 10*1 + 10*4
        np.testing.assert_array_almost_equal(plan, expected_plan)
        self.assertAlmostEqual(total_cost, expected_cost)

    def test_invalid_input(self):
        # Test invalid cost matrix
        with self.assertRaises(ValueError):
            optimize_transportation([["a", "b"], [3, 4]], [10, 10], [10, 10])

        # Test mismatched supply and demand
        with self.assertRaises(ValueError):
            optimize_transportation([[1, 2], [3, 4]], [10], [10, 10])

        # Test empty input
        with self.assertRaises(ValueError):
            optimize_transportation([], [], [])

if __name__ == '__main__':
    unittest.main()
