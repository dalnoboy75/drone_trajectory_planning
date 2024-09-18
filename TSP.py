import numpy as np
from itertools import permutations


def find_min_route(numbers):
    matrix = np.array(numbers).reshape(int(len(numbers)**0.5), int(len(numbers)**0.5))
    lines = int(len(numbers)**0.5)
    columns = int(len(numbers) ** 0.5)

    x = list(range(1, lines + 1))
    number_solutions = list(permutations(x))
    if len(number_solutions) == 1:  # проверка на пустоту списка
        return "Нет циклов"

    # Нахождение оценки снизу
    result = np.array(numbers).reshape(int(len(numbers)**0.5), int(len(numbers)**0.5))
    row_mins = matrix.min(axis=1)
    result -= row_mins[:, np.newaxis]
    columns_mins = result.min(axis=0)
    result -= columns_mins
    low_mark = sum(row_mins) + sum(columns_mins)


    if len(number_solutions) == 1:  # проверка на пустоту списка
        return "Нет циклов"

    route_data = []

    for i in number_solutions:
        sum_length = 0
        for j in range(len(i)):
            if j == len(i) - 1:
                sum_length += matrix[i[j] - 1][i[0] - 1]
            else:
                sum_length += matrix[i[j] - 1][i[j + 1] - 1]
        route_data.append((sum_length, i))

    return min(route_data), low_mark


# find_min_route([10**8, 5, 16, 14, 13, 10**8, 6, 9, 10, 12, 10**8, 11, 8, 15, 7, 10**8])
# result = find_min_route([], 0, 0)
# print(result)
#
#print(find_min_route([10**8, 5, 16, 14, 13, 10**8, 6, 9, 10, 12, 10**8, 11, 8, 15, 7, 10**8]))
# print(find_min_route([10**8, 1, 2, 3, 4, 14, 10**8, 15, 16, 5, 13, 20, 10**8, 17, 6, 12, 19, 18, 10**8, 7, 11, 10, 9, 8, 10**8]))
# print(find_min_route([10**8, 5, 7, 16, 10**8, 2, 4, 6, 10**8]))
# print(find_min_route([]))