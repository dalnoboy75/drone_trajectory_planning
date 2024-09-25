import numpy as np

bottomLimit = 0
record = np.inf


def get_coefficient(m, r, c):
    rmin = cmin = float('inf')

    # Обход строки и столбца
    for i in range(m.shape[0]):
        if i != r:
            rmin = min(rmin, m[i, c])
        if i != c:
            cmin = min(cmin, m[r, i])

    return rmin + cmin

def algorithm_Lit(numbers):
    global bottomLimit, record
    matrix = np.array(numbers).reshape(int(len(numbers) ** 0.5), int(len(numbers) ** 0.5))
    lines = int(len(numbers) ** 0.5)
    columns = int(len(numbers) ** 0.5)
    list_column = np.arange(1, columns + 1).reshape(-1, 1)  # столбец из элементов от 1 до n
    list_row = np.arange(0, columns + 1).reshape(1, -1)  # строка из элементов от 0 до n
    row_min = matrix.min(axis=1)
    matrix -= row_min[:, np.newaxis]
    columns_min = matrix.min(axis=0)
    matrix -= columns_min
    substractSum = sum(row_min) + sum(columns_min)
    bottomLimit += substractSum

    if bottomLimit > record:  # сравнение верхней и нижней границ
        return

    # Список координат нулевых элементов
    zeros = []
    # Список их коэффициентов
    coeff_list = []

    # Максимальный коэффициент
    max_coeff = 0
    # Поиск нулевых элементов
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            # Если равен нулю
            if matrix[i, j] == 0:
                # Добавление в список координат
                zeros.append((i, j))
                # Расчет коэффициента и добавление в список
                coeff = get_coefficient(matrix, i, j)
                coeff_list.append(coeff)
                # Сравнение с максимальным
                max_coeff = max(max_coeff, coeff)

    length = len(zeros)
    i = 0
    print(len(zeros), len(coeff_list))
    cnt = 0
    while cnt != length:
        if coeff_list[i] != max_coeff:
            del zeros[i]
            del coeff_list[i]
        else:
            i += 1

        cnt += 1

    # Переход к множеству, содержащему ребро с максимальным штрафом
    edge = zeros[0]
    new_matrix = matrix
    print(new_matrix)
    new_matrix = np.hstack((np.array(list_column), new_matrix))
    new_matrix = np.vstack((np.array(list_row), new_matrix))
    new_matrix[edge[1] + 1][edge[0] + 1] = -1
    new_matrix = np.delete(new_matrix, edge[0] + 1, axis=0)  # Удаляем строку
    new_matrix = np.delete(new_matrix, edge[1] + 1, axis=1)  # Удаляем столбец

    return new_matrix



numbers = [10**8, 5, 7, 16, 10**8, 2, 4, 6, 10**8]
print(algorithm_Lit(numbers))
# list_column = [[1], [2]]
# list_row = [[0, 1, 2]]
#
# matrix = np.hstack((np.array(list_column), matrix))
# matrix = np.vstack((np.array(list_row), matrix))
# n = 5  # Задайте нужное значение n
# new_column = np.arange(1, n + 1).reshape(-1, 1)  # Создаем столбец с элементами от 1 до n
# print(new_column)
