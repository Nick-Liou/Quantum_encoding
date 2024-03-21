# from pathlib import Path
# print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


# Add the parent directory of the current script's directory to the Python path
import sys
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path

import time
# 
import numpy as np
from typing import Callable, Optional, Union
from qiskit.result.result import Result


import pytest

# Custom libraries
from General_encoding import encode_data

from Utilities.utils import pad_with_zeros

from Amplitude_Encoding_QPIE.qs_AmplitudeEncoding   import AmplitudeEncoding
from Angle_encoding_FRQI.qs_AngleEncoding           import AngleEncoding
from Basis_Encoding_NEQR.qs_BasisEncoding           import BasisEncoding
from Basis_Encoding_NEQR.qs_BasisEncoding           import convert_to_bin

TOLERANCE = 1e-6

def Amplitude_Expected_statevector( data_to_encode : Union[list, np.ndarray] ) -> np.ndarray:

    # pad with zeros if needed
    padded_data = pad_with_zeros(np.array(data_to_encode))
    # Normalize data 
    expected_statevector: np.ndarray = padded_data / np.sqrt(sum(np.abs(padded_data)**2))  + 0j

    return expected_statevector 




def AngleEncoding_Expected_statevector(data : Union[list, np.ndarray] , min_val : Optional[float] = None , max_val : Optional[float]= None ) -> np.ndarray:
    """
    Calculates the statevector from a list of data.

    Args:
        data (list or numpy.ndarray): The list or array of values to be encoded.
        min_val (float, optional): The minimum value of the data. If not provided, it will be calculated from the data. Defaults to None.
        max_val (float, optional): The maximum value of the data. If not provided, it will be calculated from the data. Defaults to None.

    Returns:
        numpy.ndarray: Statevector corresponding to the given data.
    """
    
    data = np.array(data)

    # Calculate min_val if it is None, otherwise use the provided value
    min_val = np.min(data) if min_val is None else min_val
    # Calculate max_val if it is None, otherwise use the provided value
    max_val = np.max(data) if max_val is None else max_val

    angles : Union[list, np.ndarray]
    if len(data) == 1 and min_val == max_val :
        angles = [0]
    else:
        # Normalize to the range [0, pi/2]
        angles = (data - min_val) * (np.pi / 2) / (max_val - min_val)
    

    statevector = np.array([np.cos(angles[0]), np.sin(angles[0])])

    for angle in angles[1:]:
        statevector = np.kron(np.array([np.cos(angle), np.sin(angle)]) , statevector )

    return statevector


def BasisEncoding_Expected_statevector(data : Union[list, np.ndarray]) -> np.ndarray:
    
    # pad with zeros if needed
    padded_data = pad_with_zeros(np.array(data))
    
    number_of_qubits = int ( np.ceil(np.log2(len(padded_data))) )
    
    # For now only works for integeres
    bin_data , bit_depth = convert_to_bin(padded_data)

    expected_statevector = np.zeros(2**(number_of_qubits+bit_depth))

    # print("len(bin_data) = " , len(bin_data))
    for i , element  in enumerate(bin_data) :
        # print(i , element)
        #  First term is for the address second term is for the vaule
        # index = i*2**bit_depth + int(element,2)
        index = i + int(element,2)*2**number_of_qubits
        # print(f"i {i} data {padded_data[i]}  bin: {element}  new_data {int(element,2)}  index {index}")

        # print(index)
        expected_statevector[index] = 1 

    
    expected_statevector = expected_statevector / np.sqrt(sum(np.abs(expected_statevector)**2))  + 0j

    return expected_statevector


from enum import Enum
class DataType(Enum):
    ANALOG = 0
    DIGITAL = 1

@pytest.mark.parametrize("encoding_function,expected_statevector_gen,data_type", 
                         [(AmplitudeEncoding, Amplitude_Expected_statevector,DataType.ANALOG),
                          (AngleEncoding, AngleEncoding_Expected_statevector,DataType.ANALOG),
                          (BasisEncoding, BasisEncoding_Expected_statevector,DataType.DIGITAL)])
def test_Encodings_multiple_cases(encoding_function: Callable , expected_statevector_gen: Callable , data_type: DataType) -> None:
    # Test with known input data
    result : Result
    data_to_encode = [1, 2, 3]
    _ , result = encode_data(data_to_encode, encoding_function)
    state_vector = result.get_statevector().data
    expected_statevector = expected_statevector_gen(data_to_encode)
    # print("Actual statevector",state_vector)
    # print("Expected statevector" , expected_statevector)
    assert np.allclose(state_vector, expected_statevector, atol=TOLERANCE)

    # Test with edge cases
    edge_cases : list[list[Union[int, float]]] = [
        # [],  # Empty input
        # [0],  # Single element input
        # [0, 0],  # All zeros
        [1],  # Single element non-zero
        [0, 1],  # Zero followed by non-zero
        [1, 0],  # Non-zero followed by zero
        [1, -1],  # Positive and negative values        
        [7, -4],  # Positive and negative values
        [1, -1, 3, 5],  # Positive and negative values
        [1, 1, 1, 1, 1, 0, 0, 1],
        [1, -1, 3, 5, -1, 4, 6, 7],  # Positive and negative values
        [1, -1, 3, 5, -1, 4, 6, 7, -4],  # Positive and negative values
        [1, -1, 3, -10, 8, 13, -8, -3, -5, 13, 16, 18, 32],  # Positive and negative values
    ]

    if data_type == DataType.ANALOG:
        edge_cases.extend([
            [0.4, -1.4],
            [4.6, -0.5, 3.6, 1.6],
            [1.3, 0.5, 1.6, -1.4, 5, -4.24, 13],
            [1e10, -1e10],  # Large positive and negative values
            [1e-10, 1e-20],  # Small positive values
            [1e-10, -1e-20],  # Small positive and negative values
            [-1e-10, -1e-20],  # Small negative values
            [1e10, 1e-20],  # Large positive and small positive values
            [1e-10, 1e10],  # Small positive and large positive values
            [-1e-10, 1e10],  # Small negative and large positive values
        ])


    for case in edge_cases:
        # print("\n\nCase : " ,case)
        _, result = encode_data(case, encoding_function)
        state_vector = result.get_statevector().data
        expected_statevector = expected_statevector_gen(case)
        
        # print(f"Actual statevector {len(state_vector)} :",state_vector)
        # print(f"Expected statevector {len(expected_statevector)} :" , expected_statevector)
        # print(f"Diff actual - expected" ,state_vector -expected_statevector )
        
        # print("Indices of non-zero elements Actual statevector  :", np.nonzero(state_vector))
        # print("Indices of non-zero elements Expected statevector:", np.nonzero(expected_statevector))

        assert np.allclose(state_vector, expected_statevector, atol=TOLERANCE)

    # Test with multiple randomly generated inputs
    num_tests = 10  # Adjust the number of tests as needed
    for _ in range(num_tests):
        # Generate random input data within a certain range
        random_data : np.ndarray
        if data_type == DataType.ANALOG:
            random_data = np.random.uniform(low=-16, high=15, size=np.random.randint(1, 25 ))
        elif data_type == DataType.DIGITAL:
            random_data = np.random.randint(low=-16, high=15, size=np.random.randint(1, 25 ))
        
        # print("\n\n",random_data)
        _, result = encode_data(random_data, encoding_function)
        state_vector = result.get_statevector().data
        expected_statevector = expected_statevector_gen(random_data)
        # print(len(state_vector))
        assert np.allclose(state_vector, expected_statevector, atol=TOLERANCE)



if __name__ == "__main__":
    
    test_Encodings_multiple_cases(BasisEncoding, BasisEncoding_Expected_statevector, DataType.DIGITAL)
