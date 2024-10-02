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


def plot_trajectory(trajectory, circles=None):
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
    plt.savefig(os.path.join(Path.cwd() / 'plots', f'plot-{random.randint(100, 10000)}.png'))


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
        plot_trajectory(trajectory, data['circles'])
        return distance_matrix
    except:
        return 'error'
