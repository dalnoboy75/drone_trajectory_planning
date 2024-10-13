from __future__ import annotations

import numpy as np

class Edge:
    def __init__(self, istart: int, ifinish: int, include: bool):
        self.istart = istart
        self.ifinish = ifinish
        self.include = include

class AlgLittle:
    def __init__(self, new_matrix: np.ndarray, discarded_nodes: list[AlgLittle] | list[AlgLittle] = [], paths: list[tuple] = None, hmin: float | int = 0):
        self.matrix = new_matrix
        # обрезаем первый столбец и строку - это номера точек, а не расстояния,
        self.sub_matrix = new_matrix[1:, 1:]
        self.paths: list[Edge] = paths or []   # [+(1, 5), -(3, 4), -(2, 5)]
        self.discarded_nodes: list[AlgLittle] = discarded_nodes or []  # ноды дерева, суть планы Xi
        self.hmin = hmin

    def include_edge(self, zeros: list):
        edge = zeros[0]

        self.matrix = np.delete(self.matrix, edge[0], axis=0)  # Удаляем строку
        self.matrix = np.delete(self.matrix, edge[1], axis=1)  # Удаляем столбец
        self.sub_matrix = self.matrix[1:, 1:]
        print('in_h_min = ', self.hmin)
        return self.matrix, self.reduce()

    def reduce(self: np.ndarray) -> int:
        """высчитывает НГЦФ, редуцирует матрицу"""
        # Находим минимумы по строкам и столбцам подматрицы
        row_min = self.sub_matrix.min(axis=1)
        self.sub_matrix -= row_min[:, np.newaxis]
        columns_min = self.sub_matrix.min(axis=0)
        self.sub_matrix -= columns_min

        # Суммируем минимумы
        self.hmin += sum(row_min) + sum(columns_min)

        self.matrix[1:, 1:] = self.sub_matrix
        print('1231231', self.hmin)
        return self.hmin



    def SerachingMaxDegreeZero(self, max_coeff: int) -> (list, int):
        "Передаем матрицу, считаем максимальную степень нуля и возвращаем индексы, под которыми находится этот ноль в матрице"
        # Список координат нулевых элементов
        zeros = []
        # Список их коэффициентов
        coeff_list = []
        # Поиск нулевых элементов
        for i in range(1, self.matrix.shape[0]):
            for j in range(1, self.matrix.shape[1]):
                # Если равен нулю
                if self.matrix[i, j] == 0:
                    # Добавление в список координат
                    zeros.append((self.matrix[i][0], self.matrix[0][j]))
                    # Расчет коэффициента и добавление в список
                    coeff = self.get_coefficient(i, j)
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

    def get_coefficient(self: np.ndarray, r: int, c: int) -> int:
        "На вход получаем матрицу и номер столбца и строки матрицы, в которой под индексами [r][c] содержится в матрице 0, на выходе получаем его коэффицент"
        rmin = cmin = float('inf')

        # Обход строки и столбца
        for i in range(1, self.matrix.shape[0]):
            if i != r:
                rmin = min(rmin, self.matrix[i, c])
            if i != c:
                cmin = min(cmin, self.matrix[r, i])
        return rmin + cmin

    def delete_edge(self, zeros: list, max_coeff: int) -> (np.ndarray, int):
        "На вход получаем индексы элемента, который имеет наибольший наибольшую степень нуля, удаляем строку и столбец с этими индексами, возвращаем измененную матрицу"

        edge = zeros[0]
        self.matrix[1:, edge[1]] -= max_coeff
        self.matrix[edge[0]][edge[1]] = 10 ** 8
        print('d_h_min = ', self.hmin)
        self.hmin += max_coeff
        return self.matrix, self.hmin


    @staticmethod
    def head_matrix(matrix: np.ndarray) -> np.ndarray:
        """Возвращает матрицу, приписывая первую строку и столбец с НОМЕРАМИ точек от 1 до n."""
        rows, columns = np.shape(matrix)
        list_column = np.arange(1, columns + 1).reshape(-1, 1)  # столбец из элементов от 1 до n
        list_row = np.arange(0, columns + 1).reshape(1, -1)  # строка из элементов от 0 до n
        new_matrix = matrix
        new_matrix = np.hstack((np.array(list_column), new_matrix))
        new_matrix = np.vstack((np.array(list_row), new_matrix))
        return new_matrix

    def trajectory(self) -> list[int]:
        """Возвращает последовательность точек от 1 до конца, связанную траекторию."""
        return [1, 2, 3]


def algorithm_Lit(numbers: np.ndarray) -> list[int]:
    max_coeff = 0
    headed_matrix = AlgLittle.head_matrix(numbers)
    node = AlgLittle(new_matrix=numbers)
    node.reduce()
    zeros, max_coeff = node.SerachingMaxDegreeZero(max_coeff)
    return
    node_1, node_2 = node, node
    Matrix_1, node_exclude = node_1.delete_edge(zeros, max_coeff)
    Matrix_2, node_include = node_2.include_edge(zeros)
    print("Matrix and node_include:")
    print(Matrix_1, node_exclude)
    print(Matrix_2, node_include)

matrix = np.array(
        [[0, 1, 2, 3, 4, 5], [1, 10 ** 8, 20, 18, 12, 8], [2, 5, 10 ** 8, 14, 7, 11], [3, 12, 18, 10 ** 8, 6, 11],
         [4, 11, 17, 11, 10 ** 8, 12],
         [5, 5, 5, 5, 5, 10 ** 8]])
algorithm_Lit(matrix)
    # while True:
    #     if node.the_end():
    #         return node.trajectory()
    #     node.reduce()
    #     zeros, max_coeff = node.zero_degrees()
    #     node_include = node.include_edge(zeros, max_coeff)
    #     node_exclude = node.delete_edge(zeros, max_coeff)
    #     # по node_include, node_exclude и списку отброшенных планов self.discarded_nodes
    #     # ищем ноду с наименьшим весом и переходим к ней
    #     next_node = AlgLittle.minh_node(node_include, node_exclude, node.discarded_nodes)
    #     node = next_node
