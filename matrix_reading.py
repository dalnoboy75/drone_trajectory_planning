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

'''
def plot_trajectory(trajectory, circles=None, name=""):
    fig, ax = plt.subplots(figsize=(10, 10))
    # Рисуем зоны пво
    for circle in circles:
        ax.add_patch(
            matplotlib.patches.Circle((circle[0], circle[1]), circle[2], fill=False, edgecolor='black', linewidth=0.5))
    for path in trajectory:
        for line in path.route:
            if isinstance(line, Line):
                # Рисуем линию
                l = matplotlib.lines.Line2D([line.first_point.x, line.second_point.x],
                                            [line.first_point.y, line.second_point.y], color="blue")
                ax.scatter(line.first_point.x, line.first_point.y, color="purple")
                ax.scatter(line.second_point.x, line.second_point.y, color="purple")
                ax.add_line(l)
            elif isinstance(line, Arc):
                # Рисуем дугу
                arc = line
                center = arc.circle.center
                radius = arc.circle.radius
                start_angle = np.degrees(np.arctan2(line.first_point.y - center.y, line.first_point.x - center.x))
                end_angle = np.degrees(np.arctan2(line.second_point.y - center.y, line.second_point.x - center.x))
                arc_patch = matplotlib.patches.Arc((center.x, center.y), 2 * radius, 2 * radius, theta1=start_angle,
                                                   theta2=end_angle, edgecolor="orange")
                ax.add_patch(arc_patch)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Trajectory Plot')
    plt.axis('equal')
    plt.savefig(os.path.join(Path.cwd() / 'plots', f'plot_{name}.png'))


def reading_matrix():
    with open('data.json') as file:
        data = json.load(file)
    matrix_distance(data)


def matrix_distance(data: dict):
    trajectory = list()
    try:
        points = np.array([(float(point['x']), float(point['y'])) for point in data['points']])
        point_amount = len(points)
        # Используем векторизацию для вычисления матрицы расстояний
        distance_matrix = np.sqrt(np.sum((points[:, np.newaxis] - points[np.newaxis, :]) ** 2, axis=-1))
        distance_matrix = np.round(distance_matrix, 6)
        np.fill_diagonal(distance_matrix, INF)

        # Запрещенные коридоры для полёта
        for segment in data['forbid_segments']:
            start = segment[0]
            finish = segment[1]
            distance_matrix[start, finish] = distance_matrix[finish, start] = INF

        # Облёт ПВО
        for circle in data["circles"]:
            for start in range(point_amount):
                for finish in range(start + 1, point_amount):
                    if distance_matrix[start, finish] != INF:
                        if intersection_number(points[start], points[finish], circle) == 2:
                            new_distance = INF
                            path = GPath()
                            line1 = Line()
                            line1.first_point = Point2D(points[start, 0], points[start, 1])
                            line2 = Line()
                            line2.second_point = Point2D(points[finish, 0], points[finish, 1])
                            arc = None
                            # Ищем точки касания касательных в окружности (в процессе)
                            start_touch_points = touch_points_search(points[start], circle)
                            finish_touch_points = touch_points_search(points[finish], circle)
                            # Ищем минимальный путь
                            for st in start_touch_points:
                                for ft in finish_touch_points:
                                    path_len = calc_dist(points[start], st) + arc_length(st, ft, circle) + calc_dist(ft,
                                                                                                                     points[
                                                                                                                         finish])
                                    if path_len < new_distance:
                                        # Запоминаем мин. путь, добавляем этот путь в общую траекторию
                                        new_distance = path_len
                                        line1.second_point = Point2D(st[0], st[1])
                                        line2.first_point = Point2D(ft[0], ft[1])
                                        arc = Arc(Point2D(st[0], st[1]), Point2D(ft[0], ft[1]),
                                                  Circle(circle[0], circle[1], circle[2]))
                            path.route = [line1, arc, line2]
                            trajectory.append(path)
                            distance_matrix[start, finish] = distance_matrix[finish, start] = round(new_distance, 6)
                        else:
                            line = Line(Point2D(points[start, 0], points[start, 1]),
                                        Point2D(points[finish, 0], points[finish, 1]))
                            path = GPath([line])
                            trajectory.append(path)
        plot_trajectory(trajectory, data['circles'], data['name'])
        return distance_matrix
    except:
        return 'error'

'''


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
