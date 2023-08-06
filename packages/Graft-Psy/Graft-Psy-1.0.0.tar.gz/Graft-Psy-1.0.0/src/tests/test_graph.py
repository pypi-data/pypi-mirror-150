import unittest

from src.graph import Graph, Period


class GraphTestCase(unittest.TestCase):
    def test_graph(self):
        graph = Graph(1, 2)
        self.assertEqual(graph(3), 0)
        self.assertIsInstance(graph(lb=0, ub=10), Period)


class PeriodTestCase(unittest.TestCase):
    def test_period(self):
        self.assertRaises(ValueError, Period, None, 2, 1)
        one_two = Period(None, 1, 2)
        three = Period(None, 3, None)
        self.assertRaises(ValueError, one_two.__rshift__, three)
        self.assertRaises(TypeError, one_two.__rshift__, 5)

    def test_periodic(self):
        periodic = Period(None, None, 1) >> Period(None, 1, 2)
        three_four = Period(None, 3, 4)
        self.assertRaises(ValueError, periodic.__rshift__, three_four)
        self.assertRaises(TypeError, periodic.__rshift__, 5)


if __name__ == '__main__':
    unittest.main()
