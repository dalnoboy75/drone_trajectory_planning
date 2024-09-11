import numpy as np
from itertools import permutations


def find_min_route(numbers, lines, columns):
    # Считываем числа от пользователя
    # numbers = input("Введите числа, разделенные пробелами: ")

    # Преобразуем строку в список чисел
    number_list = [np.inf if x == 1e9 else int(x) for x in numbers]

    # Определяем размерность матрицы
    # lines = int(input("Введите количество строк: "))
    # columns = int(input("Введите количество столбцов: "))

    # Проверяем, достаточно ли чисел для создания матрицы
    if len(number_list) != lines * columns:
        return "Ошибка: количество чисел не соответствует размерности матрицы."

    # Создаем матрицу
    matrix = np.array(number_list).reshape(columns, lines)

    x = list(range(1, lines + 1))
    number_solutions = list(permutations(x))
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

    return min(route_data)


# result = find_min_route([], 0, 0)
# print(result)
