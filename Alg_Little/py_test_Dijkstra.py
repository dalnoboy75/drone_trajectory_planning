import unittest
from Algorithm_Dijkstra import dijkstra


class TestDijkstra(unittest.TestCase):
    def test_shortest_path(self):
        n = 5
        m = 6
        edges = [(1, 2, 1), (1, 3, 4), (2, 3, 2), (2, 4, 5), (3, 4, 1), (4, 5, 3)]
        s = 1
        t = 5
        distance, path = dijkstra(n, m, s, t, edges)
        self.assertEqual(distance, 7)
        self.assertEqual(path, [1, 2, 3, 4, 5])

    def test_no_path(self):
        n = 3
        m = 2
        edges = [(1, 2, 1), (2, 3, 1)]
        s = 1
        t = 3
        distance, path = dijkstra(n, m, s, t, edges)
        self.assertEqual(distance, 2)
        self.assertEqual(path, [1, 2, 3])

    def test_disconnected_graph(self):
        n = 4
        m = 1
        edges = [(1, 2, 1)]
        s = 1
        t = 3
        distance, path = dijkstra(n, m, s, t, edges)
        self.assertEqual(distance, -1)
        self.assertEqual(path, [])

    def test_medium_graph(self):
        n = 5
        m = 7
        s = 2
        t = 5
        edges = [
            (1, 2, 1),
            (1, 3, 4),
            (1, 5, 5),
            (2, 3, 1),
            (3, 4, 2),
            (3, 5, 3),
            (4, 5, 7),
        ]
        distance, path = dijkstra(n, m, s, t, edges)
        self.assertEqual(distance, 4)
        self.assertEqual(path, [2, 3, 5])


if __name__ == "__main__":
    unittest.main()
