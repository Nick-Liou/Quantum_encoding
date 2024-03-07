# from pathlib import Path
# print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


# Add the parent directory of the current script's directory to the Python path
import sys
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path

# 
import numpy as np

# Custom libraries
from General_encoding import encode_data

from Utilities.utils import pad_with_zeros

from Amplitude_Encoding_QPIE.qs_AmplitudeEncoding   import AmplitudeEncoding
from Angle_encoding_FRQI.qs_AngleEncoding           import AngleEncoding
from Basis_Encoding_NEQR.qs_BasisEncoding           import BasisEncoding



def test_AmplitudeEncoding() -> None :

    data_to_encode = [1, 2, 3]
    
    _ , result  = encode_data( data_to_encode ,  AmplitudeEncoding)
    state_vector = result.get_statevector().data
    
    # pad with zeros if needed
    padded_data = pad_with_zeros(np.array(data_to_encode))
    # Normalize data 
    expected_statevector = padded_data / np.sqrt(sum(np.abs(padded_data)**2))  + 0j

    tolerance = 1e-6
    # Check if the actual and expected values are equal within the tolerance
    assert np.allclose(state_vector,  expected_statevector , atol=tolerance)
        

test_AmplitudeEncoding()