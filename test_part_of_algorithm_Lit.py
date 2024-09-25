import numpy as np
from algorithm_Littla import algorithm_Lit
def test_algorithm_Lit():
    # Тест 1: Простая матрица 2x2
    numbers_1 = nums = [10**8, 12, 6, 10**8]
    expected_output_1 = np.array([[, 2], [3, 4]])  # Ожидаемое значение после удаления строки и столбца
    output_1 = algorithm_Lit(numbers_1)
    assert np.array_equal(output_1, expected_output_1), f"Test 1 failed: {output_1}"

# Запуск тестов
test_algorithm_Lit()
