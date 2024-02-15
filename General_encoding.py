import numpy as np
from qiskit import transpile
from qiskit_aer import Aer
from qiskit.visualization import circuit_drawer

import matplotlib.pyplot as plt

# Custom libraries
from Amplitude_Encoding_QPIE.qs_AmplitudeEncoding   import AmplitudeEncoding
from Angle_encoding_FRQI.qs_AngleEncoding           import AngleEncoding

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
        AmplitudeEncoding: (1, 2),
        AngleEncoding: {'min_val': -0.5, 'max_val': 0.5},
        # More examples 
        # function_1: (1, 2),
        # function_2: {'x': 3, 'y': 4, 'z': 5},
        # function_3: {'message': "Hello, World!"}
    }
    

    show_plot = False    
    data_length = 4 
    data_to_encode = np.random.rand(data_length)-0.5

    print(data_to_encode)

    qc , result = encode_data(data_to_encode ,  encodings[0] , min_val = -0.5 , max_val =  0.5 )

    state_vector = result.get_statevector().data

    
    # Print the circuit in the console
    print(qc)

    print("\n\nFinal state vector: ", state_vector)    

    if show_plot:
        # # Print the circuit in the console
        # print(qc.draw())

        # Plot the circuit
        fig = circuit_drawer(qc, output='mpl', style="iqp")
        plt.show()

