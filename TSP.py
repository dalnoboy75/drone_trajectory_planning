import numpy as np
from itertools import permutations

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

    for i in number_solutions:
        sum_length = 0
        for j in range(len(i)):
            if j == len(i) - 1:
                sum_length += numbers[i[j] - 1][i[0] - 1]
            else:
                sum_length += numbers[i[j] - 1][i[j + 1] - 1]
        route_data.append((sum_length, i))

    return min(route_data), low_mark
#
# numbers = np.array(
#         [
#             [INF, 20, 18, 12, 8],
#             [5, INF, 14, 7, 11],
#             [12, 18, INF, 6, 11],
#             [11, 17, 11, INF, 12],
#             [5, 5, 5, 5, INF],
#         ]
#     )
# print(find_min_route(numbers))
#
#print(find_min_route([10**8, 5, 16, 14, 13, 10**8, 6, 9, 10, 12, 10**8, 11, 8, 15, 7, 10**8]))
# print(find_min_route([10**8, 1, 2, 3, 4, 14, 10**8, 15, 16, 5, 13, 20, 10**8, 17, 6, 12, 19, 18, 10**8, 7, 11, 10, 9, 8, 10**8]))
# print(find_min_route([10**8, 5, 7, 16, 10**8, 2, 4, 6, 10**8]))
# print(find_min_route([]))