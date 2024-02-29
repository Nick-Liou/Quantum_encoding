# import the template
import pennylane as qml
from pennylane.templates.embeddings import AmplitudeEmbedding
import numpy as np 
import math
import matplotlib.pyplot as plt

# To import my custom funcitons
import Util_testing.Direct_sum_util as Direct_sum_util
from typing import Any, Optional, Union
from pennylane.measurements import StateMP

def pad_with_zeros(arr: np.ndarray, number_of_zeros: Optional[int] = None) -> np.ndarray:
    """
    Pad an np.array with a specified number of zeros at the end.

    Parameters:
        arr (numpy.ndarray): Input array.
        number_of_zeros (int, optional): Number of zeros to add at the end of the array.
            If not provided, the number of zeros will be calculated based on the next power of 2.
    
    Returns:
        numpy.ndarray: Padded array.
    """
    if number_of_zeros is None:
        number_of_zeros = int(2 ** np.ceil(np.log2(len(arr))) - len(arr))
    
    return np.pad(arr, (0, number_of_zeros), mode='constant')





# Define data to embedd into qubits
# data = np.array([2,3])
# data = np.array([2,3,3,2])
data = np.array([1,2,3,4,5,6,7,8])
# data = np.array([6,12.5,11.15,7])
Qubits = math.ceil( math.log(len(data),2) ) 
data = pad_with_zeros(data)     # If necessary

print(f"Number of qubits used: {Qubits}")
print("Original data:",data)



# The quantum device to run and how many Qubits to use
dev = qml.device('default.qubit', wires=Qubits)


@qml.qnode(dev)
def circuit_mine(data: Union[list, np.ndarray],num_qubits:int) -> StateMP: # "Non working (it does something else)"

    for qubit_id in range(num_qubits):
        p = Direct_sum_util.generate_p (data, qubit_id )

        custom_gate_matrix = Direct_sum_util.custom_matrix_generator(p)
        
        # Apply your custom gate to a set of qubits
        qml.QubitUnitary(custom_gate_matrix, wires=range(qubit_id+1))


    return qml.state()
    

@qml.qnode(dev)
def circuit(data: Union[list, np.ndarray]) -> StateMP:
    AmplitudeEmbedding(features=data, wires=range(Qubits),normalize=True)
    return qml.state()

# Print the circuit diagram
print(qml.draw(circuit, expansion_strategy="device", show_all_wires=True)(data))
# print(qml.draw(circuit_mine, expansion_strategy="device", show_all_wires=True)(data,Qubits))


# # Print the quantum gates used in the circuit
# print("Quantum Gates Used:")
# for gate in circuit.qtape.operations:
#     print(gate.name)


    
# fig, ax = qml.draw_mpl(circuit,show_all_wires=True)(data)
# # fig.show()
# # Show the diagram and wait for user to close the window
# plt.show()


# fig, ax = qml.draw_mpl(circuit_mine,show_all_wires=True)(data,Qubits)
# # fig.show()
# # Show the diagram and wait for user to close the window
# plt.show()

print("\nQuantum register state:")
Qreg = circuit(data) 
print(Qreg)

# print("\nQuantum register state mine:")
# Qreg_mine = circuit_mine(data,Qubits)
# print(Qreg_mine)
# print(sum(np.abs(Qreg_mine)**2))

print("\nExpected quantum register state:")
Qreg_expected = data / np.sqrt(sum(np.abs(data)**2)) + 0j 
print(Qreg_expected) 


# Define a tolerance for comparison, adjust as needed
tolerance = 1e-6  

# Check if the actual and expected values are equal within the tolerance
if np.allclose(Qreg,  Qreg_expected , atol=tolerance):
    print(f"The actual values match the expected values within the tolerance ({tolerance}).")
else:        
    print("Final state vector:    ", Qreg)    
    print("Expected state vector: " , Qreg_expected )
    print(f"The actual values do NOT match the expected values within the tolerance ({tolerance}).")
    

print()
# # Expected output for data = np.array([6,-12.5,11.15,7])
#  0: ──╭QubitStateVector(M0)──╭┤ State 
#  1: ──╰QubitStateVector(M0)──╰┤ State 
# M0 = [ 0.31380835+0.j -0.65376739+0.j  0.58316051+0.j  0.36610974+0.j]