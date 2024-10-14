from __future__ import annotations
from dataclasses import dataclass


import numpy as np

@dataclass
class Edge:
    istart: int
    ifinish: int
    include: bool

class AlgLittle:
    def __init__(self,
                 new_matrix: np.ndarray,
                 discarded_nodes: list[AlgLittle] | None = None,
                 paths: list[Edge] = None,
                 hmin: float | int = 0
                 ):

        self.matrix = new_matrix
        # обрезаем первый столбец и строку - это номера точек, а не расстояния,
        self.sub_matrix = new_matrix[1:, 1:]
        self.paths: list[Edge] = paths or []   # [+(1, 5), -(3, 4), -(2, 5)]
        self.discarded_nodes: list[AlgLittle] = discarded_nodes or []  # ноды дерева, суть планы Xi
        self.hmin = hmin
        # self.reduce()   # ????

    # @property
    # def hmin(self):
    #     return self.__hmin

    # @hmin.setter
    # def hmin(self, value: int):
    #     self.__hmin += value


    def include_edge(self, zeros: list):
        edge = zeros[0]
        node_include = AlgLittle(new_matrix=self.matrix.copy(),
                                 discarded_nodes=self.discarded_nodes,
                                 paths=self.paths + [Edge(*edge, include=True)],
                                 hmin=self.hmin
                                 )
        col_index = np.where(node_include.matrix[0] == edge[1])[0]
        row_index = np.where(node_include.matrix[:, 0] == edge[0])[0]

        col_index_1 = np.where(node_include.matrix[0] == edge[0])[0]
        row_index_1 = np.where(node_include.matrix[:, 0] == edge[1])[0]
        print(col_index_1, row_index_1)
        print(node_include.matrix[row_index_1[0]][col_index_1[0]])

        keeps_value = node_include.matrix[row_index_1[0]][col_index_1[0]]
        node_include.matrix[row_index_1[0]][col_index_1[0]] = 10 ** 8
        self.matrix[row_index_1[0]][col_index_1[0]] = keeps_value
        print(node_include.matrix)
        node_include.matrix = np.delete(node_include.matrix, row_index[0], axis=0)  # Удаляем строку
        node_include.matrix = np.delete(node_include.matrix, col_index[0], axis=1)  # Удаляем столбец
        node_include.sub_matrix = node_include.matrix[1:, 1:]
        print(f'{self.include_edge.__qualname__}: {node_include.hmin=} {node_include.matrix=} {node_include.paths=}')
        return node_include
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
        print(f'{self.reduce.__qualname__}: {self.hmin=}')
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

        node_exclude = AlgLittle(new_matrix=self.matrix,
                                 discarded_nodes=self.discarded_nodes,
                                 paths=self.paths + [Edge(edge[0], edge[1], include=False)],
                                 hmin=self.hmin
                                 )
        keeps_value = node_exclude.matrix[edge[1]][edge[0]]
        node_exclude.matrix[edge[0], edge[1]] = 10 ** 8
        self.matrix = keeps_value
        node_exclude.matrix[1:, edge[1]] -= max_coeff
        node_exclude.hmin += max_coeff
        print(f'{self.delete_edge.__qualname__}: {node_exclude.hmin=} {node_exclude.matrix=} {node_exclude.paths=}')
        return node_exclude

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

    def check_end_algo(self) -> bool:
        if self.sub_matrix.shape == (2, 2):
            return True
        return False

    def end_algo(self):
        for i in range(len(self.paths)):
            if self.paths[i].include == True:
                print(self.paths[i])

def algorithm_Lit(numbers: np.ndarray) -> list[int]:
    max_coeff = 0
    # добавление строки и столбца "заголовков"
    # headed_matrix = AlgLittle.head_matrix(numbers)
    node = AlgLittle(new_matrix=numbers)
    # node.reduce()
    # zeros, max_coeff = node.SerachingMaxDegreeZero(max_coeff)
    # node_include, node_exclude = node, node
    # node_include = node_include.include_edge(zeros)
    # node_exclude = node_exclude.delete_edge(zeros, max_coeff)
    cnt = 0
    node.reduce()
    while True:
        # если размер матрицы 2х2, то закончить алгоритм
        if node.check_end_algo():
            return node.end_algo()   # [(2, 5)-, (4, 3)+ ]  ---> [1, 3, 4, ...], из набора ребер делаем последовательность вершин
        # if cnt == 1:
        #     print(node.hmin, node.paths, node.matrix)
        #     return
        zeros, max_coeff = node.SerachingMaxDegreeZero(max_coeff)
        node_include, node_exclude = node, node
        node_include = node_include.include_edge(zeros)
        if cnt == 1:
            print(node_include.hmin, node_include.paths, node_include.matrix)
            return
        node_exclude = node_exclude.delete_edge(zeros, max_coeff)
        node_include.discarded_nodes.append(node_exclude)
        node_exclude.discarded_nodes.append(node_include)
        all_possible_plans = node.discarded_nodes + [node_exclude, node_include]
        cnt += 1
        if cnt == 2:
            print(next_node.hmin, next_node.paths, next_node.matrix)
            return
        next_node = min(all_possible_plans, key=lambda node: node.hmin)
        # clean up current node
        # node.clean()   # TODO: node.matrix = None, node.submatrix = None, node.path = None....
        node = next_node


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