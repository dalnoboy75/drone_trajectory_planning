import json
from pathlib import Path

import matplotlib.pyplot as plt

from classes import *
from geometric_functions import *

INF = 10 ** 8


class Task:
    """
        Класс для решения задачи

        Атрибуты:
        targets (list): Список целевых точек.
        forbidden_segments (list): Список запрещенных участков.
        circles (list): Список круговых препятствий (ПВО).
        length_matrix (numpy array): Матрица расстояний между точками.
        path_matrix (numpy array): Матрица путей между точками.

        Методы:
        parse_targets(data): Парсинг списка целевых точек из входных данных.
        parse_forbidden_segments(data): Парсинг списка запрещенных участков из входных данных.
        parse_circles(data): Парсинг списка круговых препятствий из входных данных.
        read_data(filename='data.json'): Чтение входных данных из JSON-файла.
        matrix_distance(): Вычисление матрицы расстояний и путей.
        calculate_path(start, finish, matrix_length, matrix_path): Вычисление оптимального пути между двумя точками.
        plot_trajectory(): Рисование траектории на графике.
        dijkstra(start_vertex=0): Реализация алгоритма Дейкстры для нахождения кратчайшего пути.
        reconstruct_path(predecessors, start, end): Реконструкция оптимального пути из предков.

        Args:
            data (dict): Словарь с входными данными.

        Returns:
            None
        """

    def __init__(self, data: dict):
        """
        Инициализация объекта Task.

        Args:
            data (dict): Словарь с входными данными.

        Returns:
            None
        """
        self.targets: list[Point2D] = self.parse_targets(data)
        self.forbidden_segments: list[tuple] = self.parse_forbidden_segments(data)
        self.circles: list[Circle] = self.parse_circles(data)
        self.length_matrix, self.path_matrix = self.matrix_distance()
        self.plot_trajectory()

    def parse_targets(self, data: dict) -> list[Point2D]:
        """
                Парсинг списка целевых точек из входных данных.

                Args:
                    data (dict): Словарь с входными данными.

                Returns:
                    list[Point2D]: Список целевых точек.
                """
        target = list()
        for point in data['points']:
            p = Point2D(point['x'], point['y'])
            target.append(p)
        return target

    def parse_forbidden_segments(self, data: dict):
        """
               Парсинг списка запрещенных участков из входных данных.

               Args:
                   data (dict): Словарь с входными данными.

               Returns:
                   list[tuple]: Список запрещенных участков.
               """
        forbid_seg = list()
        for segment in data['forbid_segments']:
            forbid_seg.append((segment[0], segment[1]))
        return forbid_seg

    def parse_circles(self, data: dict):
        """
                Парсинг списка круговых препятствий из входных данных.

                Args:
                    data (dict): Словарь с входными данными.

                Returns:
                    list[Circle]: Список круговых препятствий.
                """
        circles = list()
        for circle in data['circles']:
            c = Circle(circle[0], circle[1], circle[2])
            circles.append(c)
        return circles

    @classmethod
    def read_data(cls, filename: str | Path = 'data.json'):
        """
                Чтение входных данных из JSON-файла.

                Args:
                    filename (str | Path): Путь к файлу с входными данными (по умолчанию 'data.json').

                Returns:
                    dict: Словарь с входными данными.
                """
        with open(filename) as file:
            data = json.load(file)
        return data

    def matrix_distance(self):
        """
                Вычисление матрицы расстояний и путей между точками.

                Returns:
                    tuple: Матрица расстояний и матрица путей.
                """
        if not self.targets:
            raise ValueError

        points = np.array([(float(point.x), float(point.y)) for point in self.targets])
        point_amount = len(points)
        # Используем векторизацию для вычисления матрицы расстояний
        matrix_length = np.sqrt(np.sum((points[:, np.newaxis] - points[np.newaxis, :]) ** 2, axis=-1))
        np.fill_diagonal(matrix_length, INF)
        # делаем матрицу такого же размера для хранения путей
        matrix_path = np.array(
            [[GPath([Line(self.targets[start], self.targets[finish])]) for start in range(point_amount)] for
             finish in range(point_amount)])

        # Запрещенные коридоры для полёта
        for segment in self.forbidden_segments:
            start = segment[0]
            finish = segment[1]
            matrix_length[start, finish] = matrix_length[finish, start] = INF
            matrix_path[start, finish] = matrix_path[finish, start] = GPath()

        # Облёт ПВО

        for start in range(point_amount):
            for finish in range(start + 1, point_amount):
                if matrix_length[start, finish] != INF:
                    length, path = self.calculate_path(start, finish, matrix_length, matrix_path)
                    matrix_length[start, finish] = matrix_length[finish, start] = length
                    matrix_path[start, finish] = matrix_path[finish, start] = path
        matrix_length = np.round(matrix_length, 6)
        return matrix_length, matrix_path

    def calculate_path(self, start: int, finish: int, matrix_length, matrix_path) -> (float, GPath):
        """
                Вычисление оптимального пути между двумя точками.

                Args:
                    start (int): Начальная точка.
                    finish (int): Конечная точка.
                    matrix_length (numpy array): Матрица расстояний.
                    matrix_path (numpy array): Матрица путей.

                Returns:
                    tuple: Длина пути и объект пути.
                """
        pstart = self.targets[start]
        pfinish = self.targets[finish]
        new_distance = matrix_length[start, finish]
        path = matrix_path[start, finish]
        inter_circles = []

        # Смотрим все окружности с которыми пересекаемся
        for circle in self.circles:
            # не пересекаемся с окружностями
            if intersection_number(pstart, pfinish, circle) != 2:
                continue
            inter_circles.append(circle)
        '''
        Ищем касательные которые не пересекают окружности
        ищем общие касательные между окружностями
        
        '''
        if len(inter_circles):
            all_points = [[pstart, None, None]]
            # Ищем касательные точки
            for circle in inter_circles:
                start_touch_points = touch_points_search(pstart, circle)
                finish_touch_points = touch_points_search(pfinish, circle)
                for p in start_touch_points + finish_touch_points:
                    f = True
                    for c in self.circles:
                        if c != circle:
                            if intersection_number(pstart if p in start_touch_points else pfinish, p, c) == 2:
                                f = False
                    if f:
                        all_points.append([p, circle, pstart if p in start_touch_points else pfinish])

            # ищем точки общих касательных к окружностям

            if len(inter_circles) > 1:
                for fc in range(len(inter_circles)):
                    for sc in range(fc + 1, len(inter_circles)):
                        tangents = tangents_between_circles(inter_circles[fc], inter_circles[sc])
                        for tangent in tangents:
                            p1, p2 = tangent_points(tangent, inter_circles[fc], inter_circles[sc])
                            f = True
                            for c in self.circles:
                                if c != inter_circles[fc] and c != inter_circles[sc]:
                                    if intersection_number(p1, p2, c) == 2:
                                        f = False
                            if f:
                                all_points.append([p1, inter_circles[fc], p2])
                                all_points.append([p2, inter_circles[sc], p1])

            all_points.append([pfinish, None, None])
            points_length = np.full((len(all_points), len(all_points)), fill_value=INF, dtype=float)
            points_path = np.empty((len(all_points), len(all_points)), dtype=GPath)

            # ищем оптимальный путь
            for i in range(len(all_points)):
                for j in range(i + 1, len(all_points)):
                    if i == 0 and j == len(all_points) - 1:
                        continue
                    # если касательная из контрольной точки
                    if i == 0 and all_points[j][2] == pstart or j == len(all_points) - 1 and all_points[i][
                        2] == pfinish:
                        if i == 0:
                            kt = all_points[i][0]
                            p = all_points[j]
                        else:
                            kt = all_points[j][0]
                            p = all_points[i]
                        points_length[i, j] = points_length[j, i] = calc_dist(kt, p[0])
                        points_path[i, j] = points_path[j, i] = GPath([Line(kt, p[0])])
                    # если точки на одной окружности
                    elif all_points[i][1] == all_points[j][1] and all_points[i][1] is not None:
                        points_length[i, j] = points_length[j, i] = arc_length(all_points[i][0], all_points[j][0],
                                                                               all_points[i][1])
                        points_path[i, j] = points_path[j, i] = GPath(
                            [Arc(all_points[i][0], all_points[j][0], all_points[i][1])])
                    # если точки на общей касательной к окружностям
                    elif all_points[i][0] == all_points[j][2]:
                        if all([intersection_number(all_points[i][0], all_points[j][0], circle) != 2 for circle in
                                inter_circles if circle not in (all_points[i][1], all_points[j][1])]):
                            points_length[i, j] = points_length[j, i] = calc_dist(all_points[i][0], all_points[j][0])
                            points_path[i, j] = points_path[j, i] = GPath([Line(all_points[i][0], all_points[j][0])])
                    # остальные варианты
                    else:
                        if all([intersection_number(all_points[i][0], all_points[j][0], circle) != 2 for circle in
                                inter_circles]):
                            points_length[i, j] = points_length[j, i] = calc_dist(all_points[i][0], all_points[j][0])
                            points_path[i, j] = points_path[j, i] = GPath([Line(all_points[i][0], all_points[j][0])])

            # Представляем наши точки в виде графа и ищем оптимальный путь между начальной и конечной
            new_distance, new_path = self.dijkstra(points_length)
            path = GPath()
            for i in range(len(new_path) - 1):
                path += points_path[int(new_path[i]), int(new_path[i + 1])]

        return new_distance, path

    def plot_trajectory(self):
        """
                Рисование траектории на графике.

                Создает изображение с отображением зон ПВО и возможных маршрутов.
                """

        fig, ax = plt.subplots(figsize=(10, 10))
        # Рисуем зоны пво
        for circle in self.circles:
            circle.plot(ax)

        for start in range(len(self.targets)):
            for finish in range(start + 1, len(self.targets)):
                path = self.path_matrix[start, finish]
                for line in path.route:
                    line.plot(ax, self.targets)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Trajectory Plot')
        plt.axis('equal')
        plt.savefig('plot1.png')

    def dijkstra(self, matrix, start_vertex=0):
        """
                Реализация алгоритма Дейкстры для нахождения кратчайшего пути.

                Args:
                    matrix (numpy array): Матрица расстояний между точками.
                    start_vertex (int): Начальная вершина (по умолчанию 0).

                Returns:
                    tuple: Короткая длина пути и список предков.
                """
        num_vertices = len(matrix)
        distances = np.full(num_vertices, np.inf)
        predecessors = np.full(num_vertices, -1)
        used = np.full(num_vertices, 0)
        distances[start_vertex] = 0

        for _ in range(num_vertices):
            v = -1
            for u in range(num_vertices):
                if not used[u] and (v == -1 or distances[u] < distances[v]):
                    v = u
            used[v] = 1
            for i in range(num_vertices):
                if matrix[v, i] != INF:
                    if distances[v] + matrix[v, i] < distances[i]:
                        distances[i] = distances[v] + matrix[v, i]
                        predecessors[i] = v

        return distances[num_vertices - 1], self.reconstruct_path(predecessors, 0, num_vertices - 1)

    def reconstruct_path(self, predecessors, start, end):
        """
                Реконструкция оптимального пути из предков.

                Args:
                    predecessors (numpy array): Массив предков.
                    start (int): Начальная вершина.
                    end (int): Конечная вершина.

                Returns:
                    list: Список вершин оптимального пути.
        """
        path = []
        current = end
        while current != start:
            path.append(current)
            current = predecessors[current]
        path.append(start)
        return path[::-1]
