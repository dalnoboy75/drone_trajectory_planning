import pytest
import numpy as np
import json
from matrix_reading import matrix_reading

mock_data = {
    "points": [
        {"x": 0.5, "y": 0},
        {"x": 3, "y": 4.2},
        {"x": 6.3, "y": -8}
    ]
}

@pytest.fixture
def setup_data_file(tmp_path):
    data_file = tmp_path / "data.json"
    with open(data_file, 'w') as f:
        json.dump(mock_data, f)
    return data_file

def test_matrix_reading(setup_data_file):
    distance_matrix = matrix_reading(setup_data_file)
    expected_matrix = np.array([
        [10**8, 4.887740, 9.881295],
        [4.88774, 10**8, 12.638433],
        [9.881295, 12.638433, 10**8]
    ])

    np.testing.assert_array_almost_equal(distance_matrix, expected_matrix)

mock_empty_data = {
    "points": []
}

mock_single_point_data = {
    "points": [{"x": 1, "y": 1}]
}

mock_two_points_data = {
    "points": [
        {"x": 1, "y": 1},
        {"x": 4, "y": 5}
    ]
}

@pytest.fixture
def setup_empty_data_file(tmp_path):
    data_file = tmp_path / "empty_data.json"
    with open(data_file, 'w') as f:
        json.dump(mock_empty_data, f)
    return data_file

@pytest.fixture
def setup_single_point_file(tmp_path):
    data_file = tmp_path / "single_point_data.json"
    with open(data_file, 'w') as f:
        json.dump(mock_single_point_data, f)
    return data_file

@pytest.fixture
def setup_two_points_file(tmp_path):
    data_file = tmp_path / "two_points_data.json"
    with open(data_file, 'w') as f:
        json.dump(mock_two_points_data, f)
    return data_file

def test_matrix_reading_empty(setup_empty_data_file):
    distance_matrix = matrix_reading(setup_empty_data_file)
    assert distance_matrix == 'error'

def test_matrix_reading_single_point(setup_single_point_file):
    distance_matrix = matrix_reading(setup_single_point_file)
    expected_matrix = np.array([[10**8]])
    np.testing.assert_array_almost_equal(distance_matrix, expected_matrix)

def test_matrix_reading_two_points(setup_two_points_file):
    distance_matrix = matrix_reading(setup_two_points_file)
    expected_matrix = np.array([
        [10**8, 5.0],
        [5.0, 10**8]
    ])
    np.testing.assert_array_almost_equal(distance_matrix, expected_matrix)

