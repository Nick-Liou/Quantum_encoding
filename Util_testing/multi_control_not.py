from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer

import matplotlib.pyplot as plt
# Create a QuantumCircuit instance
qc = QuantumCircuit(3)

# Define a custom gate representing the grouped sequence of gates
grouped_gate = QuantumCircuit(3, name="MyGroup")
grouped_gate.h(0)
grouped_gate.cx(0, 1)
grouped_gate.cx(0, 2)

# Add the custom gate to the circuit
qc.append(grouped_gate.to_instruction(), [0, 1, 2])

# Add individual gates to the circuit
qc.h(1)
qc.cx(1, 2)

# Visualize the circuit with legend
legend = {'MyGroup': 'My Grouped Gates',}
# circuit_drawer(qc, style={'name': legend})
# Plot the circuit
fig = circuit_drawer(qc, style={'name': legend})
# circuit_drawer(qc, output='mpl', style="iqp")
figure = plt.show()
print(qc)