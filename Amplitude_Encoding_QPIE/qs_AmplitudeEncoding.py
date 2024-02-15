import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import RYGate
from qiskit.circuit.library import XGate
from math import pi

# # To import my custom funciton to solve a system of equations
# from qiskit_amp_ecnode_util import solve_spherical_angles

def AmplitudeEncoding(data):

    padded_data = pad_with_zeros(data) 
    
    number_of_qubits = int ( np.ceil(np.log2(len(padded_data))) )
    
    # Normalize data 
    norm_data = padded_data / np.sqrt(sum(np.abs(padded_data)**2))  

    # Find the angles "alpha"
    alpha = solve_spherical_angles(norm_data)

    print(alpha)


    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(number_of_qubits)

     
    # Create an Amplitude Encoding (QPIE) circuit   
    qc = custom_amplitude_encoding(qc, alpha, number_of_qubits )

    # Return the final quantum circuit
    return qc 



def custom_amplitude_encoding(QCircuit:QuantumCircuit, alpha , n ,  control_qubits:list = list() ):

    if n == 1 : 
        QCircuit.ry(alpha[0], 0)
    elif n == 2 : 
       
        # Remove duplicates 
        control_qubits = list(set(control_qubits))    

        number_of_extra_ctr_qubits = len(control_qubits)

        if number_of_extra_ctr_qubits == 0 : 
            QCircuit.ry(alpha[0], 0)
            QCircuit.cry(-alpha[1], 0, 1)
            QCircuit.cry(pi + alpha[2], 1, 0)
        else:             
            
            # Template 
            # multi_ctr_RYGate =  RYGate(theta).control(number_of_ctr_qubits,label=None)
            # QCircuit.append(multi_ctr_RYGate, control_qubits + [target_qubit] )            
            
            # Gate 1
            multi_ctr_RYGate =  RYGate(alpha[0]).control(number_of_extra_ctr_qubits,label=None)
            QCircuit.append(multi_ctr_RYGate, control_qubits + [0] )
            
            # Gate 2
            multi_ctr_RYGate =  RYGate(-alpha[1]).control(number_of_extra_ctr_qubits+1,label=None)
            QCircuit.append(multi_ctr_RYGate, control_qubits + [0] + [1] )

            # Gate 3
            multi_ctr_RYGate =  RYGate(pi + alpha[2]).control(number_of_extra_ctr_qubits+1,label=None)
            QCircuit.append(multi_ctr_RYGate, control_qubits + [1] + [0] )

    else : 
        # Remove duplicates 
        control_qubits = list(set(control_qubits))
        
        # Step b
        # Design an (n-1)-qubit arbitrary statevector
        # generator circuit, recursively, employing the first (n-1) qubits on the
        # system.

        QCircuit = custom_amplitude_encoding(QCircuit, alpha , n - 1 , control_qubits)

        # Step c
        # Employ an (n-1)-qubit controlled 𝑅𝑦 (alpha[2**(n-1)-1]) gate, with control on first (n-1)
        # qubits and target on last qubit.

        
        # multi_ctr_RYGate =  RYGate(alpha[n]).control(n-1 + len(control_qubits),label=None)
        multi_ctr_RYGate =  RYGate(alpha[2**(n-1)-1]).control(n-1 + len(control_qubits),label=None)
        QCircuit.append(multi_ctr_RYGate, list(range(0, n-1)) + control_qubits + [n-1] )

        # Step d 
        # Employ (n-1) CNOT gates, one by one, on each of the first (n-1) qubits.
        # Each of these CNOT gates has control on the last qubit.

        multi_ctr_XGate =  XGate().control(1 + len(control_qubits),label=None)
        for i in range(n-1):
            QCircuit.append(multi_ctr_XGate, [n-1] + control_qubits + [i] )
        
        # Step e
            
        # Employ another (n-1)-qubit arbitrary statevector generator circuit with the last
        # (2**𝑛−1 − 1) angles, recursively, on first (n-1) qubits. Each gate in this subcircuit
        # must have additional control from last qubit.
            
        control_qubits.append(n-1)
        QCircuit = custom_amplitude_encoding(QCircuit, alpha[2**(n-1):] , n - 1 , control_qubits)

    return QCircuit


def solve_spherical_angles(c):
    
    n = len(c) - 1
    alpha = np.zeros(n)

    alpha[0] = 2 * np.arccos(abs(c[0]))
    sin_prod = np.sin(alpha[0] / 2)

    # Solve the system for possitive c 
    for i in range(1, n):
        if sin_prod == 0 : 
            break
            # Leave alpha as zeros (they can have any value)
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