import json
import numpy as np


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
        np.fill_diagonal(distance_matrix, 10 ** 8)
        for segment in data['forbid_segments']:
            start = segment[0]
            finish = segment[1]
            distance_matrix[start, finish] = distance_matrix[finish, start] = 10**8
        return distance_matrix
    except:
        return 'error'


if __name__ == '__main__':
    reading_matrix()
