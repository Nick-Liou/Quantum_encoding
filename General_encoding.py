import numpy as np
from qiskit import transpile
from qiskit_aer import Aer
from qiskit.visualization import circuit_drawer

from Amplitude_Encoding_QPIE.qs_AmplitudeEncoding import AmplitudeEncoding

def encode_data(data, encoding_function):
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
    qc = encoding_function(data)

    # Transpile the circuit for the backend
    transpiled_circuit = transpile(qc, Aer.get_backend('qasm_simulator'))

    # Simulate the transpiled circuit
    backend = Aer.get_backend('statevector_simulator')
    job = backend.run(transpiled_circuit)
    result = job.result()

    return qc , result



if __name__ == "__main__" : 

    data_length = 7
    data_to_encode = np.random.rand(data_length)-0.5

    qc , result = encode_data(data_to_encode ,  AmplitudeEncoding )

    state_vector = result.get_statevector()

    
    # Print or manipulate the encoded circuit and result as needed
    print(qc)

    print("\n\nFinal state vector: ", state_vector.data)    


