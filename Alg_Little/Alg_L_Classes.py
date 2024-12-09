from __future__ import annotations

import typing
from dataclasses import dataclass

import numpy as np

INF = 10**8


@dataclass
class Edge:
    istart: int
    ifinish: int
    include: bool


class AlgLittle:
    MAXID = -1  # чтобы первый id был 0 и как в примере.

    def __init__(
        self,
        new_matrix: np.ndarray,
        discarded_nodes: list[AlgLittle] | None = None,
        paths: list[Edge] = None,
        hmin: float | int = 0,
        h_level: int = 0,
    ):
        self.planID = AlgLittle.next_id()
        self.matrix = new_matrix
        # обрезаем первый столбец и строку - это номера точек, а не расстояния,
        self.sub_matrix = new_matrix[1:, 1:]
        self.paths: list[Edge] = paths or []  # [+(1, 5), -(3, 4), -(2, 5)]
        self.discarded_nodes: list[AlgLittle] = (
            discarded_nodes or []
        )  # ноды дерева, суть планы Xi
        self.hmin = hmin
        self.h_level = h_level or 0
        # self.reduce()   # ????

    def __str__(self):
        return f"x{self.planID}({self.hmin})"

    def __repr__(self):
        delim = "-" * 20
        discarded = " ".join([str(n) for n in self.discarded_nodes])
        return f"{delim}\nX{self.planID}\n{self.pretty_matrix()}\nhmin={self.hmin}\ndiscraded={discarded}"

    def pretty_matrix(self):
        return str(self.matrix)

    # @property
    # def hmin(self):
    #     return self.__hmin

    # @hmin.setter
    # def hmin(self, value: int):
    #     self.__hmin += value

    def include_edge(self, zeros: list):
        edge = zeros[0]
        new_matrix = self.matrix.copy()

        col_index = np.where(new_matrix[0] == edge[1])[0]
        row_index = np.where(new_matrix[:, 0] == edge[0])[0]

        col_index_1 = np.where(new_matrix[0] == edge[0])[0]
        row_index_1 = np.where(new_matrix[:, 0] == edge[1])[0]

        # print(node_include.matrix, col_index_1[0], edge[1])
        if len(row_index_1) != 0 and len(col_index_1) != 0:
            keeps_value = new_matrix[row_index_1[0]][col_index_1[0]]
            new_matrix[row_index_1[0]][col_index_1[0]] = INF
            self.matrix[row_index_1[0]][col_index_1[0]] = keeps_value
        # print(node_include.matrix)
        new_matrix = np.delete(new_matrix, row_index[0], axis=0)  # Удаляем строку
        new_matrix = np.delete(new_matrix, col_index[0], axis=1)  # Удаляем столбец

        node_include = AlgLittle(
            new_matrix=new_matrix,
            discarded_nodes=self.discarded_nodes.copy(),
            paths=self.paths + [Edge(edge[0], edge[1], include=True)],
            hmin=self.hmin,
            h_level=self.h_level + 1,
        )
        node_include.reduce()
        # print(f'{self.include_edge.__qualname__}: {node_include.hmin=} {node_include.matrix=} {node_include.paths=}')
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
        # print(f'{self.reduce.__qualname__}: {self.hmin=}')
        return self.hmin

    def SearchingMaxDegreeZero(self, max_coeff: int) -> (list, int):
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

        # print("zeros = ", zeros)
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
        rmin = cmin = float("inf")

        # Обход строки и столбца
        for i in range(1, self.matrix.shape[0]):
            if i != r:
                rmin = min(rmin, self.matrix[i, c])
            if i != c:
                cmin = min(cmin, self.matrix[r, i])
        return rmin + cmin

    def delete_edge(self, zeros: list, max_coeff: int) -> (typing.Self, int):
        "На вход получаем индексы элемента, который имеет наибольший наибольшую степень нуля, удаляем строку и столбец с этими индексами, возвращаем измененную матрицу"

        edge = zeros[0]

        # делаем КОПИЮ матрицы с поставленной куда надо бесконечностью
        new_matrix = self.matrix.copy()
        col_index_1 = np.where(new_matrix[0] == edge[1])[0]
        row_index_1 = np.where(new_matrix[:, 0] == edge[0])[0]
        new_matrix[row_index_1[0], col_index_1[0]] = INF

        node_exclude = AlgLittle(
            new_matrix=new_matrix,
            discarded_nodes=self.discarded_nodes.copy(),
            paths=self.paths + [Edge(edge[0], edge[1], include=False)],
            hmin=self.hmin,
            h_level=self.h_level + 1,
        )
        node_exclude.reduce()
        return node_exclude

    @staticmethod
    def head_matrix(matrix: np.ndarray) -> np.ndarray:
        """Возвращает матрицу, приписывая первую строку и столбец с НОМЕРАМИ точек от 1 до n."""
        rows, columns = np.shape(matrix)
        list_column = np.arange(1, columns + 1).reshape(
            -1, 1
        )  # столбец из элементов от 1 до n
        list_row = np.arange(0, columns + 1).reshape(
            1, -1
        )  # строка из элементов от 0 до n
        new_matrix = matrix
        new_matrix = np.hstack((np.array(list_column), new_matrix))
        new_matrix = np.vstack((np.array(list_row), new_matrix))
        return new_matrix

    def trajectory(self) -> list[int]:
        """Возвращает последовательность точек от 1 до конца, связанную траекторию."""
        return [1, 2, 3]

    def check_end_algo(self) -> bool:
        """Проверка на то, надо ли заканчивать алгоритм или нет, если матрица 2*2, то алггоритм закоончен"""
        print(f"MATRIX_SHAPE = {self.sub_matrix.shape}")
        if self.sub_matrix.shape == (2, 2):
            return True
        return False

    def end_algo(self) -> list[list]:
        """Преобразовывает пути в лист ребер, где первый параметр это начальная вершина, второй параметр это конечная вершина, третий параметр показывает включено это ребро в путь или нет"""
        l = []
        for i in self.paths:
            listok = []
            listok.append(i.istart)
            listok.append(i.ifinish)
            listok.append(i.include)
            l.append(listok)
        return l

    def find_rest_path(self) -> list[list]:
        """Выбирает два ребра из матрицы 2 на 2, которые надо включить в путь"""
        print(f"self.matrix: {self.matrix}")
        l = []
        if (
            self.matrix[1][1] + self.matrix[2][2]
            <= self.matrix[1][2] + self.matrix[2][1]
        ):
            indices = [
                (self.matrix[1][0], self.matrix[0][1]),
                (self.matrix[2][0], self.matrix[0][2]),
            ]
        else:
            indices = [
                (self.matrix[1][0], self.matrix[0][2]),
                (self.matrix[2][0], self.matrix[0][1]),
            ]

        l = [[value[0], value[1], True] for value in indices]
        print(l)
        return l

    @classmethod
    def next_id(cls):
        cls.MAXID += 1
        return cls.MAXID


def get_list_edges(data: list, num_rows: int, start_airfield: int) -> list[tuple]:
    """Возвращает лист ребер, где у первого ребра начальная вершина, в которой находится аэродром"""
    result = []
    # Найти первую пару
    for item in data:
        if item[2] and item[0] == start_airfield:
            result.append((int (item[0]), int (item[1])))
            last_pair = result[-1]
            break
    cnt = 1
    while cnt < num_rows:
        for item in data:
            if item[2] and last_pair[1] == item[0]:
                result.append((int (item[0]), int (item[1])))
                last_pair = result[-1]
                cnt += 1
                data.remove(item)  # Удаляем элемент из data
                break

    return result


def vertex(edges: list[tuple], list_airfields: list) -> list[list]:
    """Возвращает массив вершин, через которые проходит гамильтонов путь"""
    print(edges, list_airfields)
    vertices = [edge[0] for edge in edges]
    result = []
    cur_res = []
    for i in vertices:
        cur_res.append(i)
        if i in list_airfields:
            result.append(cur_res)
            cur_res = []
    return result


def add_airfields(numbers: np.ndarray, s: int, kolvo_airfields: int) -> np.matrix:
    """Добавление в матрицу аэродромов, возвращает матрицу с добавленными аэродромами"""
    rows = numbers.shape[0]
    size = rows + kolvo_airfields
    new_matrix = np.zeros((size, size), dtype=int)
    new_matrix[:rows, :rows] = numbers
    numbers = new_matrix
    for i in range(rows):
        numbers[i, rows:size] = numbers[i][s]
    for j in range(rows):
        numbers[rows:size, j] = numbers[s][j]
    pos_x = rows + 1
    pos_y = rows + 2
    for i in range(rows, size):
        for j in range(rows, size):
            if i == size - 1 and j == rows:
                continue
            if i == pos_x and j == pos_y:
                pos_x += 2
                pos_y += 2
            else:
                numbers[i][j] = INF
    numbers = np.delete(np.delete(numbers, s, axis=0), s, axis=1)
    return numbers


def algorithm_Lit(
        numbers: np.ndarray, s: int, kolvo_airfields: int
) -> tuple[list[list], list[tuple]]:
    """Алгоритм Литтла"""
    # добавление строки и столбца "заголовков"
    pos = numbers.shape[0]
    numbers = add_airfields(numbers, s, kolvo_airfields)
    numbers = AlgLittle.head_matrix(numbers)
    node = AlgLittle(new_matrix=numbers)
    num_rows = node.matrix.shape[0] - 1
    node.reduce()
    start_airfield = pos
    list_airfields = []
    for i in range(int(kolvo_airfields / 2)):
        list_airfields.append(pos + 1)
        pos += 2

    print(f"list: {list_airfields}")
    while True:
        print(repr(node))
        max_coeff = 0
        zeros, max_coeff = node.SearchingMaxDegreeZero(max_coeff)
        # node_include, node_exclude = node, node
        # print('Before delete ' + repr(node))
        node_exclude = node.delete_edge(zeros, max_coeff)
        # print('After delete ' + repr(node))
        node_include = node.include_edge(zeros)

        node_include.discarded_nodes.append(node_exclude)
        node_exclude.discarded_nodes.append(node_include)
        all_possible_plans = node.discarded_nodes + [node_exclude, node_include]
        prev_node = node
        node = min(all_possible_plans, key=lambda nd: nd.hmin)
        print("=" * 20)
        print(f"prev_node: {prev_node.hmin}")
        print(f"node: {node.hmin}")
        if prev_node.h_level == node.h_level:
            node.discarded_nodes.remove(prev_node)
        # если размер матрицы 2х2, то закончить алгоритм
        node1 = node
        if node1.check_end_algo():
            l = node1.find_rest_path()
            for i in node1.paths:
                listok = []
                listok.append(i.istart)
                listok.append(i.ifinish)
                listok.append(i.include)
                l.append(listok)
            answer = get_list_edges(l, num_rows, start_airfield)
            ans = vertex(answer, list_airfields)
            print(f"ans: {ans}")
            return ans, answer


