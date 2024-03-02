from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import numpy as np
import pytest
# from Quantum_encoding.Utilities.utils import pad_with_zeros

# from ..Utilities.utils import pad_with_zeros
from ...Quantum_encoding.Utilities.utils import pad_with_zeros

# Test cases for pad_with_zeros function

def test_pad_with_zeros_basic():
    arr = np.array([1, 2, 3])
    padded_arr = pad_with_zeros(arr, 2)
    assert np.array_equal(padded_arr, np.array([1, 2, 3, 0, 0]))

def test_pad_with_zeros_default():
    arr = np.array([1, 2, 3])
    padded_arr = pad_with_zeros(arr)
    assert np.array_equal(padded_arr, np.array([1, 2, 3, 0]))

def test_pad_with_zeros_large():
    arr = np.array([1, 2, 3])
    padded_arr = pad_with_zeros(arr, 10)
    assert np.array_equal(padded_arr, np.array([1, 2, 3] + [0]*10))

def test_pad_with_zeros_empty_array():
    arr = np.array([])
    padded_arr = pad_with_zeros(arr, 5)
    assert np.array_equal(padded_arr, np.array([0]*5))

def test_pad_with_zeros_no_zeros():
    arr = np.array([1, 2, 3])
    padded_arr = pad_with_zeros(arr, 0)
    assert np.array_equal(padded_arr, arr)

def test_pad_with_zeros_negative_zeros():
    arr = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        padded_arr = pad_with_zeros(arr, -5)

def test_pad_with_zeros_float_zeros():
    arr = np.array([1, 2, 3])
    with pytest.raises(TypeError):
        padded_arr = pad_with_zeros(arr, 5.5)

def test_pad_with_zeros_non_array_input():
    with pytest.raises(TypeError):
        padded_arr = pad_with_zeros([1, 2, 3], 5)

