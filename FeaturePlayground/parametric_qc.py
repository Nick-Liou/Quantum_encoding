
# Add the parent directory of the current script's directory to the Python path
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path

from Amplitude_Encoding_QPIE.qs_AmplitudeEncoding   import custom_amplitude_encoding

from qiskit.circuit import QuantumCircuit, Parameter, ParameterVector
from qiskit.visualization import circuit_drawer 
import matplotlib.pyplot as plt


# Amplitude enc

def amp_param (number_of_qubits : int = 3) -> QuantumCircuit :  
    alpha = ParameterVector("a", 2**number_of_qubits-1 )
    print("alpha: ",alpha)
    qc = QuantumCircuit(number_of_qubits)
    qc = custom_amplitude_encoding(qc, alpha, number_of_qubits )
    return qc



# Angle enc
def angle_param (number_of_qubits : int = 3) -> QuantumCircuit: 

    theta = ParameterVector("θ", number_of_qubits)
    qc = QuantumCircuit(number_of_qubits)
    for i in range(number_of_qubits):
            qc.ry(2 * theta[i] , i)

    return qc



qc = amp_param(number_of_qubits=4)
print(qc)

# fig = circuit_drawer(qc, output='mpl', style="iqp" ,fold=None)
# figure = plt.show()