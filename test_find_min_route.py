import pytest
import numpy as np
from TSP import find_min_route


def test_valid_case():
    numbers = [10**8, 5, 7, 16, 10**8, 2, 4, 6, 10**8]
    expected = ((11, (1, 2, 3)), 11)
    assert find_min_route(numbers) == expected

#
def test_empty_permutations():
    numbers = []
    expected = "Нет циклов"
    assert find_min_route(numbers) == expected


def test_inf_value():
    numbers = [10**8, 5, 16, 14, 13, 10**8, 6, 9, 10, 12, 10**8, 11, 8, 15, 7, 10**8]
    expected = ((30, (1, 2, 3, 4)), 29)  # пример ожидаемого результата
    assert find_min_route(numbers) == expected

def test_inf_value_1():
    numbers = [10**8, 1, 2, 3, 4, 14, 10**8, 15, 16, 5, 13, 20, 10**8, 17, 6, 12, 19, 18, 10**8, 7, 11, 10, 9, 8, 10**8]
    expected = ((42, (1, 2, 3, 5, 4)), 31)  # пример ожидаемого результата
    assert find_min_route(numbers) == expected
