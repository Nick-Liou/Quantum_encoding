
# Add the parent directory of the current script's directory to the Python path
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path

from Amplitude_Encoding_QPIE.qs_AmplitudeEncoding   import custom_amplitude_encoding

from qiskit.circuit import QuantumCircuit, Parameter, ParameterVector
from qiskit.visualization import circuit_drawer 
import matplotlib.pyplot as plt



number_of_qubits = 3
alpha = ParameterVector("a", 2**number_of_qubits-1 )
qc = QuantumCircuit(number_of_qubits)

qc = custom_amplitude_encoding(qc, alpha, number_of_qubits )
print(qc)

fig = circuit_drawer(qc, output='mpl', style="iqp" ,fold=-1)
figure = plt.show()