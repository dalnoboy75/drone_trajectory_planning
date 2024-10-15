import pytest
import numpy as np
from Alg_L_Classes import AlgLittle, algorithm_Lit

def test_1_include_and_exclude_Edge():
    numbers = np.array([[0, 1, 2, 3, 4, 5], [1, 10 ** 8, 20, 18, 12, 8], [2, 5, 10 ** 8, 14, 7, 11], [3, 12, 18, 10 ** 8, 6, 11],
     [4, 11, 17, 11, 10 ** 8, 12],
     [5, 5, 5, 5, 5, 10 ** 8]])

    node = AlgLittle(new_matrix=numbers)
    cnt = 0
    node.reduce()
    list_hmin = [(35, 41), (42, 44), (41, 47), (41, 50), (41, 56)]
    for i in range(5):
        max_coeff = 0
        zeros, max_coeff = node.SearchingMaxDegreeZero(max_coeff)
        node_include, node_exclude = node, node
        node_include = node_include.include_edge(zeros)
        node_exclude = node_exclude.delete_edge(zeros, max_coeff)

        node_include.discarded_nodes.append(node_exclude)
        node_exclude.discarded_nodes.append(node_include)
        assert node_include.hmin == list_hmin[i][0]
        assert node_exclude.hmin == list_hmin[i][1]
        all_possible_plans = node.discarded_nodes + [node_exclude, node_include]
        cnt += 1
        if cnt == 1:
            node_exclude.discarded_nodes = []
        next_node = min(all_possible_plans, key=lambda node: node.hmin)
        node = next_node

def test_2_right_paths():
    numbers = np.array(
        [[0, 1, 2, 3, 4, 5], [1, 10 ** 8, 20, 18, 12, 8], [2, 5, 10 ** 8, 14, 7, 11], [3, 12, 18, 10 ** 8, 6, 11],
         [4, 11, 17, 11, 10 ** 8, 12],
         [5, 5, 5, 5, 5, 10 ** 8]])
    result = algorithm_Lit(numbers)
    answer = [[5, 2, False], [4, 2, True], [1, 5, True], [2, 1, True]]
    assert result == answer

