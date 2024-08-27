
# Add the parent directory of the current script's directory to the Python path
import sys
import os

from qiskit import QuantumRegister

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path

from Encodings.qs_AmplitudeEncoding   import circuit_maker_amplitude_encoding

from qiskit.circuit import QuantumCircuit, Parameter, ParameterVector
from qiskit.visualization import circuit_drawer 
import matplotlib.pyplot as plt


from qiskit.circuit.library import RYGate
# Amplitude enc

def amp_param (number_of_qubits : int = 3) -> QuantumCircuit :  
    alpha = ParameterVector("a", 2**number_of_qubits-1 )
    print("alpha: ",alpha)
    qc = QuantumCircuit(number_of_qubits)
    qc = circuit_maker_amplitude_encoding(qc, alpha, number_of_qubits )
    return qc



# Angle enc
def angle_param (number_of_qubits : int = 3) -> QuantumCircuit: 

    theta = ParameterVector("θ", number_of_qubits)
    qc = QuantumCircuit(number_of_qubits)
    for i in range(number_of_qubits):
            qc.ry(2 * theta[i] , i)

    return qc


# FRQI enc
def FRQI_param (number_of_qubits : int = 3 , dim : int = 1 ) -> QuantumCircuit: 

    if dim == 1 : 
        theta = ParameterVector("θ", 2**number_of_qubits)
    else:   
        theta = []
        for j in range(dim-1,-1,-1):
            theta.append(ParameterVector(f"θ_{j}", 2**number_of_qubits))

    print(theta)
    
    # Indices of data
    qr1 = QuantumRegister(number_of_qubits, "a") 
    # Data
    qr2 = QuantumRegister(dim, "d")        
    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(qr1 ,qr2 )

    
    qc.h(range(number_of_qubits))


    for i in range(2**number_of_qubits):
        qc.barrier()
        if dim == 1 : 
            qc.append(RYGate(2*theta[i]).control(num_ctrl_qubits=number_of_qubits, ctrl_state=i), list(range(number_of_qubits+1)) )
        else:
            for j in range(dim):
                apply_gate_to = qubits_ids = list(range(number_of_qubits)) + [number_of_qubits + dim - j - 1]
                qc.append(RYGate(2*theta[j][i]).control(num_ctrl_qubits=number_of_qubits, ctrl_state=i), apply_gate_to )
    qc.barrier()
            

    return qc


# Theoretical examples
def theoretical_intro (number_of_qubits : int = 1) -> QuantumCircuit: 

    # NOT and H gates
    qc = QuantumCircuit(1)
    # qc.h(0)
    qc.x(0)

    qc = QuantumCircuit(1)
    theta = Parameter("φ")
    qc.ry(theta, 0)
    
    # Bell State and Example
    # qc = QuantumCircuit(2)    
    # qc.h(0)
    # qc.cx(0,1)
    # qc.x(0)

    return qc



if __name__ == "__main__" : 
    qc = theoretical_intro(number_of_qubits=3)
    print(qc)

    fig = circuit_drawer(qc, output='mpl', style="iqp" ,fold=None)
    figure = plt.show()



    from qiskit import transpile  
    from qiskit.visualization import circuit_drawer 
    from qiskit_aer import Aer 
    import numpy as np

    from qiskit.result.result import Result
    from qiskit_aer.jobs.aerjob import AerJob
    from qiskit_aer.backends.statevector_simulator import StatevectorSimulator

    # Transpile the circuit for the backend
    transpiled_circuit = transpile(qc, Aer.get_backend('qasm_simulator'))

    # Simulate the transpiled circuit
    backend : StatevectorSimulator = Aer.get_backend('statevector_simulator')
    #  AerSimulator(method="statevector")
    job : AerJob = backend.run(transpiled_circuit)
    result : Result = job.result()    

    state_vector = result.get_statevector().data


    print("\n\nFinal state vector: ", state_vector)  
    print("\n\nFinal real state vector: ", state_vector.real)    
    print("Indices of non-zero elements in the statevector:", np.nonzero(state_vector))
