import numpy as np
from qiskit import QuantumCircuit

def BasisEncoding(data , bit_depth=4) :

    # pad with zeros if needed
    padded_data = pad_with_zeros(data) 
    
    number_of_qubits = int ( np.ceil(np.log2(len(padded_data))) )
    

    if all_integers(padded_data):
        bin_data = convert_to_binary(padded_data)
        pass


    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(number_of_qubits + bit_depth)

    qc.h(range(number_of_qubits))
    
    for i in range(len(padded_data)):
        padded_data[i]

    
    
    # Return the final quantum circuit
    return qc 




def all_integers(arr):
    for element in arr:        
        # Check if the element is an integer or a float representing an integer
        if not isinstance(element, int) and not element.is_integer():
            return False
    return True


def convert_to_binary(arr):
    binary_array = []
    max_abs_value = max(abs(num) for num in arr)
    max_length = len(np.binary_repr(int(max_abs_value)))  # Calculate the maximum number of bits needed
    
    if min(arr) < 0 :
        max_length += 1 

    for num in arr:
        binary_num = np.binary_repr(int(num), width=max_length)  # Convert the number to binary with specified width
        binary_array.append(binary_num)

    return binary_array


# Refactor it outside !
def pad_with_zeros(arr, number_of_zeros = None ):
    """
    Pad an np.array with a specified number of zeros at the end.

    Parameters:
        arr (numpy.ndarray): Input array.
        number_of_zeros (int, optional): Number of zeros to add at the end of the array.
            If not provided, the number of zeros will be calculated based on the next power of 2.
    
    Returns:
        numpy.ndarray: Padded array.
    """
    if number_of_zeros == None :
        number_of_zeros = int( 2 ** np.ceil( np.log2(len(arr)) ) -  len(arr) )

    # Create an array of zeros with the desired length
    zeros_array = np.zeros(number_of_zeros, dtype=arr.dtype)
    
    # Concatenate the original array with the zeros array
    padded_arr = np.concatenate((arr, zeros_array))
    
    return padded_arr

