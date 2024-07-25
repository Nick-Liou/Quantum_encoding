from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.circuit.library import RYGate

def custom_amplitude_encoding(qc : QuantumCircuit, alpha:ParameterVector, number_of_qubits:int) -> QuantumCircuit:
    n = number_of_qubits
    
    for i in range(1):
        param = alpha[i]
        print(f"Attempting to create controlled RYGate with param: {param} for qubits: {n}")
        
        try:
            multi_ctr_RYGate = RYGate(param).control(n-1)
            qc.append(multi_ctr_RYGate, range(n))
            print(f"Successfully created controlled RYGate with param: {param}")
        except Exception as e:
            print(f"Failed to create controlled RYGate with param: {param}: {e}")
            
    return qc

def amp_param(number_of_qubits:int) -> QuantumCircuit:
    alpha = ParameterVector('a', length=1)
    qc = QuantumCircuit(number_of_qubits)
    qc = custom_amplitude_encoding(qc, alpha, number_of_qubits)
    return qc

# https://github.com/Qiskit/qiskit/issues/9187
# Example usage
number_of_qubits = 2
qc = amp_param(number_of_qubits)
print(qc)


# from qiskit.visualization import circuit_drawer 
# import matplotlib.pyplot as plt
# fig = circuit_drawer(qc, output='mpl', style="iqp")
# figure = plt.show()