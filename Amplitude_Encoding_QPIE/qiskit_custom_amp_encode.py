from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np
from math import pi
from qiskit.circuit.library import RYGate
from qiskit.circuit.library import XGate
import matplotlib.pyplot as plt
from qiskit.visualization import circuit_drawer

# To import my custom funcitons
from qiskit_amp_ecnode_util import solve_spherical_angles


def custom_amplitude_encoding(QCircuit:QuantumCircuit, alpha , n ,  control_qubits:list = list() ):

    if n == 1 : 
        QCircuit.ry(alpha[0], 0)
    elif n == 2 : 
       
        # print(type(control_qubits))
        # print(control_qubits) 
        control_qubits = list(set(control_qubits))            
        # print(control_qubits) 

        number_of_extra_ctr_qubits = len(control_qubits)

        if number_of_extra_ctr_qubits == 0 : 
            QCircuit.ry(alpha[0], 0)
            QCircuit.cry(-alpha[1], 0, 1)
            QCircuit.cry(pi + alpha[2], 1, 0)
        else:             
            
            # Template 
            # multi_ctr_RYGate =  RYGate(theta).control(number_of_ctr_qubits,label=None)
            # QCircuit.append(multi_ctr_RYGate, control_qubits + [target_qubit] )

            
            
            # Gate 1
            multi_ctr_RYGate =  RYGate(alpha[0]).control(number_of_extra_ctr_qubits,label=None)
            QCircuit.append(multi_ctr_RYGate, control_qubits + [0] )
            
            # Gate 2
            multi_ctr_RYGate =  RYGate(-alpha[1]).control(number_of_extra_ctr_qubits+1,label=None)
            QCircuit.append(multi_ctr_RYGate, control_qubits + [0] + [1] )

            # Gate 3
            multi_ctr_RYGate =  RYGate(pi + alpha[2]).control(number_of_extra_ctr_qubits+1,label=None)
            QCircuit.append(multi_ctr_RYGate, control_qubits + [1] + [0] )


      
        # if with_extra_control :
        #     pass
        # else : 
        #     QCircuit.ry(alpha[0], 0)
        #     QCircuit.cry(-alpha[1], 0, 1)
        #     QCircuit.cry(pi + alpha[2], 1, 0)   
    else : 

        control_qubits = list(set(control_qubits))
        
        # Step b
        # Design an (n-1)-qubit arbitrary statevector
        # generator circuit, recursively, employing the first (n-1) qubits on the
        # system.

        QCircuit = custom_amplitude_encoding(QCircuit, alpha , n - 1 , control_qubits)

        # Step c
        # Employ an (n-1)-qubit controlled 𝑅𝑦 (𝛼3) gate, with control on first (n-1)
        # qubits and target on last qubit.

        
        # multi_ctr_RYGate =  RYGate(alpha[n]).control(n-1 + len(control_qubits),label=None)
        multi_ctr_RYGate =  RYGate(alpha[2**(n-1)-1]).control(n-1 + len(control_qubits),label=None)
        QCircuit.append(multi_ctr_RYGate, list(range(0, n-1)) + control_qubits + [n-1] )

        # Step d 
        # Employ (n-1) CNOT gates, one by one, on each of the first (n-1) qubits.
        # Each of these CNOT gates has control on the last qubit.

        multi_ctr_XGate =  XGate().control(1 + len(control_qubits),label=None)
        for i in range(n-1):
            QCircuit.append(multi_ctr_XGate, [n-1] + control_qubits + [i] )
            # QCircuit.cx(n-1,i)
        
        # Step e
            
        # Employ another (n-1)-qubit arbitrary statevector generator circuit with the last
        # (2**𝑛−1 − 1) angles, recursively, on first (n-1) qubits. Each gate in this subcircuit
        # must have additional control from last qubit.
            
        control_qubits.append(n-1)
        QCircuit = custom_amplitude_encoding(QCircuit, alpha[2**(n-1):] , n - 1 , control_qubits)

    return QCircuit


if __name__ == "__main__" : 


    number_of_qubits =  5
    show_plot = True

    # Generate random numbers
    c = np.random.rand(2**number_of_qubits)-0.5
    # Convert it into a statevector
    c = c / np.sqrt(sum(np.abs(c)**2))      
    # Find the angles "alpha"
    alpha = solve_spherical_angles(c)
    # print("c = " , c)
    # print("Spherical angles:", alpha)


    # Create a quantum circuit with one qubit
    qc = QuantumCircuit(number_of_qubits)

    
    # Create the circuit     
    # Apply the Ry gate with the specified angle
    # qc.ry(alpha[0], 0)
    # qc = custom_amplitude_encoding(qc, list(range(0, 2**number_of_qubits-1)), number_of_qubits )
    qc = custom_amplitude_encoding(qc, alpha, number_of_qubits )
    # qc = custom_amplitude_encoding(qc, alpha, 2 , [] )
    

    
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

    # Get the final state vector
    state_vector = result.get_statevector()
    # print("\n\nFinal state vector:    ", state_vector.data)    

    # Define a tolerance for comparison
    tolerance = 1e-6  # Example tolerance, you can adjust as needed

    # Check if the actual and expected values are equal within the tolerance
    if np.allclose(state_vector.data,  c + 0j , atol=tolerance):
        print(f"The actual values match the expected values within the tolerance ({tolerance}).")
        print("YEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEES")
    else:        
        print("Final state vector:    ", state_vector.data)    
        print("Expected state vector: " , c + 0j )
        print(f"The actual values do not match the expected values within the tolerance ({tolerance}).")
        print("NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    

    


