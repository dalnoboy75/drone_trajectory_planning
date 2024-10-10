import json
import os.path
import random

import numpy as np
from geometric_functions import *
from classes import *
import matplotlib.pyplot as plt
import matplotlib.patches
import matplotlib.lines
from pathlib import Path

INF = 10 ** 8

class Task:
    def __init__(self, data: dict):
        """Описываем формат входного словаря."""
        self.targets: list[Point2D] = self.parse_targets(data)
        self.forbidden_segments: list[tuple] = self.parse_forbidden_segments(data)
        self.circles: list[Circle] = self.parse_circles(data)
        self.length_matrix, self.path_matrix = self.matrix_distance()

    def parse_targets(self, data: dict) -> list[Point2D]:
        target = list()
        for point in data['points']:
            p = Point2D(point['x'], point['y'])
            target.append(p)
        return target

    def parse_forbidden_segments(self, data: dict):
        forbid_seg = list()
        for segment in data['forbid_segments']:
            forbid_seg.append((segment[0], segment[1]))
        return forbid_seg

    def parse_circles(self, data: dict):
        circles = list()
        for circle in data['circles']:
            c = Circle(circle[0], circle[1], circle[2])
            circles.append(c)
        return circles

    @classmethod
    def read_data(cls, filename: str | Path = 'data.json'):
        with open(filename) as file:
            data = json.load(file)
        return data

    def matrix_distance(self):
        if not self.targets:
            raise ValueError

        trajectory = list()
        points = np.array([(float(point.x), float(point.y)) for point in self.targets])
        point_amount = len(points)
        # Используем векторизацию для вычисления матрицы расстояний
        matrix_length = np.sqrt(np.sum((points[:, np.newaxis] - points[np.newaxis, :]) ** 2, axis=-1))
        matrix_length = np.round(matrix_length, 6)
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
        return matrix_length, matrix_path

    def calculate_path(self, start: int, finish: int, matrix_length, matrix_path) -> (float, GPath):
        pstart = self.targets[start]
        pfinish = self.targets[finish]
        new_distance = matrix_length[start, finish]
        path = matrix_path[start, finish]
        for circle in self.circles:
            # не пересекаемся с окружностями или пересечение по касательной
            if intersection_number(pstart, pfinish, circle) != 2:
                continue

            # 2 точки пересечения с окружностью, строим касательные и дугу
            new_distance = INF
            path = GPath()
            line1 = Line()
            line1.first_point = pstart
            line2 = Line()
            line2.second_point = pfinish
            arc = None
            # Ищем точки касания касательных в окружности
            start_touch_points = touch_points_search(pstart, circle)
            finish_touch_points = touch_points_search(pfinish, circle)
            # Ищем минимальный путь
            for st in start_touch_points:
                for ft in finish_touch_points:
                    path_len = calc_dist(pstart, st) + arc_length(st, ft, circle) + calc_dist(ft, pfinish)
                    if path_len < new_distance:
                        # Запоминаем мин. путь, добавляем этот путь в общую траекторию
                        new_distance = path_len
                        line1.second_point = st
                        line2.first_point = ft
                        arc = Arc(st, ft, circle)
            path.route = [line1, arc, line2]
        return new_distance, path

    def plot_trajectory(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        # Рисуем зоны пво
        for circle in self.circles:
            circle.plot(ax)

        for start in range(len(self.targets)):
            for finish in range(start + 1, len(self.targets)):
                path = self.path_matrix[start, finish]
                for line in path.route:
                    line.plot(ax)

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Trajectory Plot')
        plt.axis('equal')
        plt.savefig('plot.png')
