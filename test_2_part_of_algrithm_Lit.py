import pytest
import numpy as np
from algorithm_Littla import CalculationBottomLimit, SerachingMaxDegreeZero, get_coefficient, DeleteEdge, algorithm_Lit

max_coeff = 0


def test_2_CalculationBottomLimit():
    matrix = np.array(
        [[0, 1, 2, 3, 4, 5], [1, 10 ** 8, 20, 18, 12, 8], [2, 5, 10 ** 8, 14, 7, 11], [3, 12, 18, 10 ** 8, 6, 11],
         [4, 11, 17, 11, 10 ** 8, 12],
         [5, 5, 5, 5, 5, 10 ** 8]])
    bottom_limit = 0
    result = CalculationBottomLimit(matrix, bottom_limit)
    assert result == 35  # Ожидаемое значение нижней границы


def test_1_SerachingMaxDegreeZero():
    matrix = np.array(
        [[0, 1, 2, 3, 4, 5], [1, 99999992, 12, 10, 4, 0], [2, 0, 99999995, 9, 2, 6], [3, 6, 12, 99999994, 0, 5],
         [4, 0, 6, 0, 99999989, 1], [5, 0, 0, 0, 0, 99999995]])
    global max_coeff
    expected_max_coeff = 6
    expected_zeros = [(5, 2)]  # Ожидаемые индексы
    result, max_coeff = SerachingMaxDegreeZero(matrix, max_coeff)
    assert result == expected_zeros
    assert expected_max_coeff == max_coeff


def test_1_get_coefficient():
    matrix = np.array([[0, 1, 3, 4, 5], [1, 99999992, 10, 4, 0], [2, 0, 9, 2, 100000000], [3, 6, 99999994, 0, 5],
                       [4, 0, 0, 99999989, 1]])
    array_r_and_c = [(1, 4), (2, 1), (3, 3), (4, 1), (4, 2)]
    right_sum_rmin_and_cmin = [5, 2, 7, 0, 9]
    result = []
    for i in range(5):
        result.append(get_coefficient(matrix, array_r_and_c[i][0], array_r_and_c[i][1]))
    assert set(right_sum_rmin_and_cmin) == set(result)


def test_2_DeleteEdge():
    matrix = np.array(
        [[0, 1, 2, 3, 4, 5], [1, 99999992, 12, 10, 4, 0], [2, 0, 99999995, 9, 2, 6], [3, 6, 12, 99999994, 0, 5],
         [4, 0, 6, 0, 99999989, 1], [5, 0, 0, 0, 0, 99999995]])
    zeros = [(5, 2)]
    bottom_limit = 35
    new_matrix, new_bottom_limit = DeleteEdge(zeros, matrix, bottom_limit, max_coeff)
    assert new_bottom_limit == 41  # Ожидаемое значение нижней границы
    assert np.any(new_matrix == [[0, 1, 3, 4, 5], [1, 99999992, 10, 4, 0], [2, 0, 9, 2, 6], [3, 6, 99999994, 0, 5],
                                 [4, 0, 0, 99999989, 1]])  # Проверяем, что размер матрицы уменьшился


def test_2_algorithm_Lit():
    numbers = [10 ** 8, 20, 18, 12, 8, 5, 10 ** 8, 14, 7, 11, 12, 18, 10 ** 8, 6, 11, 11, 17, 11, 10 ** 8, 12, 5, 5, 5,
               5,
               10 ** 8]
    result = algorithm_Lit(numbers)
    assert np.any(result == [[0, 1, 3, 4, 5], [1, 99999992, 10, 4, 0], [2, 0, 9, 2, 100000000], [3, 6, 99999994, 0, 5],
                             [4, 0, 0, 99999989, 1]])  # Проверяем, что размер матрицы соответствует ожидания
