import pytest
import numpy as np
from TSP import find_min_route


def test_valid_case():
    numbers = [1e9, 5, 7, 16, 1e9, 2, 4, 6, 1e9]
    lines = 3
    columns = 3
    expected = (11, (1, 2, 3))
    assert find_min_route(numbers, lines, columns) == expected


def test_invalid_matrix_size():
    numbers = [0, 10, 15]
    lines = 2
    columns = 2
    expected = "Ошибка: количество чисел не соответствует размерности матрицы."
    assert find_min_route(numbers, lines, columns) == expected


#
def test_empty_permutations():
    numbers = []
    lines = 0
    columns = 0
    expected = "Нет циклов"
    assert find_min_route(numbers, lines, columns) == expected


def test_inf_value():
    numbers = [1e9, 5, 16, 14, 13, 1e9, 6, 9, 10, 12, 1e9, 11, 8, 15, 7, 1e9]
    lines = 4
    columns = 4
    expected = (30, (1, 2, 3, 4))  # пример ожидаемого результата
    assert find_min_route(numbers, lines, columns) == expected
