import numpy as np
from qiskit import QuantumCircuit , QuantumRegister
from qiskit.circuit.library import MCXGate

def BasisEncoding(data ) :

    # pad with zeros if needed
    padded_data = pad_with_zeros(data) 
    
    number_of_qubits = int ( np.ceil(np.log2(len(padded_data))) )
    
    # For now only works for integeres
    bin_data , bit_depth = convert_to_bin(padded_data)

    
    # Indices of data
    qr1 = QuantumRegister(number_of_qubits, "q") 
    # Data
    qr2 = QuantumRegister(bit_depth, "a")    

    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(qr1 ,qr2 )


    # Create a superposition for all the indices 
    qc.h(range(number_of_qubits))
    
    for i in range(len(padded_data)):
        # padded_data[i]

        for j in range(bit_depth):
            
            if bin_data[i][j] == '1' :

                array = list(range(number_of_qubits)) + [number_of_qubits + bit_depth - j - 1]

                qc.append(MCXGate(num_ctrl_qubits=number_of_qubits, ctrl_state=i), array )
        
        # qc.barrier()

         

    
    
    # Return the final quantum circuit
    return qc 


def convert_to_bin(arr):

    
    if all_integers(arr):
        return int_to_binary(arr)        
    else:
        raise("Float representation not yet")
        # Add the float case
    


def all_integers(arr):
    for element in arr:        
        # Check if the element is an integer or a float representing an integer
        if not isinstance(element, int) and not element.is_integer():
            return False
    return True


def int_to_binary(arr):
    binary_array = []
    max_abs_value = max(map(abs, arr))
    max_length = len(np.binary_repr(int(max_abs_value)))  # Calculate the maximum number of bits needed
    
    # Add one bit for the "sign" bit
    if min(arr) < 0 :
        max_length += 1 

    binary_array = list(map(lambda num: np.binary_repr(int(num), width=max_length), arr))
    
    return binary_array , max_length


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



if __name__=="__main__": 

    array = [0, 1, 2, -1.00 , -4 ]

    print(all_integers(array) ) 

    print( int_to_binary(array) )


    pass