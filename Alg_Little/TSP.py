import numpy as np
from itertools import permutations
import timeit

INF = 10**8
def find_min_route(numbers):
    lines = numbers.shape[0]

    x = list(range(1, lines + 1))
    number_solutions = list(permutations(x))
    if len(number_solutions) == 1:  # проверка на пустоту списка
        return "Нет циклов"

    # Нахождение оценки снизу
    row_mins = numbers.min(axis=1)
    numbers -= row_mins[:, np.newaxis]
    columns_mins = numbers.min(axis=0)
    numbers -= columns_mins
    low_mark = sum(row_mins) + sum(columns_mins)


    if len(number_solutions) == 1:  # проверка на пустоту списка
        return "Нет циклов"

    route_data = []

    number_solutions = list(permutations(x))
    for i in number_solutions:
        sum_length = 0
        for j in range(len(i)):
            if j == len(i) - 1:
                sum_length += numbers[i[j] - 1][i[0] - 1]
            else:
                sum_length += numbers[i[j] - 1][i[j + 1] - 1]
        route_data.append((int(sum_length), i))
    return min(route_data), int(low_mark)

# size = 10
# matrix = np.random.randint(1, 100, size=(size, size))
# np.fill_diagonal(matrix, INF)
# start_airfield = matrix.shape[0]
# execution_time_2 = timeit.timeit(lambda: find_min_route(matrix), number=1)
# print(execution_time_2)