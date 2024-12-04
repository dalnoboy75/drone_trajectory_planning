import pytest
import numpy as np
from geometry.matrix_reading import Task
from constants import *

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
    "name": "empty",
    "polygons": [

    ]
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
    "name": "single",
    "polygons": [

    ]
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
    "name": "two",
    "polygons": [

    ]
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
    "name": "three_with_forbid",
    "polygons": [

    ]
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
    "name": "three_circle",
    "polygons": [

    ]
}
expected_matrix_5 = np.array([[INF, 11.861007, 11.180340], [11.861007, INF, 11.180340], [11.180340, 11.180340, INF]])

mock_data_6 = {
    "points": [
        {"x": 2, "y": 0},
        {"x": 0, "y": 10},
    ],
    "forbid_segments": [
    ],
    "circles": [
        [0, 5, 3]
    ],
    "name": "two_circle",
    "polygons": [

    ]
}
expected_matrix_6 = np.array([[INF, 11.0337384], [11.0337384, INF]])

mock_data_7 = {
    "points": [
        {"x": 1, "y": 0},
        {"x": 0, "y": 10},
    ],
    "forbid_segments": [
    ],
    "circles": [
        [0, 4, 3],
        [0, 6, 3]
    ],
    "name": "two_circles",
    "polygons": [

    ]
}

expected_matrix_7 = np.array([[INF, 11.727909], [11.727909, INF]])

mock_data_8 = {
    "points": [
        {"x": 1, "y": 0},
        {"x": 0, "y": 12},
    ],
    "forbid_segments": [
    ],
    "circles": [
        [0, 4, 2],
        [0, 9, 2],
        [2.05, 1.66, 0.7]
    ],
    "name": "three_circles",
    "polygons": [

    ]
}
expected_matrix_8 = np.array([[INF, 13.558623], [13.558623, INF]])
mock_data_9 = {
    "points": [
        {"x": 1, "y": 0},
        {"x": 0, "y": 12},
    ],
    "forbid_segments": [
    ],
    "circles": [
        [0, 4, 2],
        [0, 9, 2],
        [1.0, 1.2, 0.7],
        [-0.8, 1.02, 0.7]
    ],
    "name": "four_circles",
    "polygons": [

    ]
}

expected_matrix_9 = np.array([[INF, 12.92248], [12.92248, INF]])

mock_data_10 = {
    "points": [
        {"x": 2, "y": 0},
        {"x": 0, "y": 12},
    ],
    "forbid_segments": [
    ],
    "circles": [
    ],
    "name": "one_polygon",
    "polygons": [
        [
            {"x": -3, "y": 2},
            {"x": 0, "y": 7},
            {"x": 4, "y": 6},
            {"x": 3, "y": 2}
        ]
    ]
}
expected_matrix_10 = np.array([[INF, 13.570276], [13.570276, INF]])

mock_data_11 = {
    "points": [
        {"x": 2, "y": 0},
        {"x": 0, "y": 12},
    ],
    "forbid_segments": [
    ],
    "circles": [
        [0, 10, 1.5]
    ],
    "name": "one_polygon",
    "polygons": [
        [
            {"x": -3, "y": 2},
            {"x": 0, "y": 7},
            {"x": 4, "y": 6},
            {"x": 3, "y": 2}
        ]
    ]
}
expected_matrix_11 = np.array([[INF, 16.117994], [16.117994, INF]])

mock_data_12 = {
    "points": [
        {"x": 2, "y": 0},
        {"x": 0, "y": 12},
    ],
    "forbid_segments": [
    ],
    "circles": [
    ],
    "name": "one_polygon",
    "polygons": [
        [
            {"x": -3, "y": 2},
            {"x": 0, "y": 7},
            {"x": 4, "y": 6},
            {"x": 3, "y": 2}
        ],
        [
            {"x": -3, "y": 10},
            {"x": 0, "y": 11},
            {"x": 2, "y": 9}
        ]
    ]
}
expected_matrix_12 = np.array([[INF, 16.990716], [16.990716, INF]])


@pytest.mark.parametrize('mock_data, expected_matrix',
                         [(mock_data_1, expected_matrix_1), (mock_single_point_data, expected_matrix_2),
                          (mock_two_points_data, expected_matrix_3), (mock_data_4, expected_matrix_4),
                          (mock_data_5, expected_matrix_5), (mock_data_6, expected_matrix_6),
                          (mock_data_7, expected_matrix_7), (mock_data_8, expected_matrix_8),
                          (mock_data_9, expected_matrix_9), (mock_data_10, expected_matrix_10),
                          (mock_data_11, expected_matrix_11), (mock_data_12, expected_matrix_12)])
def test_matrix_reading(mock_data, expected_matrix):
    t = Task(mock_data)
    distance_matrix = t.length_matrix
    np.testing.assert_array_almost_equal(distance_matrix, expected_matrix)
