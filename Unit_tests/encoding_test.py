# from pathlib import Path
# print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


# Add the parent directory of the current script's directory to the Python path
import sys
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path

# 
import numpy as np
from typing import Callable, Union

# Custom libraries
from General_encoding import encode_data

from Utilities.utils import pad_with_zeros

from Amplitude_Encoding_QPIE.qs_AmplitudeEncoding   import AmplitudeEncoding
from Angle_encoding_FRQI.qs_AngleEncoding           import AngleEncoding
from Basis_Encoding_NEQR.qs_BasisEncoding           import BasisEncoding

def Amplitude_Expected_statevector( data_to_encode : Union[list, np.ndarray] ) -> np.ndarray:

    # pad with zeros if needed
    padded_data = pad_with_zeros(np.array(data_to_encode))
    # Normalize data 
    expected_statevector = padded_data / np.sqrt(sum(np.abs(padded_data)**2))  + 0j

    return expected_statevector 

TOLERANCE = 1e-6


def test_AmplitudeEncoding_multiple_cases() -> None:
    # Test with known input data
    data_to_encode = [1, 2, 3]
    _, result = encode_data(data_to_encode, AmplitudeEncoding)
    state_vector = result.get_statevector().data
    expected_statevector = Amplitude_Expected_statevector(data_to_encode)
    assert np.allclose(state_vector, expected_statevector, atol=TOLERANCE)

    # Test with edge cases
    edge_cases = [
        # [],  # Empty input
        # [0],  # Single element input
        # [0, 0],  # All zeros
        [1],  # Single element non-zero
        [0, 1],  # Zero followed by non-zero
        [1, 0],  # Non-zero followed by zero
        [1, -1],  # Positive and negative values
        [1e10, -1e10],  # Large positive and negative values
        [1e-10, 1e-20],  # Small positive values
        [1e-10, -1e-20],  # Small positive and negative values
        [-1e-10, -1e-20],  # Small negative values
        [1e10, 1e-20],  # Large positive and small positive values
        [1e-10, 1e10],  # Small positive and large positive values
        [-1e-10, 1e10],  # Small negative and large positive values
    ]

    for case in edge_cases:
        # print("Case : " ,case)
        _, result = encode_data(case, AmplitudeEncoding)
        state_vector = result.get_statevector().data
        expected_statevector = Amplitude_Expected_statevector(case)
        assert np.allclose(state_vector, expected_statevector, atol=TOLERANCE)

    # Test with multiple randomly generated inputs
    num_tests = 10  # Adjust the number of tests as needed
    for _ in range(num_tests):
        # Generate random input data within a certain range
        random_data = np.random.uniform(low=-100, high=100, size=np.random.randint(1, 32 ))
        _, result = encode_data(random_data, AmplitudeEncoding)
        state_vector = result.get_statevector().data
        expected_statevector = Amplitude_Expected_statevector(random_data)
        assert np.allclose(state_vector, expected_statevector, atol=TOLERANCE)




def test_Encodings_multiple_cases(encoding_function: Callable , expected_statevector_gen: Callable ) -> None:
    # Test with known input data
    data_to_encode = [1, 2, 3]
    _, result = encode_data(data_to_encode, encoding_function)
    state_vector = result.get_statevector().data
    expected_statevector = expected_statevector_gen(data_to_encode)
    assert np.allclose(state_vector, expected_statevector, atol=TOLERANCE)

    # Test with edge cases
    edge_cases = [
        # [],  # Empty input
        # [0],  # Single element input
        # [0, 0],  # All zeros
        [1],  # Single element non-zero
        [0, 1],  # Zero followed by non-zero
        [1, 0],  # Non-zero followed by zero
        [1, -1],  # Positive and negative values
        [1e10, -1e10],  # Large positive and negative values
        [1e-10, 1e-20],  # Small positive values
        [1e-10, -1e-20],  # Small positive and negative values
        [-1e-10, -1e-20],  # Small negative values
        [1e10, 1e-20],  # Large positive and small positive values
        [1e-10, 1e10],  # Small positive and large positive values
        [-1e-10, 1e10],  # Small negative and large positive values
    ]

    for case in edge_cases:
        # print("Case : " ,case)
        _, result = encode_data(case, encoding_function)
        state_vector = result.get_statevector().data
        expected_statevector = expected_statevector_gen(case)
        assert np.allclose(state_vector, expected_statevector, atol=TOLERANCE)

    # Test with multiple randomly generated inputs
    num_tests = 10  # Adjust the number of tests as needed
    for _ in range(num_tests):
        # Generate random input data within a certain range
        random_data = np.random.uniform(low=-100, high=100, size=np.random.randint(1, 32 ))
        _, result = encode_data(random_data, AmplitudeEncoding)
        state_vector = result.get_statevector().data
        expected_statevector = Amplitude_Expected_statevector(random_data)
        assert np.allclose(state_vector, expected_statevector, atol=TOLERANCE)

