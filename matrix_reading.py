import json
import numpy as np
from geometric_functions import *

INF = 10 ** 8


def reading_matrix():
    with open('data.json') as file:
        data = json.load(file)
    matrix_distance(data)


def matrix_distance(data: dict):
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
                            # Ищем точки касания касательных в окружности (в процессе)
                            start_touch_points = touch_points_search(points[start], circle)
                            finish_touch_points = touch_points_search(points[finish], circle)
                            # Ищем минимальный путь
                            for st in start_touch_points:
                                for ft in finish_touch_points:
                                    new_distance = min(new_distance,
                                                       calc_dist(points[start], st) + arc_length(st, ft,circle) + calc_dist(ft,points[finish]))
                            distance_matrix[start, finish] = distance_matrix[finish, start] = round(new_distance, 6)

        return distance_matrix
    except:
        return 'error'
