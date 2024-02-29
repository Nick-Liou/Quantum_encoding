import numpy as np
from qiskit import transpile  
from qiskit.visualization import circuit_drawer 
from qiskit_aer import Aer 

import matplotlib.pyplot as plt

# Typing stuff
from typing import Any, Callable, Union, Optional 
from qiskit import QuantumCircuit
from qiskit.result.result import Result
from qiskit_aer.jobs.aerjob import AerJob
from qiskit_aer.backends.statevector_simulator import StatevectorSimulator

# Custom libraries
from Amplitude_Encoding_QPIE.qs_AmplitudeEncoding   import AmplitudeEncoding
from Angle_encoding_FRQI.qs_AngleEncoding           import AngleEncoding
from Basis_Encoding_NEQR.qs_BasisEncoding           import BasisEncoding


def encode_data(data: Union[list, np.ndarray], 
                encoding_function: Callable[[Union[list, np.ndarray], Any], QuantumCircuit],
                *args: tuple, 
                **kwargs: dict[str, Any]) -> tuple[QuantumCircuit, Result]:
    """
    Encode the given data using the specified encoding function.

    Parameters:
        data (array_like): The data to be encoded. It can be either a list or a NumPy array.
        encoding_function (callable): A function that takes the data and additional arguments,
                                      and returns the QuantumCircuit.
        *args: Additional positional arguments to be passed to the encoding function.
        **kwargs: Additional keyword arguments to be passed to the encoding function.

    Returns:
        tuple: A tuple containing the encoded QuantumCircuit and the result of simulation.
    """
    # Assuming `data` is already prepared and `encoding_function` is implemented as per requirements


    # Apply the custom encoding function
    qc = encoding_function(data, *args, **kwargs)

    # Transpile the circuit for the backend
    transpiled_circuit = transpile(qc, Aer.get_backend('qasm_simulator'))

    # Simulate the transpiled circuit
    backend : StatevectorSimulator = Aer.get_backend('statevector_simulator')
    job : AerJob = backend.run(transpiled_circuit)
    result : Result = job.result()    

    return qc , result



if __name__ == "__main__" : 

    encodings : dict[Callable, dict] =  {
        AmplitudeEncoding:  {},
        AngleEncoding:      {'min_val': 0, 'max_val': 255},
        BasisEncoding:      {'use_Espresso': True},
        # More examples 
        # function_1: {'args': (1, 2)},
        # function_2: {'x': 3, 'y': 4, 'z': 5},
        # function_3: {'message': "Hello, World!"}
    }
    

    show_plot = False
    data_length = 30
    # data_to_encode = np.random.rand(data_length) * 2  -1    
    data_to_encode = np.random.randint(low=0, high=3, size=data_length)
    
    # data_to_encode = np.array( [3, 3, 2, 2] ) 



    encoding_used : Callable = AmplitudeEncoding
    kwargs : dict[str, Any] = encodings.get(encoding_used, {})
    args : tuple = kwargs.pop('args', ())  # Extracting 'args' if present, otherwise empty tuple
    
    
    qc , result  = encode_data(data_to_encode ,  encoding_used , *args, **kwargs )

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

