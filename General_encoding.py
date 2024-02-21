import numpy as np
from qiskit import transpile 
from qiskit.visualization import circuit_drawer
from qiskit_aer import Aer


import matplotlib.pyplot as plt

# Custom libraries
from Amplitude_Encoding_QPIE.qs_AmplitudeEncoding   import AmplitudeEncoding
from Angle_encoding_FRQI.qs_AngleEncoding           import AngleEncoding
from Basis_Encoding_NEQR.qs_BasisEncoding           import BasisEncoding

def encode_data(data, encoding_function, *args, **kwargs):
    """
    Encode the given data using the specified encoding function.

    Parameters:
        data (array_like): The data to be encoded.
        encoding_function (callable): A function that takes the data,
                                      and returns the QuantumCircuit.

    Returns:
        tuple: A tuple containing the encoded QuantumCircuit and the result of simulation.
    """
    # Assuming `data` is already prepared and `encoding_function` is implemented as per requirements


    # Apply the custom encoding function
    qc = encoding_function(data, *args, **kwargs)

    # Transpile the circuit for the backend
    transpiled_circuit = transpile(qc, Aer.get_backend('qasm_simulator'))

    # Simulate the transpiled circuit
    backend = Aer.get_backend('statevector_simulator')
    job = backend.run(transpiled_circuit)
    result = job.result()

    return qc , result



if __name__ == "__main__" : 

    encodings =  {
        AmplitudeEncoding:  {},
        AngleEncoding:      {'min_val': 0, 'max_val': 255},
        BasisEncoding:      {},
        # More examples 
        # function_1: {'args': (1, 2)},
        # function_2: {'x': 3, 'y': 4, 'z': 5},
        # function_3: {'message': "Hello, World!"}
    }
    

    show_plot = True 
    data_length = 8
    # data_to_encode = np.random.rand(data_length) * 2  -1
    data_to_encode = np.random.random_integers(low= -4 , high= 3 , size=data_length) 



    encoding_used = BasisEncoding
    kwargs = encodings[encoding_used]
    args = kwargs.pop('args', ())  # Extracting 'args' if present, otherwise empty tuple
    

    qc , result = encode_data(data_to_encode ,  encoding_used , *args, **kwargs )

    state_vector = result.get_statevector().data

    
    # Print the circuit in the console
    print(qc)

    print("\n\nFinal state vector: ", state_vector)    

    print("\nData to encode:" , data_to_encode)
    print(f'\nNumber of qubits {qc.num_qubits}')
    print(f"Total number of gates used {qc.size()}")
    print(f"Circuit depth/layers {qc.depth()}")
    print("Gates used:")
    print(qc.count_ops())


    if show_plot:
        # # Print the circuit in the console
        # print(qc.draw())

        # Plot the circuit
        fig = circuit_drawer(qc, output='mpl', style="iqp")
        figure = plt.show()

