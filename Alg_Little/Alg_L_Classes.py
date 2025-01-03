from __future__ import annotations

import typing
from dataclasses import dataclass

import numpy as np
import timeit

INF = 10**8

def has_cycle(edges: list[tuple]):
    from collections import defaultdict

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    visited = set()
    rec_stack = set()
    cycle_nodes = set()  

    def dfs(node):
        if node in rec_stack:
            cycle_nodes.add(node)  
            return True
        if node in visited:
            return False
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph[node]:
            if neighbor not in graph:
                return False
            if dfs(neighbor):
                cycle_nodes.add(node)  
                return True

        rec_stack.remove(node)
        return False

    for vertex in graph:
        if dfs(vertex):
            return True, len(cycle_nodes)  
    return False, 0  

@dataclass
class Edge:
    """
        Класс для представления ребра графа.

        Attributes:
            istart (int): Начальная вершина ребра.
            ifinish (int): Конечная вершина ребра.
            include (bool): Флаг, указывающий, включено ли ребро в путь.
    """
    istart: int
    ifinish: int
    include: bool


class AlgLittle:
    """
        Класс для реализации алгоритма Литтла.

        Attributes:
            MAXID (int): Максимальный идентификатор узла.
            planID (int): Уникальный идентификатор текущего узла.
            matrix (np.ndarray): Матрица расстояний.
            sub_matrix (np.ndarray): Подматрица расстояний без заголовков.
            paths (list[Edge]): Список путей (ребер) в текущем узле.
            discarded_nodes (list[AlgLittle]): Список исключенных узлов.
            hmin (float | int): Текущая нижняя граница стоимости.
            h_level (int): Уровень узла в дереве решений.
    """
    MAXID = -1  

    def __init__(
        self,
        new_matrix: np.ndarray,
        discarded_nodes: list[AlgLittle] | None = None,
        paths: list[Edge] = None,
        hmin: float | int = 0,
        h_level: int = 0,
    ):
        """
            Инициализация узла алгоритма Литтла.

            Args:
                new_matrix (np.ndarray): Матрица расстояний.
                discarded_nodes (list[AlgLittle] | None): Список исключенных узлов.
                paths (list[Edge]): Список путей (ребер).
                hmin (float | int): Начальная нижняя граница стоимости.
                h_level (int): Уровень узла в дереве решений.
        """
        self.planID = AlgLittle.next_id()
        self.matrix = new_matrix
        self.sub_matrix = new_matrix[1:, 1:]
        self.paths: list[Edge] = paths or [] 
        self.discarded_nodes: list[AlgLittle] = (
            discarded_nodes or []
        )
        self.hmin = hmin
        self.h_level = h_level or 0

    def __str__(self):
        """
            Возвращает строковое представление узла.

            Returns:
                str: Строковое представление узла.
        """
        return f"x{self.planID}({self.hmin})"

    def __repr__(self):
        """
            Возвращает подробное строковое представление узла.

            Returns:
                str: Подробное строковое представление узла.
        """
        delim = "-" * 20
        discarded = " ".join([str(n) for n in self.discarded_nodes])
        return f"{delim}\nX{self.planID}\n{self.pretty_matrix()}\nhmin={self.hmin}\ndiscraded={discarded}"

    def pretty_matrix(self):
        """
            Возвращает строковое представление матрицы.

            Returns:
                str: Строковое представление матрицы.
        """
        return str(self.matrix)

    def include_edge(self, zeros: list):
        """
            Включает ребро в путь, обновляет матрицу и создает новый узел с учетом включенного ребра.

            Args:
                zeros (list): Список координат нулевых элементов матрицы, из которых выбирается ребро для включения.

            Returns:
                AlgLittle: Новый узел с обновленной матрицей и включенным ребром.
        """
        edge = zeros[0]
        new_matrix = self.matrix.copy()

        col_index = np.where(new_matrix[0] == edge[1])[0]
        row_index = np.where(new_matrix[:, 0] == edge[0])[0]

        col_index_1 = np.where(new_matrix[0] == edge[0])[0]
        row_index_1 = np.where(new_matrix[:, 0] == edge[1])[0]

        paths_1 = self.paths.copy()
        paths_1 += [Edge(edge[0], edge[1], include=True)]
        edges = [(int(edge.istart), int(edge.ifinish)) for edge in paths_1 if edge.include]
        if len(row_index_1) != 0 and len(col_index_1) != 0:
            keeps_value = new_matrix[row_index_1[0]][col_index_1[0]]
            new_matrix[row_index_1[0]][col_index_1[0]] = INF
            self.matrix[row_index_1[0]][col_index_1[0]] = keeps_value
        new_matrix = np.delete(new_matrix, row_index[0], axis=0)
        new_matrix = np.delete(new_matrix, col_index[0], axis=1)  

        has_cycle_result, cycle_count = has_cycle(edges)
        if len(edges) >= 3 and has_cycle_result:
            node_include = AlgLittle(
                new_matrix=new_matrix,
                discarded_nodes=self.discarded_nodes.copy(),
                paths=self.paths + [Edge(edge[0], edge[1], include=True)],
                hmin=self.hmin,
                h_level=self.h_level + 1,
            )
        else:    
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
        """
            Высчитывает НГЦФ и выполняет редукцию матрицы, уменьшая ее значения на минимумы строк и столбцов, и обновляет значение hmin.

            Returns:
                int: Значение hmin после редукции.
        """
        row_min = self.sub_matrix.min(axis=1)
        self.sub_matrix -= row_min[:, np.newaxis]
        columns_min = self.sub_matrix.min(axis=0)
        self.sub_matrix -= columns_min

        self.hmin += sum(row_min) + sum(columns_min)

        self.matrix[1:, 1:] = self.sub_matrix
        # print(f'{self.reduce.__qualname__}: {self.hmin=}')
        return self.hmin

    def SearchingMaxDegreeZero(self, max_coeff: int) -> (list, int):
        """
            Находит нулевые элементы матрицы и определяет их коэффициенты. Возвращает список координат нулей с максимальным коэффициентом.

            Args:
                max_coeff (int): Текущее максимальное значение коэффициента.

            Returns:
                tuple: Список координат нулей с максимальным коэффициентом и обновленное значение max_coeff.
        """
        zeros = []
        coeff_list = []
        for i in range(1, self.matrix.shape[0]):
            for j in range(1, self.matrix.shape[1]):
                if self.matrix[i, j] == 0:
                    zeros.append((self.matrix[i][0], self.matrix[0][j]))
                    coeff = self.get_coefficient(i, j)
                    coeff_list.append(coeff)
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
        """
            Вычисляет коэффициент для нулевого элемента матрицы, находящегося в строке r и столбце c.

            Args:
                r (int): Индекс строки нулевого элемента.
                c (int): Индекс столбца нулевого элемента.

            Returns:
                int: Коэффициент нулевого элемента.
        """
        rmin = cmin = float("inf")

        for i in range(1, self.matrix.shape[0]):
            if i != r:
                rmin = min(rmin, self.matrix[i, c])
            if i != c:
                cmin = min(cmin, self.matrix[r, i])
        return rmin + cmin

    def delete_edge(self, zeros: list, max_coeff: int) -> (typing.Self):
        """
            Удаляет ребро из пути, обновляет матрицу, устанавливая бесконечность для соответствующего элемента, и создает новый узел.

            Args:
                zeros (list): Список координат нулевых элементов матрицы, из которых выбирается ребро для удаления.
                max_coeff (int): Максимальный коэффициент нулевого элемента.

            Returns:
                AlgLittle: Новый узел с обновленной матрицей и удаленным ребром.
        """
        
        edge = zeros[0]

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
        """
            Добавляет заголовки строк и столбцов к матрице.

            Args:
                matrix (np.ndarray): Исходная матрица.

            Returns:
                np.ndarray: Матрица с заголовками.
        """
        rows, columns = np.shape(matrix)
        list_column = np.arange(1, columns + 1).reshape(
            -1, 1
        )
        list_row = np.arange(0, columns + 1).reshape(
            1, -1
        )
        new_matrix = matrix
        new_matrix = np.hstack((np.array(list_column), new_matrix))
        new_matrix = np.vstack((np.array(list_row), new_matrix))
        return new_matrix

    def trajectory(self) -> list[int]:
        """
            Возвращает последовательность точек, связанных траекторией.

            Returns:
                list[int]: Список точек траектории.
        """
        return [1, 2, 3]

    def check_end_algo(self) -> bool:
        """
            Проверяет, завершен ли алгоритм (если матрица 2*2, то алггоритм закончен).

            Returns:
                bool: True, если алгоритм завершен, иначе False.
        """
        # print(f"MATRIX_SHAPE = {self.sub_matrix.shape}")
        if self.sub_matrix.shape == (2, 2):
            return True
        return False

    def end_algo(self) -> list[list]:
        """
            Преобразует пути в список ребер.

            Returns:
                list[list]: Список ребер.
        """
        l = []
        for i in self.paths:
            listok = []
            listok.append(i.istart)
            listok.append(i.ifinish)
            listok.append(i.include)
            l.append(listok)
        return l

    def find_rest_path(self) -> list[list]:
        """
            Выбирает два ребра из матрицы 2x2, которые нужно включить в путь.

            Returns:
                list[list]: Список выбранных ребер.
        """
        # print(f"self.matrix: {self.matrix}")
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
        return l

    @classmethod
    def next_id(cls):
        """
            Генерирует следующий уникальный идентификатор узла.

            Returns:
                int: Уникальный идентификатор.
        """
        cls.MAXID += 1
        return cls.MAXID


def get_list_edges(data: list, num_rows: int, start_airfield: int) -> list[tuple]:
    """
        Возвращает список ребер, начиная с заданного аэродрома.

        Args:
            data (list): Список данных о путях.
            num_rows (int): Количество строк в матрице.
            start_airfield (int): Начальный аэродром.

        Returns:
            list[tuple]: Список ребер.
    """
    print(f"st: {start_airfield}")
    for i in data:
        if i[0] == 7:
            print(i)
    
    result = []
    for item in data:
        if item[2]:
            result.append((int (item[0]), int (item[1])))
            last_pair = result[-1]
            break
    cnt = 1
    data_1 = [(int(x), int(y), z) for (x, y, z) in data]
    while cnt < num_rows:
        for item in data_1:
            if item[2] and last_pair[1] == item[0]:
                result.append((int (item[0]), int (item[1])))
                last_pair = result[-1]
                cnt += 1
                data_1.remove(item) 
                break

    return result


def vertex(edges: list[tuple], list_airfields: list) -> list[list]:
    """
        Возвращает массив вершин, через которые проходит гамильтонов путь.

        Args:
            edges (list[tuple]): Список ребер.
            list_airfields (list): Список аэродромов.

        Returns:
            list[list]: Массив вершин.
    """
    vertices = [edge[0] for edge in edges]
    result = []
    cur_res = []
    for i in vertices:
        cur_res.append(i)
        if i in list_airfields:
            result.append(cur_res)
            cur_res = []
    if len(cur_res) != 0:
        result.append(cur_res)
    return result


def add_airfields(numbers: np.ndarray, s: int, kolvo_airfields: int) -> np.matrix:
    """
        Добавляет аэродромы в матрицу.

        Args:
            numbers (np.ndarray): Исходная матрица.
            s (int): Индекс начального аэродрома.
            kolvo_airfields (int): Количество аэродромов.

        Returns:
            np.matrix: Матрица с добавленными аэродромами.
    """
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
    """
        Реализация алгоритма Литтла.

        Args:
            numbers (np.ndarray): Матрица расстояний.
            s (int): Индекс начального аэродрома.
            kolvo_airfields (int): Количество аэродромов.

        Returns:
            tuple[list[list], list[tuple]]: Результаты алгоритма.
    """

    kolvo_airfields *= 2
    pos = numbers.shape[0]
    if kolvo_airfields != 1:
        numbers = add_airfields(numbers, s, kolvo_airfields)
    numbers = AlgLittle.head_matrix(numbers)
    node = AlgLittle(new_matrix=numbers)
    num_rows = node.matrix.shape[0] - 1
    node.reduce()
    start_airfield = pos
    list_airfields = []
    if kolvo_airfields != 1:
        for i in range(int(kolvo_airfields / 2)):
            list_airfields.append(pos + 1)
            pos += 2
    size_matrix = numbers.shape[0]
    # print(f"list: {list_airfields}")
    while True:
        # print(repr(node))
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
        # print("=" * 20)
        # print(f"prev_node: {prev_node.hmin}")
        # print(f"node: {node.hmin}")
        if prev_node.h_level == node.h_level:
            node.discarded_nodes.remove(prev_node)
        node1 = node
        if node1.check_end_algo():
            l = node1.find_rest_path()    
            r = l.copy()   
            for i in node1.paths:
                listok = []
                listok.append(i.istart)
                listok.append(i.ifinish)
                listok.append(i.include)
                l.append(listok)
            
            edges = [(int(edge[0]), int(edge[1])) for edge in l if edge[2]]
            has_cycle_result, cycle_count = has_cycle(edges)

            if has_cycle_result and cycle_count + 1 != size_matrix:

                edges_1 = [(int(edge[0]), int(edge[1])) for edge in r if edge[2]]
                if(edges_1[0] == (node1.matrix[1][0], node1.matrix[0][1])):
                    indices = [
                                (node1.matrix[1][0], node1.matrix[0][2], True),
                                (node1.matrix[2][0], node1.matrix[0][1], True),
                            ]
                else:
                    indices = [
                                (node1.matrix[1][0], node1.matrix[0][1], True),
                                (node1.matrix[2][0], node1.matrix[0][2], True),
                            ]
                l_1 = indices
                for i in node1.paths:
                    listok = []
                    listok.append(i.istart)
                    listok.append(i.ifinish)
                    listok.append(i.include)
                    l_1.append(listok)
                answer = get_list_edges(l_1, num_rows, start_airfield)
                # print(f"answer: {answer}")
                ans = vertex(answer, list_airfields)
                for i in range(len(answer)):
                    x, y = answer[i]
                    if x > start_airfield:
                        x = start_airfield
                    if y > start_airfield:
                        y = start_airfield
                    answer[i] = (x, y)
                for x in range(len(ans)):
                    for j in range(len(ans[x])):
                        if ans[x][j] > start_airfield:
                            ans[x][j] = start_airfield
                # print(f"ans: {ans}")
                return ans, answer
            
            answer = get_list_edges(l, num_rows, start_airfield)
            # print(f"answer: {answer}")
            # result = [(int(x), int(y)) for (x, y) in answer]
            ans = vertex(answer, list_airfields)
            for i in range(len(answer)):
                    x, y = answer[i]
                    if x > start_airfield:
                        x = start_airfield
                    if y > start_airfield:
                        y = start_airfield
                    answer[i] = (x, y)
            for x in range(len(ans)):
                for j in range(len(ans[x])):
                    if ans[x][j] > start_airfield:
                            ans[x][j] = start_airfield
            # print(f"ans: {ans}")
            return ans, answer