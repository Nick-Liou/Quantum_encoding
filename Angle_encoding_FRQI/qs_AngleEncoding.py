import numpy as np
from qiskit import QuantumCircuit


def AngleEncoding(data , min_val = None , max_val = None ):

    number_of_qubits = len(data)


    data = np.array(data)

    # Calculate min_val if it is None, otherwise use the provided value
    min_val = np.min(data) if min_val is None else min_val
    # Calculate max_val if it is None, otherwise use the provided value
    max_val = np.max(data) if max_val is None else max_val

    # Normalize to the range [0, pi/2]
    theta = (data - min_val) * (np.pi / 2) / (max_val - min_val)

    
    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(number_of_qubits)


    for i in range(number_of_qubits):
        qc.ry(2 * theta[i] , i)


    # Return the final quantum circuit
    return qc 



# Example usage:
if __name__ == "__main__" : 

    pass