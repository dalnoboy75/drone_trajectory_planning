import pytest
import numpy as np
from algorithm_Littla import CalculationBottomLimit, SerachingMaxDegreeZero,get_coefficient, DeleteEdge, algorithm_Lit

max_coeff = 0
def test_1_CalculationBottomLimit():
    matrix = np.array([[10**8, 2, 3], [4, 10**8, 6], [7, 8, 10**8]])
    bottom_limit = 0
    result = CalculationBottomLimit(matrix, bottom_limit)
    assert result == 14  # Ожидаемое значение нижней границы

def test_1_SerachingMaxDegreeZero():
    matrix = np.array([[0, 1, 2, 3], [1, 99999998, 0, 0], [2, 0, 99999996, 1], [3, 0, 1, 99999992]])
    global max_coeff
    expected_max_coeff = 1
    expected_zeros = [(1, 2), (1, 3), (2, 1), (3, 1)]  # Ожидаемые индексы
    result, max_coeff = SerachingMaxDegreeZero(matrix, max_coeff)
    assert result == expected_zeros
    assert max_coeff == 1

def test_1_get_coefficient():
    matrix = np.array([[0, 1, 2, 3], [1, 99999998, 0, 0], [2, 0, 99999996, 1], [3, 0, 1, 99999992]])
    r = 3
    c = 1
    expected_rmin_cmin = 1
    result = get_coefficient(matrix, r, c)
    assert result == expected_rmin_cmin
def test_1_DeleteEdge():
    global max_coeff
    matrix = np.array([[0, 1, 2, 3], [1, 99999998, 0, 0], [2, 0, 99999996, 1], [3, 0, 1, 99999992]])
    zeros = [(1, 2), (1, 3), (2, 1), (3, 1)]
    bottom_limit = 14
    new_matrix, new_bottom_limit = DeleteEdge(zeros, matrix, bottom_limit, max_coeff)
    assert new_bottom_limit == 15  # Ожидаемое значение нижней границы
    assert np.any(new_matrix == [[0, 1, 3], [2, 0, 1], [3, 0, 99999992]])   # Проверяем, что размер матрицы уменьшился

def test_1_algorithm_Lit():
    numbers = [10 ** 8, 2, 3, 4, 10 ** 8, 6, 7, 8, 10 ** 8]
    result = algorithm_Lit(numbers)
    assert np.any(result == [[0, 1, 3], [2, 0, 0], [3, 0, 99999991]])  # Проверяем, что размер матрицы соответствует ожиданиям
