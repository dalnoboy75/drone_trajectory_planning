import pytest
import numpy as np
import json
from matrix_reading import matrix_distance

mock_data_1 = {
    "points": [
        {"x": 0.5, "y": 0},
        {"x": 3, "y": 4.2},
        {"x": 6.3, "y": -8}
    ],
    "forbid_segments": [

    ]
}
expected_matrix_1 = np.array([
    [10 ** 8, 4.887740, 9.881295],
    [4.88774, 10 ** 8, 12.638433],
    [9.881295, 12.638433, 10 ** 8]
])

mock_single_point_data = {
    "points": [{"x": 1, "y": 1}],
    "forbid_segments": [

    ]
}
expected_matrix_2 = np.array([[10 ** 8]])

mock_two_points_data = {
    "points": [
        {"x": 1, "y": 1},
        {"x": 4, "y": 5}
    ],
    "forbid_segments": [

    ]
}

expected_matrix_3 = np.array([
    [10 ** 8, 5.0],
    [5.0, 10 ** 8]
])

mock_data_4 = {
    "points": [
        {"x": 0.5, "y": 0},
        {"x": 3, "y": 4.2},
        {"x": 6.3, "y": -8}
    ],
    "forbid_segments": [
        [0, 1]
    ]
}

expected_matrix_4 = np.array([
    [10 ** 8, 10 ** 8, 9.881295],
    [10 ** 8, 10 ** 8, 12.638433],
    [9.881295, 12.638433, 10 ** 8]
])


@pytest.mark.parametrize('mock_data, expected_matrix',
                         [(mock_data_1, expected_matrix_1), (mock_single_point_data, expected_matrix_2),
                          (mock_two_points_data, expected_matrix_3), (mock_data_4, expected_matrix_4)])
def test_matrix_reading(mock_data, expected_matrix):
    distance_matrix = matrix_distance(mock_data)
    np.testing.assert_array_almost_equal(distance_matrix, expected_matrix)
