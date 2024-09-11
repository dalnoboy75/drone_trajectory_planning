import json
import numpy as np


def matrix_reading(data_path):
    with open(data_path) as file:
        data = json.load(file)
    try:
        points = np.array([(float(point['x']), float(point['y'])) for point in data['points']])
        point_amount = len(points)
        # Используем векторизацию для вычисления матрицы расстояний
        distance_matrix = np.sqrt(np.sum((points[:, np.newaxis] - points[np.newaxis, :]) ** 2, axis=-1))
        distance_matrix = np.round(distance_matrix, 6)
        np.fill_diagonal(distance_matrix, 10 ** 8)
        return distance_matrix
    except:
        return 'error'


if __name__ == '__main__':
    pass
