import numpy as np
from Alg_L_Classes import algorithm_Lit

INF = 10**8
def test_right_paths():
    numbers = np.array(
        [
            [INF, 20, 18, 12, 8],
            [5, INF, 14, 7, 11],
            [12, 18, INF, 6, 11],
            [11, 17, 11, INF, 12],
            [5, 5, 5, 5, INF],
        ]
    )
    start_airfield = 4
    kolvo_airdields = 4
    result = algorithm_Lit(numbers, start_airfield, kolvo_airdields)
    answer = ([[5, 2, 1, 6], [7, 3, 4, 8]], [(5, 2), (2, 1), (1, 6), (6, 7), (7, 3), (3, 4), (4, 8), (8, 5)])
    assert result == answer