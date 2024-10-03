import pytest
import numpy as np
import json
from matrix_reading import matrix_distance

INF = 10 ** 8
mock_data_1 = {
    "points": [
        {"x": 0.5, "y": 0},
        {"x": 3, "y": 4.2},
        {"x": 6.3, "y": -8}
    ],
    "forbid_segments": [

    ],
    "circles": [

    ],
    "name": "empty"
}
expected_matrix_1 = np.array([
    [INF, 4.887740, 9.881295],
    [4.88774, INF, 12.638433],
    [9.881295, 12.638433, INF]
])

mock_single_point_data = {
    "points": [{"x": 1, "y": 1}],
    "forbid_segments": [

    ],
    "circles": [

    ],
    "name": "single"
}
expected_matrix_2 = np.array([[INF]])

mock_two_points_data = {
    "points": [
        {"x": 1, "y": 1},
        {"x": 4, "y": 5}
    ],
    "forbid_segments": [

    ],
    "circles": [

    ],
    "name": "two"
}

expected_matrix_3 = np.array([
    [INF, 5.0],
    [5.0, INF]
])

mock_data_4 = {
    "points": [
        {"x": 0.5, "y": 0},
        {"x": 3, "y": 4.2},
        {"x": 6.3, "y": -8}
    ],
    "forbid_segments": [
        [0, 1]
    ],
    "circles": [

    ],
    "name":"three_with_forbid"
}

expected_matrix_4 = np.array([
    [INF, INF, 9.881295],
    [INF, INF, 12.638433],
    [9.881295, 12.638433, INF]
])

mock_data_5 = {
    "points": [
        {"x": 0, "y": 0},
        {"x": 0, "y": 10},
        {"x": 10, "y": 5}
    ],
    "forbid_segments": [
    ],
    "circles": [
        [0, 5, 3]
    ],
    "name":"three_circle"
}
expected_matrix_5 = np.array([[INF, 11.861007, 11.180340], [11.861007, INF, 11.180340], [11.180340, 11.180340, INF]])

mock_data_6 = {
    "points": [
        {"x": 0, "y": 0},
        {"x": 0, "y": 6},
    ],
    "forbid_segments": [
    ],
    "circles": [
        [0, 3, 3]
    ],
    "name":"two_circle"
}
expected_matrix_6 = np.array([[INF, 9.424778], [9.424778, INF]])


@pytest.mark.parametrize('mock_data, expected_matrix',
                         [(mock_data_1, expected_matrix_1), (mock_single_point_data, expected_matrix_2),
                          (mock_two_points_data, expected_matrix_3), (mock_data_4, expected_matrix_4),
                          (mock_data_5, expected_matrix_5), (mock_data_6, expected_matrix_6)])
def test_matrix_reading(mock_data, expected_matrix):
    distance_matrix = matrix_distance(mock_data)
    np.testing.assert_array_almost_equal(distance_matrix, expected_matrix)
