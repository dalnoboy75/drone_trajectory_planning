import numpy as np
from Alg_L_Classes import algorithm_Lit


def test_2_right_paths():
    numbers = np.array(
        [[0, 1, 2, 3, 4, 5], [1, 10 ** 8, 20, 18, 12, 8], [2, 5, 10 ** 8, 14, 7, 11], [3, 12, 18, 10 ** 8, 6, 11],
         [4, 11, 17, 11, 10 ** 8, 12],
         [5, 5, 5, 5, 5, 10 ** 8]])
    result = algorithm_Lit(numbers)
    answer = [(1, 5), (5, 3), (3, 4), (4, 2), (2, 1)]
    assert result == answer