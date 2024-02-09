from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from math import pi

# Define the angle of rotation in radians
theta = pi/2 + pi  

# Create a quantum circuit with one qubit
qc = QuantumCircuit(1)

# Apply the Ry gate with the specified angle
qc.ry(theta, 0)

# Draw the circuit
print(qc.draw())

# Transpile the circuit for the backend
transpiled_circuit = transpile(qc, Aer.get_backend('qasm_simulator'))

# Simulate the transpiled circuit
backend = Aer.get_backend('statevector_simulator')
job = backend.run(transpiled_circuit)
result = job.result()

# Get the final state vector
state_vector = result.get_statevector()
print("Final state vector:", state_vector)


