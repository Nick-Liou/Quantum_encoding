from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt
import numpy as np

from qiskit.circuit.library import RYGate
from qiskit.circuit.library import XGate
from math import pi

# To import my custom funcitons
# from Amplitude_Encoding_QPIE.qs_AmplitudeEncoding import custom_amplitude_encoding

from qs_AmplitudeEncoding import custom_amplitude_encoding
from qs_AmplitudeEncoding import solve_spherical_angles



if __name__ == "__main__" : 


    number_of_qubits =  3
    show_plot = True

    # Generate random numbers
    c = np.random.rand(2**number_of_qubits)-0.5
    # c = np.array([1,2,0,4,0,6,0,0])

    # Convert it into a statevector (normalize)
    c = c / np.sqrt(sum(np.abs(c)**2))      
    # Find the angles "alpha"
    alpha = solve_spherical_angles(c)
    # print("c = " , c)
    # print("Spherical angles:", alpha)


    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(number_of_qubits)

    
    # Create an Amplitude Encoding (QPIE) circuit   
    qc = custom_amplitude_encoding(qc, alpha, number_of_qubits )

    

    
    if show_plot:
        # Print the circuit in the console
        print(qc.draw())

        # Plot the circuit
        fig = circuit_drawer(qc, output='mpl', style="iqp")
        plt.show()
   
    
    # Transpile the circuit for the backend
    transpiled_circuit = transpile(qc, Aer.get_backend('qasm_simulator'))

    # Simulate the transpiled circuit
    backend = Aer.get_backend('statevector_simulator')
    job = backend.run(transpiled_circuit)
    result = job.result()

    # Get the final state vector (from the result)
    state_vector = result.get_statevector()
    # print("\n\nFinal state vector:    ", state_vector.data)    

    # Define a tolerance for comparison, adjust as needed
    tolerance = 1e-6  

    # Check if the actual and expected values are equal within the tolerance
    if np.allclose(state_vector.data,  c + 0j , atol=tolerance):
        print(f"The actual values match the expected values within the tolerance ({tolerance}).")
    else:        
        print("Final state vector:    ", state_vector.data)    
        print("Expected state vector: " , c + 0j )
        print(f"The actual values do NOT match the expected values within the tolerance ({tolerance}).")
    

    



