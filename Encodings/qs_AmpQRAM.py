



# Add the parent directory of the current script's directory to the Python path
import sys
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path


# Import Local modules
from Utilities.utils import pad_with_zeros


import numpy as np
from qiskit import QuantumCircuit , QuantumRegister


from typing import Any, Union, Optional

from Encodings.qs_AmplitudeEncoding import circuit_maker_amplitude_encoding, solve_spherical_angles, AmplitudeEncoding


def AmplitudeQRAM(data : Union[list, np.ndarray] , number_of_address_qubits : int = 0 ) -> QuantumCircuit:
    """
    Encodes the given data into a quantum circuit using QRAM Amplitude Encoding.

    Args:
        data (list): The list of real numbers to be encoded.
        number_of_address_qubits (int, optional): The number of qubits to use for the address quantum register

    Returns:
        QuantumCircuit: The quantum circuit representing the QRAM Amplitude Encoding of the data.

    Examples:
    Example 1 (with 1 qubit):
        >>> data = [2.3, 0.8]  # Example input data      
        >>> qc = AmplitudeQRAM(data)
        >>> print(qc)
           ┌─────────────┐
        q: ┤ Ry(0.66947) ├
           └─────────────┘
           
    Example 2 (with 2 qubit):
        >>> data = [0.5, 0.8, 0.3, 0.6]  # Example input data      
        >>> qc = AmplitudeQRAM(data)
        >>> print(qc)
             ┌────────────┐               ┌────────────┐
        q_0: ┤ Ry(2.2483) ├───────■───────┤ Ry(5.3559) ├
             └────────────┘┌──────┴──────┐└─────┬──────┘
        q_1: ──────────────┤ Ry(-1.3956) ├──────■───────
                           └─────────────┘
    
    Example 3 (with 2 qubit):
        >>> data = [0.5, 0.8, 0.3]  # Example input data  (they will be padded with one zero, equivalent to: [0.5, 0.8, 0.3, 0])
        >>> qc = AmplitudeQRAM(data)
        >>> print(qc)
             ┌────────────┐                ┌───────┐
        q_0: ┤ Ry(2.0827) ├───────■────────┤ Ry(π) ├
             └────────────┘┌──────┴───────┐└───┬───┘
        q_1: ──────────────┤ Ry(-0.71754) ├────■────
                           └──────────────┘

    Example 4 (with 3 qubit):
        >>> data = [0.5, 0.8, 0.3, 0.6, 0.23, 0.16, 0.89, 0.94]  # Example input data      
        >>> qc = AmplitudeQRAM(data)
        >>> print(qc)
             ┌────────────┐               ┌────────────┐              ┌───┐     ┌────────────┐               ┌───────────┐
        q_0: ┤ Ry(2.5652) ├───────■───────┤ Ry(5.8762) ├──────■───────┤ X ├─────┤ Ry(2.7925) ├───────■───────┤ Ry(4.767) ├
             └────────────┘┌──────┴──────┐└─────┬──────┘      │       └─┬─┘┌───┐└─────┬──────┘┌──────┴──────┐└─────┬─────┘
        q_1: ──────────────┤ Ry(-2.1531) ├──────■─────────────■─────────┼──┤ X ├──────┼───────┤ Ry(-2.8956) ├──────■──────
                           └─────────────┘              ┌─────┴──────┐  │  └─┬─┘      │       └──────┬──────┘      │
        q_2: ───────────────────────────────────────────┤ Ry(2.2909) ├──■────■────────■──────────────■─────────────■──────
                                                        └────────────┘

    """
        
    # pad with zeros if needed
    padded_data = pad_with_zeros(np.array(data))
    
    number_of_qubits = int ( np.ceil(np.log2(len(padded_data))) )

    if ( number_of_address_qubits >= number_of_qubits or number_of_address_qubits < 0):
        raise ValueError("Input number_of_address_qubits must be less than the total qubits requaried to encode the data")
    elif ( number_of_address_qubits == 0 ):
        return AmplitudeEncoding(padded_data)
        
    data_dimensionality = number_of_qubits - number_of_address_qubits

    # Indices of data
    qr1 = QuantumRegister(number_of_address_qubits, "a") 
    # Data
    qr2 = QuantumRegister(data_dimensionality, "d")    

    
    
    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(qr1 ,qr2 )

    
    # Create a superposition for all the addresses
    qc.h(range(number_of_address_qubits))


    for i in range(2**number_of_address_qubits) : 

        qc.barrier()
        
        # Find the 
        address_data = padded_data[i*2**data_dimensionality:(i+1)*2**data_dimensionality]

        # Normalize data 
        desired_real_statevector = address_data / np.sqrt(sum(np.abs(address_data)**2))  

        # Find the angles "alpha"
        alpha = solve_spherical_angles(desired_real_statevector)
        
        extra_ctr_qubits =  list(range(number_of_address_qubits))
        # Create a controlled Amplitude Encoding (QPIE) circuit   
        qc = circuit_maker_amplitude_encoding(qc, alpha, data_dimensionality ,extra_ctr_qubits , i ,number_of_address_qubits  )
     

    # Return the final quantum circuit
    return qc 


if __name__ == "__main__" : 
    
    show_plot = True
    # data_to_encode = [0, 172, 38, 246, 0, 172, 38, 246] 
    
    data_length = 32
    data_to_encode = np.random.randint(low=0, high=15, size=data_length)
    
    qc = AmplitudeQRAM(list(data_to_encode), 4)

    # Print quantum circuit to the console 
    print(qc)


    if show_plot:
        from qiskit.visualization import circuit_drawer
        import matplotlib.pyplot as plt
        
        # Plot the circuit
        fig = circuit_drawer(qc, output='mpl', style="iqp")
        plt.show()
        
    
    