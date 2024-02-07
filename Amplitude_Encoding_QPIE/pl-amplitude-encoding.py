# import the template
import pennylane as qml
from pennylane.templates.embeddings import AmplitudeEmbedding
import numpy as np 
import math
import matplotlib.pyplot as plt

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
        number_of_zeros = 2 ** math.ceil( math.log(len(data),2) ) -  len(arr)

    # Create an array of zeros with the desired length
    zeros_array = np.zeros(number_of_zeros, dtype=arr.dtype)
    
    # Concatenate the original array with the zeros array
    padded_arr = np.concatenate((arr, zeros_array))
    
    return padded_arr



# Define your custom gate as a unitary matrix
custom_gate_matrix = np.array([[1, 0, 0, 0],
                                [0, 1, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, np.exp(1j * np.pi / 4)]])





# Define data to embedd into qubits
# data = np.array([2,3,3,2])
data = np.array([6,-12.5,11.15,7])
Qubits = math.ceil( math.log(len(data),2) ) 
data = pad_with_zeros(data)     # If necessary

print(f"Number of qubits used: {Qubits}")
print("Original data:")
print(data)



# The quantum device to run and how many Qubits to use
dev = qml.device('default.qubit', wires=Qubits)


@qml.qnode(dev)
def circuit_test(data,num_qubits):
    # Apply your custom gate to a set of qubits
    qml.QubitUnitary(custom_gate_matrix, wires=range(num_qubits))
    return qml.state()
    

@qml.qnode(dev)
def circuit(data):
    AmplitudeEmbedding(features=data, wires=range(Qubits),normalize=True)
    return qml.state()

# Print the circuit diagram
print(qml.draw(circuit, expansion_strategy="device", show_all_wires=True)(data))


# # Print the quantum gates used in the circuit
# print("Quantum Gates Used:")
# for gate in circuit.qtape.operations:
#     print(gate.name)


    
fig, ax = qml.draw_mpl(circuit,show_all_wires=True)(data)
# fig.show()

# Show the diagram and wait for user to close the window
plt.show()

print("\nQuantum register state:")
print(circuit(data))


print("\nExpected quantum register state:")
print(data / np.sqrt(sum(np.abs(data)**2)) + 0j ) 


# # Expected output for data = np.array([6,-12.5,11.15,7])
#  0: ──╭QubitStateVector(M0)──╭┤ State 
#  1: ──╰QubitStateVector(M0)──╰┤ State 
# M0 = [ 0.31380835+0.j -0.65376739+0.j  0.58316051+0.j  0.36610974+0.j]