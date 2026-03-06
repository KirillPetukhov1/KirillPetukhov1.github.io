import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pytest

from main import (create_vector, create_matrix, reshape_vector, vector_add,
                  scalar_multiply, elementwise_multiply, dot_product,
                  matrix_multiply, matrix_determinant, load_dataset,
                  matrix_inverse, statistical_analysis, normalize_data,
                  plot_histogram, plot_heatmap, plot_line, solve_linear_system)


def test_create_vector():
    v = create_vector()
    assert isinstance(v, np.ndarray)
    assert v.shape == (10,)
    assert np.array_equal(v, np.arange(10))


def test_create_matrix():
    m = create_matrix()
    assert isinstance(m, np.ndarray)
    assert m.shape == (5, 5)
    assert np.all((m >= 0) & (m < 1))


def test_reshape_vector():
    v = np.arange(10)
    reshaped = reshape_vector(v)
    assert reshaped.shape == (2, 5)
    assert reshaped[0, 0] == 0
    assert reshaped[1, 4] == 9


def test_vector_add():
    assert np.array_equal(
        vector_add(np.array([1, 2, 3]), np.array([4, 5, 6])),
        np.array([5, 7, 9])
    )
    assert np.array_equal(
        vector_add(np.array([0, 1]), np.array([1, 1])),
        np.array([1, 2])
    )


def test_scalar_multiply():
    assert np.array_equal(
        scalar_multiply(np.array([1, 2, 3]), 2),
        np.array([2, 4, 6])
    )


def test_elementwise_multiply():
    assert np.array_equal(
        elementwise_multiply(np.array([1, 2, 3]), np.array([4, 5, 6])),
        np.array([4, 10, 18])
    )


def test_dot_product():
    assert dot_product(np.array([1, 2, 3]), np.array([4, 5, 6])) == 32
    assert dot_product(np.array([2, 0]), np.array([3, 5])) == 6


def test_matrix_multiply():
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[2, 0], [1, 2]])
    assert np.array_equal(matrix_multiply(A, B), A @ B)


def test_matrix_determinant():
    A = np.array([[1, 2], [3, 4]])
    assert round(matrix_determinant(A), 5) == -2.0


def test_matrix_inverse():
    A = np.array([[1, 2], [3, 4]])
    invA = matrix_inverse(A)
    assert np.allclose(A @ invA, np.eye(2))


def test_solve_linear_system():
    A = np.array([[2, 1], [1, 3]])
    b = np.array([1, 2])
    x = solve_linear_system(A, b)
    assert np.allclose(A @ x, b)


def test_load_dataset():
    # Для теста создадим временный файл
    test_data = "math,physics,informatics\n78,81,90\n85,89,88"
    with open("test_data.csv", "w") as f:
        f.write(test_data)
    try:
        data = load_dataset("test_data.csv")
        assert data.shape == (2, 3)
        assert np.array_equal(data[0], [78, 81, 90])
    finally:
        os.remove("test_data.csv")


def test_statistical_analysis():
    data = np.array([10, 20, 30])
    result = statistical_analysis(data)
    assert result["mean"] == 20
    assert result["min"] == 10
    assert result["max"] == 30


def test_normalization():
    data = np.array([0, 5, 10])
    norm = normalize_data(data)
    assert np.allclose(norm, np.array([0, 0.5, 1]))


def test_plot_histogram():
    # Просто проверяем, что функция не падает
    data = np.array([1, 2, 3, 4, 5])
    plot_histogram(data, False)


def test_plot_heatmap():
    matrix = np.array([[1, 0.5, 0], [0.5, 1, 0.7], [0, 0.7, 1]])
    plot_heatmap(matrix, False)


def test_plot_line():
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    plot_line(x, y, False)


def test_vector_add_shape_mismatch():
    """Проверка, что сложение векторов разной длины вызывает ValueError."""
    a = np.array([1, 2, 3])
    b = np.array([4, 5])
    with pytest.raises(ValueError, match="operands could not be broadcast together"):
        vector_add(a, b)


def test_elementwise_multiply_shape_mismatch():
    """Проверка, что поэлементное умножение с несовместимыми формами вызывает ValueError."""
    a = np.array([[1, 2], [3, 4]])
    b = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="operands could not be broadcast together"):
        elementwise_multiply(a, b)


def test_dot_product_length_mismatch():
    """Проверка, что скалярное произведение векторов разной длины вызывает ValueError."""
    a = np.array([1, 2, 3])
    b = np.array([4, 5])
    with pytest.raises(ValueError, match="shapes .* not aligned"):
        dot_product(a, b)


def test_matrix_multiply_incompatible():
    """Проверка, что умножение матриц с несовместимыми размерами вызывает ValueError."""
    A = np.array([[1, 2, 3], [4, 5, 6]])
    B = np.array([[1, 2], [3, 4]])
    with pytest.raises(ValueError, match="Input operand .* has a mismatch in its"):
        matrix_multiply(A, B)


def test_matrix_determinant_non_square():
    """Проверка, что определитель вычисляется только для квадратной матрицы."""
    A = np.array([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError, match="Last 2 dimensions of the array must be square"):
        matrix_determinant(A)


def test_matrix_inverse_non_square():
    """Проверка, что обратная матрица существует только для квадратной."""
    A = np.array([[1, 2, 3], [4, 5, 6]])
    with pytest.raises(ValueError, match="Last 2 dimensions of the array must be square"):
        matrix_inverse(A)


def test_matrix_inverse_singular():
    """Проверка, что для вырожденной матрицы выбрасывается LinAlgError."""
    A = np.array([[1, 2], [1, 2]])
    with pytest.raises(np.linalg.LinAlgError, match="Singular matrix"):
        matrix_inverse(A)


def test_solve_linear_system_non_square():
    """Решение системы Ax = b только для квадратной A."""
    A = np.array([[1, 2, 3], [4, 5, 6]])
    b = np.array([1, 2])
    with pytest.raises(ValueError, match="Last 2 dimensions of the array must be square"):
        solve_linear_system(A, b)


def test_solve_linear_system_singular():
    """Решение системы с вырожденной матрицей вызывает LinAlgError."""
    A = np.array([[1, 2], [1, 2]])
    b = np.array([1, 2])
    with pytest.raises(np.linalg.LinAlgError, match="Singular matrix"):
        solve_linear_system(A, b)


def test_solve_linear_system_b_dim_mismatch():
    """Проверка несоответствия размерностей b и A."""
    A = np.array([[1, 2], [3, 4]])
    b = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="Input operand .* has a mismatch in its"):
        solve_linear_system(A, b)


def test_load_dataset_file_not_found():
    """Проверка, что при отсутствии файла выбрасывается FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_dataset("non_existent_file.csv")


def test_normalize_data_constant_input():
    """Проверка поведения при одинаковых значениях (max-min = 0)."""
    data = np.array([5, 5, 5])
    result = normalize_data(data)
    assert np.all(np.isinf(result) | np.isnan(result)), \
        "При constant input результат должен содержать inf или nan"


if __name__ == "__main__":
    print("Запустите python -m pytest code/s2_l2/test.py -v для проверки лабораторной работы.")
