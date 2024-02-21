from qiskit import QuantumCircuit, QuantumRegister
from qiskit.visualization import circuit_drawer

from qiskit.circuit.library import MCXGate

import matplotlib.pyplot as plt

number_of_qubits = 6
bit_depth = 2

# Indices of data
qr1 = QuantumRegister(number_of_qubits, "q") 
# Data
qr2 = QuantumRegister(bit_depth, "a")    

# Create a quantum circuit with multipule qubits
qc = QuantumCircuit(qr1 ,qr2 )

pos_ctrl_qubits_ids = [5,3,1]
neg_ctrl_qubits_ids = [2,0]
target_qubit = 0 + number_of_qubits
kkk =  list(pos_ctrl_qubits_ids) + list(neg_ctrl_qubits_ids) + [target_qubit]
qc.append(MCXGate(num_ctrl_qubits=len(kkk)-1, ctrl_state= 2**(len(pos_ctrl_qubits_ids))-1 ), kkk )
    

print(qc)

# fig = circuit_drawer(qc, output='mpl', style="iqp")            
# figure = plt.show()