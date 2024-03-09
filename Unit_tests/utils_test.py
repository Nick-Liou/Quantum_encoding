# from pathlib import Path
# print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


# Add the parent directory of the current script's directory to the Python path
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path


# Import External modules
import numpy as np
import pytest

# Import Local modules
from Utilities.utils import pad_with_zeros


# Test cases for pad_with_zeros function
    
def test_pad_with_zeros_default() -> None :
    arr = np.array([1, 2, 3])
    padded_arr = pad_with_zeros(arr)
    assert np.array_equal(padded_arr, np.array([1, 2, 3, 0]))

    
def test_pad_with_zeros_default_single_input() -> None :
    arr = np.array([1])
    padded_arr = pad_with_zeros(arr)
    assert np.array_equal(padded_arr, np.array([1, 0]))

def test_pad_with_zeros_basic() -> None :
    arr = np.array([1, 2, 3])
    padded_arr = pad_with_zeros(arr, 2)
    assert np.array_equal(padded_arr, np.array([1, 2, 3, 0, 0])) 

def test_pad_with_zeros_large() -> None :
    arr = np.array([1, 2, 3])
    padded_arr = pad_with_zeros(arr, 10)
    assert np.array_equal(padded_arr, np.array([1, 2, 3] + [0]*10))

def test_pad_with_zeros_empty_array() -> None :
    arr = np.array([])
    padded_arr = pad_with_zeros(arr, 5)
    assert np.array_equal(padded_arr, np.array([0]*5))

def test_pad_with_zeros_no_zeros() -> None :
    arr = np.array([1, 2, 3])
    padded_arr = pad_with_zeros(arr, 0)
    assert np.array_equal(padded_arr, arr)

def test_pad_with_zeros_negative_zeros() -> None :
    arr = np.array([1, 2, 3])
    with pytest.raises(ValueError):
        padded_arr = pad_with_zeros(arr, -5)

def test_pad_with_zeros_float_zeros() -> None :
    arr = np.array([1, 2, 3])
    with pytest.raises(TypeError):
        padded_arr = pad_with_zeros(arr, 5.5)  # type: ignore[arg-type]

def test_pad_with_zeros_string_input() -> None :
    with pytest.raises(TypeError):
        padded_arr = pad_with_zeros("not_an_array", 5) # type: ignore[arg-type]

def test_pad_with_zeros_list_input() -> None :
    with pytest.raises(TypeError):
        padded_arr = pad_with_zeros([1, 2, 3], 5) # type: ignore[arg-type]
