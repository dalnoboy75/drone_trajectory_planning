import numpy as np


def CalculationBottomLimit(new_matrix: np.ndarray, bottomLimit: int) -> int:
    "Принимает на вход матрицу с расстояниями и высчитывает НГЦФ"

    # Пропустим первую строку и первый столбец
    sub_matrix = new_matrix[1:, 1:]

    # Находим минимумы по строкам и столбцам подматрицы
    row_min = sub_matrix.min(axis=1)
    sub_matrix -= row_min[:, np.newaxis]
    columns_min = sub_matrix.min(axis=0)
    sub_matrix -= columns_min

    # Суммируем минимумы
    substractSum = sum(row_min) + sum(columns_min)

    # Обновляем нижнюю границу
    bottomLimit += substractSum

    new_matrix[1:, 1:] = sub_matrix
    return bottomLimit


def SerachingMaxDegreeZero(new_matrix: np.ndarray, max_coeff: int) -> (list, int):
    "Передаем матрицу, считаем максимальную степень нуля и возвращаем индексы, под которыми находится этот ноль в матрице"
    # Список координат нулевых элементов
    zeros = []
    # Список их коэффициентов
    coeff_list = []

    # Поиск нулевых элементов
    for i in range(1, new_matrix.shape[0]):
        for j in range(1, new_matrix.shape[1]):
            # Если равен нулю
            if new_matrix[i, j] == 0:
                # Добавление в список координат
                zeros.append((new_matrix[i][0], new_matrix[0][j]))
                # Расчет коэффициента и добавление в список
                coeff = get_coefficient(new_matrix, i, j)
                coeff_list.append(coeff)
                # Сравнение с максимальным
                max_coeff = max(max_coeff, coeff)

    length = len(zeros)
    i = 0
    cnt = 0
    while cnt != length:
        if coeff_list[i] != max_coeff:
            del zeros[i]
            del coeff_list[i]
        else:
            i += 1

        cnt += 1
    return zeros, max_coeff

def get_coefficient(m: np.ndarray, r: int, c: int) -> int:
    "На вход получаем матрицу и номер столбца и строки матрицы, в которой под индексами [r][c] содержится в матрице 0, на выходе получаем его коэффицент"
    rmin = cmin = float('inf')

    # Обход строки и столбца
    for i in range(1, m.shape[0]):
        if i != r:
            rmin = min(rmin, m[i, c])
        if i != c:
            cmin = min(cmin, m[r, i])
    return rmin + cmin

def DeleteEdge(zeros: list, new_matrix: np.ndarray, bottomLimit, max_coeff: int) -> (np.ndarray, int):
    "На вход получаем индексы элемента, который имеет наибольший наибольшую степень нуля, удаляем строку и столбец с этими индексами, возвращаем измененную матрицу"

    edge = zeros[0]
    new_matrix[1:, edge[1]] -= max_coeff
    new_matrix[edge[0]][edge[1]] = 10 ** 8
    bottomLimit += max_coeff
    new_matrix = np.delete(new_matrix, edge[0], axis=0)  # Удаляем строку
    new_matrix = np.delete(new_matrix, edge[1], axis=1)  # Удаляем столбец
    return new_matrix, bottomLimit


def algorithm_Lit(numbers: list) -> np.ndarray:
    max_coeff = 0
    ListDanglingBranches = []
    bottomLimit = 0
    matrix = np.array(numbers).reshape(int(len(numbers) ** 0.5), int(len(numbers) ** 0.5))
    lines = int(len(numbers) ** 0.5)
    columns = int(len(numbers) ** 0.5)
    list_column = np.arange(1, columns + 1).reshape(-1, 1)  # столбец из элементов от 1 до n
    list_row = np.arange(0, columns + 1).reshape(1, -1)  # строка из элементов от 0 до n
    new_matrix = matrix
    new_matrix = np.hstack((np.array(list_column), new_matrix))
    new_matrix = np.vstack((np.array(list_row), new_matrix))
    bottomLimit = CalculationBottomLimit(new_matrix, bottomLimit)
    zeros, max_coeff = SerachingMaxDegreeZero(new_matrix, max_coeff)
    # Создание нашей новой матрицы
    new_matrix, bottomLimit_in = DeleteEdge(zeros, new_matrix, bottomLimit, max_coeff)

    bottomLimit_not_in = CalculationBottomLimit(new_matrix, bottomLimit)
    print('12312312', bottomLimit_in)
    if bottomLimit_in > bottomLimit_not_in:
        index_j = np.where(new_matrix[0] == zeros[0][0])[0]
        index_i = np.where(new_matrix[:, 0] == zeros[0][1])[0]
        new_matrix[index_i[0]][index_j[0]] = 10**8
    #     zeros = SerachingMaxDegreeZero(new_matrix)


    return new_matrix


numbers = [10 ** 8, 20, 18, 12, 8, 5, 10 ** 8, 14, 7, 11, 12, 18, 10 ** 8, 6, 11, 11, 17, 11, 10 ** 8, 12, 5, 5, 5, 5,
           10 ** 8]
print(algorithm_Lit(numbers))
# list_column = [[1], [2]]
# list_row = [[0, 1, 2]]
#
# matrix = np.hstack((np.array(list_column), matrix))
# matrix = np.vstack((np.array(list_row), matrix))
# n = 5  # Задайте нужное значение n
# new_column = np.arange(1, n + 1).reshape(-1, 1)  # Создаем столбец с элементами от 1 до n
# print(new_column)
