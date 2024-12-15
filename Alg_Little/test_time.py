import random
import timeit
import numpy as np
from Alg_L_Classes import algorithm_Lit
from TSP import find_min_route
import copy
import datetime


INF = 10**8
kolvo_airfields = 1


def test_right_p(numbers):
    result_2 = find_min_route(numbers)
    return result_2
def test_right_paths(numbers, start_airfield):
    result = algorithm_Lit(numbers, start_airfield, kolvo_airfields)
    return result

with open('answers.txt', 'a') as file, open("execution_time.txt", 'a') as f:
    size = 10
    for i in range(2):

        # Создаем матрицу с рандомными числами
        matrix = np.random.randint(1, 100, size=(size, size))

        # Устанавливаем INF на главной диагонали
        np.fill_diagonal(matrix, INF)
        matrix_tsp = copy.deepcopy(matrix)
        matrix_alg_lit = copy.deepcopy(matrix)
        start_airfield = matrix_alg_lit.shape[0]

        # Измеряем время выполнения функции test_right_p
        execution_time_1 = timeit.timeit(lambda: test_right_p(matrix_tsp), number=1)

        # Измеряем время выполнения функции test_right_paths
        execution_time_2 = timeit.timeit(lambda: test_right_paths(matrix_alg_lit, start_airfield), number=1)

        res_tsp = test_right_p(matrix_tsp)
        res_alg_lit = test_right_paths(matrix_alg_lit, start_airfield)

        file.write(f"{'res_tsp:', res_tsp, 'res_alg_lit:', res_alg_lit}\n")
        
        # Получаем текущий таймстемп
        timestamp = datetime.datetime.now().isoformat()
        
        # Записываем данные в файл
        f.write(f"Size: {size}, Algorithm: TSP, Timestamp: {timestamp}, Execution Time: {execution_time_1} seconds\n")
        f.write(f"Size: {size}, Algorithm: Alg_Lit, Timestamp: {timestamp}, Execution Time: {execution_time_2} seconds\n")


    
     
# print(test_right_paths())
# print(20*'-')
# print(test_right_p())
# # Измерим время выполнения функции
# execution_time_1 = timeit.timeit(test_right_paths, number=1)
# execution_time_2 = timeit.timeit(test_right_p, number=1)


# # Записываем время выполнения в файл
# with open("execution_time.txt", "w") as f:
#     f.write(f"Execution time 1: {execution_time_1} second\n")
#     f.write(f"Execution time 2: {execution_time_2} second\n")