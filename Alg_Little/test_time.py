import random
import timeit
import numpy as np
from Alg_L_Classes import algorithm_Lit
from TSP import find_min_route


INF = 10**8


# def rand_znach():
#     max_size = 30
#
#     # Создаем случайную матрицу размером max_size x max_size
#     matrix_size = np.random.randint(3, max_size + 1)  # случайный размер от 1 до 30
#     matrix = np.random.rand(matrix_size, matrix_size)
#     size = matrix.shape[0]
#     np.fill_diagonal(matrix, INF)
#     for i in range(matrix_size):
#         for j in range(matrix_size):
#             if i != j:
#                 matrix[i, j] = np.random.rand()
#
#     st = size - 1
#
#     kolvo = random.choice(range(2, 13, 2))
#
#     return matrix, st, kolvo
#
#
# numbers, start_airfield, kolvo_airfields = rand_znach()
#
# print(numbers, start_airfield, kolvo_airfields)



def test_right_p():
    numbers = np.array(
        [
            [INF, 20, 18, 12, 8],
            [5, INF, 14, 7, 11],
            [12, 18, INF, 6, 11],
            [11, 17, 11, INF, 12],
            [5, 5, 5, 5, INF],
        ]
    )
    result_2 = find_min_route(numbers)
    return result_2
def test_right_paths():
    numbers = np.array(
        [
            [INF, 20, 18, 12, 8],
            [5, INF, 14, 7, 11],
            [12, 18, INF, 6, 11],
            [11, 17, 11, INF, 12],
            [5, 5, 5, 5, INF],
        ]
    )
    start_airfield = 4
    kolvo_airfields = 4
    result = algorithm_Lit(numbers, start_airfield, kolvo_airfields)
    return result



# Измерим время выполнения функции
execution_time_1 = timeit.timeit(test_right_paths, number=1)
execution_time_2 = timeit.timeit(test_right_p, number=1)


# Записываем время выполнения в файл
with open("execution_time.txt", "w") as f:
    f.write(f"Execution time 1: {execution_time_1} second\n")
    f.write(f"Execution time 2: {execution_time_2} second\n")
