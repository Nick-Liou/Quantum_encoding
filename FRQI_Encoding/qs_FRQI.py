import numpy as np
from qiskit import QuantumCircuit , QuantumRegister
from qiskit.circuit.library import MCXGate
from qiskit.circuit.library import CRYGate , RYGate

# Add the parent directory of the current script's directory to the Python path
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path

# Import Local modules
from Utilities.utils import pad_with_zeros

# Typing stuff
from typing import Any, Union, Optional



def FRQIEncoding(data : Union[list, np.ndarray] , min_val : Optional[float] = None , max_val : Optional[float]= None ) -> QuantumCircuit :

    # pad with zeros if needed
    padded_data = pad_with_zeros(np.array(data))

    # Covnert data to 2D to support multipule values per address
    if np.ndim(padded_data) == 1:         
        padded_data = np.atleast_2d(padded_data)        
        padded_data = np.reshape(padded_data,padded_data.shape[::-1])
    elif np.ndim(padded_data) == 2:

        print("padded_data.shape" , padded_data.shape)
    else:
        raise TypeError("Input array must be 1D or 2D")
    
        

    # Calculate min_val if it is None, otherwise use the provided value
    min_val = np.min(padded_data) if min_val is None else min_val
    # Calculate max_val if it is None, otherwise use the provided value
    max_val = np.max(padded_data) if max_val is None else max_val

        
    
    # Normalize to the range [0, pi/2]
    if  min_val == max_val :        
        # Create an array of zeros with the same shape
        theta = np.zeros_like(padded_data)
    else:
        # Normalize to the range [0, pi/2]
        theta  = (padded_data - min_val) * (np.pi / 2) / (max_val - min_val)
        
    print("theta:" , theta)
    
    number_of_qubits = int ( np.ceil(np.log2(len(padded_data))) )

    data_dimensionality = np.size(padded_data, axis=1) 

    # Indices of data
    qr1 = QuantumRegister(number_of_qubits, "a") 
    # Data
    qr2 = QuantumRegister(data_dimensionality, "d")    

    
    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(qr1 ,qr2 )

    
    # Create a superposition for all the addresses
    qc.h(range(number_of_qubits))


    # Set up the data 
    for i in range(len(padded_data)):
        qc.barrier()
        for j in range(data_dimensionality):      
                  
            qubits_ids = list(range(number_of_qubits)) + [number_of_qubits + data_dimensionality - j - 1]

            qc.append(RYGate(2*theta[i][j]).control(num_ctrl_qubits=number_of_qubits, ctrl_state=i), qubits_ids )
            # qc.append(RYGate(theta[i]).control(num_ctrl_qubits=number_of_qubits, ctrl_state=i), qubits_ids )
    
    qc.barrier()

    # Return the final quantum circuit
    return qc



    
if __name__=="__main__": 

    # array = [0, 1, 2, -1.00 , -4 ]


    # data_length = 16
    # data = np.random.randint(low=0, high=3, size=data_length)
    # data = np.random.rand(data_length) * 20  - 10 

    # data = [1, -1, 3, 5, -1, 4, 6, 7]  # Example input data   
    # data = [1, 1, 1, 1, 1, 0, 0, 1]  # Example input data     
    # data = [1, 1, 1, 1]  # Example input data     
    # data = [1, 1, 0, 1]  # Example input data    
    
    
    data = [[1, 2, 3], [4 , 5, 6]]
    data = [[0, 0, 0], [0, 0, 0], [0, 0,0]] 

    qc = FRQIEncoding(data )
    print(qc)


