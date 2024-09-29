



# Add the parent directory of the current script's directory to the Python path
import sys
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path


# Import Local modules
from Utilities.utils import pad_with_zeros


import numpy as np
from qiskit import QuantumCircuit , QuantumRegister
from qiskit.circuit.library import RYGate


from typing import Any, Union, Optional

from Encodings.qs_AmplitudeEncoding import AmplitudeEncoding


def AmplitudeQRAM(data : Union[list, np.ndarray] , data_dimensionality : int = 1 ) -> QuantumCircuit:
    """
    Encodes the given data into a quantum circuit using ???????????.

    Args:
        data (list): The list of real numbers to be encoded.

    Returns:
        QuantumCircuit: The quantum circuit representing the Amplitude Encoding of the data.

    Example 1 (with 1 qubit):
        >>> data = [2.3, 0.8]  # Example input data      
        >>> qc = AmplitudeEncoding(data)
        >>> print(qc)
           ┌─────────────┐
        q: ┤ Ry(0.66947) ├
           └─────────────┘
           
    Example 2 (with 2 qubit):
        >>> data = [0.5, 0.8, 0.3, 0.6]  # Example input data      
        >>> qc = AmplitudeEncoding(data)
        >>> print(qc)
             ┌────────────┐               ┌────────────┐
        q_0: ┤ Ry(2.2483) ├───────■───────┤ Ry(5.3559) ├
             └────────────┘┌──────┴──────┐└─────┬──────┘
        q_1: ──────────────┤ Ry(-1.3956) ├──────■───────
                           └─────────────┘
    
    Example 3 (with 2 qubit):
        >>> data = [0.5, 0.8, 0.3]  # Example input data  (they will be padded with one zero, equivalent to: [0.5, 0.8, 0.3, 0])
        >>> qc = AmplitudeEncoding(data)
        >>> print(qc)
             ┌────────────┐                ┌───────┐
        q_0: ┤ Ry(2.0827) ├───────■────────┤ Ry(π) ├
             └────────────┘┌──────┴───────┐└───┬───┘
        q_1: ──────────────┤ Ry(-0.71754) ├────■────
                           └──────────────┘

    Example 4 (with 3 qubit):
        >>> data = [0.5, 0.8, 0.3, 0.6, 0.23, 0.16, 0.89, 0.94]  # Example input data      
        >>> qc = AmplitudeEncoding(data)
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
    
    number_of_address_qubits = number_of_qubits - data_dimensionality

    # Indices of data
    qr1 = QuantumRegister(number_of_address_qubits, "a") 
    # Data
    qr2 = QuantumRegister(data_dimensionality, "d")    

    
    
    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(qr1 ,qr2 )

    
    # Create a superposition for all the addresses
    qc.h(range(number_of_address_qubits))



    QCircuit = qc 

    for address_ctrl_state in range(2**number_of_address_qubits) : 

        extra_ctr_qubits = [number_of_qubits-3,number_of_qubits-2]
        print(extra_ctr_qubits)
        number_of_extra_ctr_qubits = len(extra_ctr_qubits) 
        
        extra_ctrl_state  = sum(2 ** i for i in extra_ctr_qubits)
        print(extra_ctrl_state)

        multi_ctr_RYGate =  RYGate(2).control(number_of_address_qubits + number_of_extra_ctr_qubits  ,ctrl_state= extra_ctrl_state + address_ctrl_state)
        print(list(range(0, number_of_address_qubits)) + extra_ctr_qubits +  list([number_of_qubits-1]))
        QCircuit.append(multi_ctr_RYGate, list(range(0, number_of_address_qubits)) + extra_ctr_qubits + list([number_of_qubits-1]) )
     
    # Create an Amplitude Encoding (QPIE) circuit   
    # qc = circuit_maker_amplitude_encoding(qc, alpha, number_of_qubits )

    # Return the final quantum circuit
    return qc 


if __name__ == "__main__" : 
    # data_to_encode = [0, 172, 38, 246, 0, 172, 38, 246] 

    
    data_length = 64
    data_to_encode = np.random.randint(low=0, high=15, size=data_length)

    qc = QuantumRegister(4)
    print(qc)
    
    qc = AmplitudeQRAM(list(data_to_encode), 3)

    print(qc)
    
    