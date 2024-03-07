# from pathlib import Path
# print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())

import numpy as np

from typing import Optional

def pad_with_zeros(arr: np.ndarray, number_of_zeros: Optional[int] = None) -> np.ndarray:
    """
    Pad an np.array with a specified number of zeros at the end.

    Parameters:
        arr (numpy.ndarray): Input array.
        number_of_zeros (int, optional): Number of zeros to add at the end of the array.
            If not provided, the number of zeros will be calculated based on the next power of 2.
    
    Returns:
        numpy.ndarray: Padded array.
    """

    if not isinstance(arr, np.ndarray):
        raise TypeError("Input arr must be a numpy array")
    
    if number_of_zeros is None:
        number_of_zeros = int(2 ** np.ceil(np.log2(len(arr))) - len(arr))
    
    return np.pad(arr, (0, number_of_zeros), mode='constant')


