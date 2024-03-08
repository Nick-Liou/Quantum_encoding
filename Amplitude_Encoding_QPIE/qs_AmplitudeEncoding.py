import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RYGate
from qiskit.circuit.library import XGate
from math import pi


# Typing stuff
from typing import Union

# Add the parent directory of the current script's directory to the Python path
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path

# Import Local modules
from Utilities.utils import pad_with_zeros

def AmplitudeEncoding(data : Union[list, np.ndarray]  ) -> QuantumCircuit:
    """
    Encodes the given data into a quantum circuit using Amplitude Encoding (QPIE).

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
    
    # Normalize data 
    desired_real_statevector = padded_data / np.sqrt(sum(np.abs(padded_data)**2))  

    # Find the angles "alpha"
    alpha = solve_spherical_angles(desired_real_statevector)


    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(number_of_qubits)

     
    # Create an Amplitude Encoding (QPIE) circuit   
    qc = custom_amplitude_encoding(qc, alpha, number_of_qubits )

    # Return the final quantum circuit
    return qc 


def custom_amplitude_encoding(QCircuit:QuantumCircuit, alpha:Union[list, np.ndarray] , n : int ,  control_qubits:list = list() ) -> QuantumCircuit:
    """
    Encodes amplitudes onto a quantum circuit using a custom amplitude encoding scheme.

    Args:
        QCircuit (QuantumCircuit): The quantum circuit to which the encoding is applied.
        alpha (array-like): An array of angles for encoding.
        n (int): The number of qubits in the circuit.
        control_qubits (list, optional): List of control qubits. Defaults to an empty list.

    Returns:
        QuantumCircuit: The modified quantum circuit after applying the custom amplitude encoding.
    """
    if n == 1 : 
        QCircuit.ry(alpha[0], 0)
    elif n == 2 : 
        # Remove duplicates from the list of control qubits
        control_qubits = list(set(control_qubits))    

        number_of_extra_ctr_qubits = len(control_qubits)

        if number_of_extra_ctr_qubits == 0 : 
            QCircuit.ry(alpha[0], 0)
            QCircuit.cry(-alpha[1], 0, 1)
            QCircuit.cry(pi + alpha[2], 1, 0)
        else:             
            
            # Apply controlled RY gates
            
            # Gate 1
            multi_ctr_RYGate =  RYGate(alpha[0]).control(number_of_extra_ctr_qubits,label=None)
            QCircuit.append(multi_ctr_RYGate, control_qubits + [0] )
            
            # Gate 2
            multi_ctr_RYGate =  RYGate(-alpha[1]).control(number_of_extra_ctr_qubits+1,label=None)
            QCircuit.append(multi_ctr_RYGate, control_qubits + [0] + [1] )

            # Gate 3
            multi_ctr_RYGate =  RYGate(pi + alpha[2]).control(number_of_extra_ctr_qubits+1,label=None)
            QCircuit.append(multi_ctr_RYGate, control_qubits + [1] + [0] )
            
            ## Template 
            ## multi_ctr_RYGate =  RYGate(theta).control(number_of_ctr_qubits,label=None)
            ## QCircuit.append(multi_ctr_RYGate, control_qubits + [target_qubit] )            

    else : 
        # Remove duplicates from the list of control qubits
        control_qubits = list(set(control_qubits))
        
        # Step b
        # Design an (n-1)-qubit arbitrary statevector
        # generator circuit, recursively, employing the first (n-1) qubits on the
        # system.

        QCircuit = custom_amplitude_encoding(QCircuit, alpha , n - 1 , control_qubits)


        # Step c
        # Apply  an (n-1)-qubit controlled 𝑅𝑦 (alpha[2**(n-1)-1]) gate, with control on first (n-1)
        # qubits and target on last qubit.
        
        # multi_ctr_RYGate =  RYGate(alpha[n]).control(n-1 + len(control_qubits),label=None)
        multi_ctr_RYGate =  RYGate(alpha[2**(n-1)-1]).control(n-1 + len(control_qubits),label=None)
        QCircuit.append(multi_ctr_RYGate, list(range(0, n-1)) + control_qubits + [n-1] )


        # Step d 
        # Apply (n-1) CNOT gates, one by one, on each of the first (n-1) qubits.
        # Each of these CNOT gates has control on the last qubit.

        multi_ctr_XGate =  XGate().control(1 + len(control_qubits),label=None)
        for i in range(n-1):
            QCircuit.append(multi_ctr_XGate, [n-1] + control_qubits + [i] )
        

        # Step e            
        # Apply another (n-1)-qubit arbitrary statevector generator circuit with the last
        # (2**𝑛−1 − 1) angles, recursively, on first (n-1) qubits. Each gate in this subcircuit
        # must have additional control from last qubit.
            
        control_qubits.append(n-1)
        QCircuit = custom_amplitude_encoding(QCircuit, alpha[2**(n-1):] , n - 1 , control_qubits)

    return QCircuit


def solve_spherical_angles(c: np.ndarray) -> np.ndarray:
    """
    Solve the system of equations to find the spherical angles corresponding to the given coefficients.

    Given a set of coefficients `c`, this function solves a system of equations of the form:
    c[0]    = cos(a[0]/2)
    c[1]    = sin(a[0]/2) * cos(a[1]/2)
    c[2]    = sin(a[0]/2) * sin(a[1]/2) * cos(a[2]/2)
    ...
    c[n-1]  = sin(a[0]/2) * sin(a[1]/2) * ... * sin(a[n-2]/2) * cos(a[n-1]/2)
    c[n]    = sin(a[0]/2) * sin(a[1]/2) * ... * sin(a[n-2]/2) * sin(a[n-1]/2)

    Args:
        c (array-like): Coefficients representing a spherical function.

    Returns:
        array-like: Spherical angles corresponding to the coefficients with length: len(c)-1.
    """
     
    n = len(c) - 1
    alpha = np.zeros(n) # Initialize array for spherical angles


    alpha[0] = 2 * np.arccos(abs(c[0]))     # Calculate alpha for the first coefficient
    sin_prod = np.sin(alpha[0] / 2)         # Initialize sin product

    # Solve the system for possitive c 
    for i in range(1, n):
        if sin_prod == 0 : 
            # Leave alpha as zeros (they can have any value) if sin_prod is zero
            break
            alpha[i] = pi 
        else:
            alpha[i] = 2 * np.arccos(min(abs(c[i]) / sin_prod , 1))
            sin_prod *= np.sin(alpha[i] / 2)

    # Adjust the solution for the signs of c
    for i in range(n):
        if c[i] < 0 :
            alpha[i] = 2*pi - alpha[i]

    if c[-1] < 0 :
        alpha[-1] = - alpha[-1]

    return alpha






# Example usage:
if __name__ == "__main__" : 
   
    from qiskit import transpile
    from qiskit_aer import Aer

    # Define a tolerance for comparison, adjust as needed
    tolerance = 1e-6
    show_plot = True

    data_length = 30

    data_to_encode = np.random.rand(data_length)-0.5


    # pad with zeros if needed
    padded_data = pad_with_zeros(data_to_encode)   
    
    # Normalize data 
    expected_statevector = padded_data / np.sqrt(sum(np.abs(padded_data)**2))  + 0j



    # Apply the custom encoding function
    qc = AmplitudeEncoding(list(data_to_encode))

    # Transpile the circuit for the backend
    transpiled_circuit = transpile(qc, Aer.get_backend('qasm_simulator'))

    # Simulate the transpiled circuit
    backend = Aer.get_backend('statevector_simulator')
    job = backend.run(transpiled_circuit)
    result = job.result()

    state_vector = result.get_statevector().data

    
    # Print the circuit in the console
    print(qc)

    print("\n\nFinal state vector: ", state_vector)    

    # Check if the actual and expected values are equal within the tolerance
    if np.allclose(state_vector,  expected_statevector , atol=tolerance):
        print(f"The actual values match the expected values within the tolerance ({tolerance}).")
    else:        
        print("Final state vector:    ", state_vector)    
        print("Expected state vector: " , expected_statevector )
        print(f"The actual values do NOT match the expected values within the tolerance ({tolerance}).")
    

    if show_plot:
        from qiskit.visualization import circuit_drawer
        import matplotlib.pyplot as plt
        
        # Plot the circuit
        fig = circuit_drawer(qc, output='mpl', style="iqp")
        plt.show()
        


   