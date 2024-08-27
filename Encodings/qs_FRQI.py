# -*- coding: utf-8 -*-
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
    """
    Encodes the given data into a quantum circuit using FRQI Encoding.

    Args:
        data (list or numpy.ndarray): The list or array of values to be encoded.
        min_val (float, optional): The minimum value of the data. If not provided, it will be calculated from the data. Defaults to None.
        max_val (float, optional): The maximum value of the data. If not provided, it will be calculated from the data. Defaults to None.

    Returns:
        QuantumCircuit: The quantum circuit representing the FRQI Encoding of the data.

        
    Example 1 (floating numbers):
        >>> data = [0.5, 0.8, 0.3, 0.6]  # Example input data
        >>> min_val = 0.0  # Minimum value
        >>> max_val = 1.0  # Maximum value
        >>> qc = FRQIEncoding(data, min_val, max_val)
        >>> print(qc)
                 ┌───┐
            a_0: ┤ H ├─────o──────────■────────────o───────────■──────
                 ├───┤     │          │            │           │
            a_1: ┤ H ├─────o──────────o────────────■───────────■──────
                 └───┘┌────┴────┐┌────┴─────┐┌─────┴─────┐┌────┴─────┐
              d: ─────┤ Ry(π/2) ├┤ Ry(4π/5) ├┤ Ry(3π/10) ├┤ Ry(3π/5) ├
                      └─────────┘└──────────┘└───────────┘└──────────┘

    Example 2 (positive integers):
        >>> data = [0, 172, 38, 246]   # Example input data
        >>> min_val = 0     # Minimum value
        >>> max_val = 255   # Maximum value
        >>> qc = FRQIEncoding(data, min_val, max_val)
        >>> print(qc)

                 ┌───┐
            a_0: ┤ H ├────o──────────■─────────────o─────────────■───────
                 ├───┤    │          │             │             │
            a_1: ┤ H ├────o──────────o─────────────■─────────────■───────
                 └───┘┌───┴───┐┌─────┴─────┐┌──────┴──────┐┌─────┴──────┐
              d: ─────┤ Ry(0) ├┤ Ry(2.119) ├┤ Ry(0.46816) ├┤ Ry(3.0307) ├
                      └───────┘└───────────┘└─────────────┘└────────────┘
          
        
    Example 3 (positive integers):
        >>> data = [159, 53, 139, 89, 120, 247, 40, 220, 173, 60, 89, 32, 181, 59, 13, 94]   # Example input data
        >>> min_val = 0     # Minimum value
        >>> max_val = 255   # Maximum value
        >>> qc = FRQIEncoding(data, min_val, max_val)
        >>> print(qc)

                 ┌───┐
            a_0: ┤ H ├──────o──────────────■─────────────o─────────────■─────────────o─────────────■────────────o─────────────■─────────────o─────────────■─────────────o──────────────■─────────────o──────────────■──────────────o─────────────■───────
                 ├───┤      │              │             │             │             │             │            │             │             │             │             │              │             │              │              │             │
            a_1: ┤ H ├──────o──────────────o─────────────■─────────────■─────────────o─────────────o────────────■─────────────■─────────────o─────────────o─────────────■──────────────■─────────────o──────────────o──────────────■─────────────■───────
                 ├───┤      │              │             │             │             │             │            │             │             │             │             │              │             │              │              │             │
            a_2: ┤ H ├──────o──────────────o─────────────o─────────────o─────────────■─────────────■────────────■─────────────■─────────────o─────────────o─────────────o──────────────o─────────────■──────────────■──────────────■─────────────■───────
                 ├───┤      │              │             │             │             │             │            │             │             │             │             │              │             │              │              │             │
            a_3: ┤ H ├──────o──────────────o─────────────o─────────────o─────────────o─────────────o────────────o─────────────o─────────────■─────────────■─────────────■──────────────■─────────────■──────────────■──────────────■─────────────■───────
                 └───┘┌─────┴──────┐┌──────┴──────┐┌─────┴──────┐┌─────┴──────┐┌─────┴──────┐┌─────┴─────┐┌─────┴──────┐┌─────┴──────┐┌─────┴──────┐┌─────┴──────┐┌─────┴──────┐┌──────┴──────┐┌─────┴──────┐┌──────┴──────┐┌──────┴──────┐┌─────┴──────┐
              d: ─────┤ Ry(1.9589) ├┤ Ry(0.65296) ├┤ Ry(1.7125) ├┤ Ry(1.0965) ├┤ Ry(1.4784) ├┤ Ry(3.043) ├┤ Ry(0.4928) ├┤ Ry(2.7104) ├┤ Ry(2.1314) ├┤ Ry(0.7392) ├┤ Ry(1.0965) ├┤ Ry(0.39424) ├┤ Ry(2.2299) ├┤ Ry(0.72688) ├┤ Ry(0.16016) ├┤ Ry(1.1581) ├
                      └────────────┘└─────────────┘└────────────┘└────────────┘└────────────┘└───────────┘└────────────┘└────────────┘└────────────┘└────────────┘└────────────┘└─────────────┘└────────────┘└─────────────┘└─────────────┘└────────────┘

    Example 4 (positive integers in 2D array):
        >>> data = [[159, 53, 139, 89], [120, 247, 40, 220], [173, 60, 89, 32], [181, 59, 13, 94]]   # Example input data
        >>> min_val = 0     # Minimum value
        >>> max_val = 255   # Maximum value
        >>> qc = FRQIEncoding(data, min_val, max_val)
        >>> print(qc)
        
                 ┌───┐
            a_0: ┤ H ├──────o──────────────o─────────────o─────────────o─────────────■─────────────■────────────■─────────────■─────────────o─────────────o─────────────o──────────────o─────────────■──────────────■──────────────■─────────────■───────
                 ├───┤      │              │             │             │             │             │            │             │             │             │             │              │             │              │              │             │       
            a_1: ┤ H ├──────o──────────────o─────────────o─────────────o─────────────o─────────────o────────────o─────────────o─────────────■─────────────■─────────────■──────────────■─────────────■──────────────■──────────────■─────────────■───────
                 └───┘      │              │             │       ┌─────┴──────┐      │             │            │       ┌─────┴──────┐      │             │             │       ┌──────┴──────┐      │              │              │       ┌─────┴──────┐
            d_0: ───────────┼──────────────┼─────────────┼───────┤ Ry(1.0965) ├──────┼─────────────┼────────────┼───────┤ Ry(2.7104) ├──────┼─────────────┼─────────────┼───────┤ Ry(0.39424) ├──────┼──────────────┼──────────────┼───────┤ Ry(1.1581) ├
                            │              │       ┌─────┴──────┐└────────────┘      │             │      ┌─────┴──────┐└────────────┘      │             │       ┌─────┴──────┐└─────────────┘      │              │       ┌──────┴──────┐└────────────┘
            d_1: ───────────┼──────────────┼───────┤ Ry(1.7125) ├────────────────────┼─────────────┼──────┤ Ry(0.4928) ├────────────────────┼─────────────┼───────┤ Ry(1.0965) ├─────────────────────┼──────────────┼───────┤ Ry(0.16016) ├──────────────
                            │       ┌──────┴──────┐└────────────┘                    │       ┌─────┴─────┐└────────────┘                    │       ┌─────┴──────┐└────────────┘                     │       ┌──────┴──────┐└─────────────┘
            d_2: ───────────┼───────┤ Ry(0.65296) ├──────────────────────────────────┼───────┤ Ry(3.043) ├──────────────────────────────────┼───────┤ Ry(0.7392) ├───────────────────────────────────┼───────┤ Ry(0.72688) ├─────────────────────────────
                      ┌─────┴──────┐└─────────────┘                            ┌─────┴──────┐└───────────┘                            ┌─────┴──────┐└────────────┘                             ┌─────┴──────┐└─────────────┘
            d_3: ─────┤ Ry(1.9589) ├───────────────────────────────────────────┤ Ry(1.4784) ├─────────────────────────────────────────┤ Ry(2.1314) ├───────────────────────────────────────────┤ Ry(2.2299) ├────────────────────────────────────────────
                      └────────────┘                                           └────────────┘                                         └────────────┘                                           └────────────┘

    """

    # pad with zeros if needed
    padded_data = pad_with_zeros(np.array(data))

    # Covnert data to 2D to support multipule values per address
    if np.ndim(padded_data) == 1:         
        padded_data = np.atleast_2d(padded_data)        
        padded_data = np.reshape(padded_data,padded_data.shape[::-1])
    elif np.ndim(padded_data) == 2:
        pass
        # print("padded_data.shape" , padded_data.shape)
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
        for j in range(data_dimensionality):      
                  
            qubits_ids = list(range(number_of_qubits)) + [number_of_qubits + data_dimensionality - j - 1]

            qc.append(RYGate(2*theta[i][j]).control(num_ctrl_qubits=number_of_qubits, ctrl_state=i), qubits_ids )
    

    # Return the final quantum circuit
    return qc



    
if __name__=="__main__": 


    show_plot = False
    
    # data_length = 16
    # data = np.random.randint(low=0, high=3, size=data_length)

    # data = [1, -1, 3, 5, -1, 4, 6, 7]  # Example input data      
    data = [[1, 2, 3], [4 , 5, 6]]



    qc = FRQIEncoding(data)

    # print(qc)


    data = [[159, 53, 139, 89], [120, 247, 40, 220], [173, 60, 89, 32], [181, 59, 13, 94]]   # Example input data
    min_val = 0     # Minimum value
    max_val = 255   # Maximum value
    qc = FRQIEncoding(data, min_val, max_val)
    print(qc)

    if show_plot:
        from qiskit.visualization import circuit_drawer
        import matplotlib.pyplot as plt
        
        # Plot the circuit
        fig = circuit_drawer(qc, output='mpl', style="iqp")
        plt.show()


