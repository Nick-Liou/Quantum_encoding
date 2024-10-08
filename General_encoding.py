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
from Encodings.qs_AmplitudeEncoding     import AmplitudeEncoding
from Encodings.qs_AngleEncoding         import AngleEncoding
from Encodings.qs_BasisEncoding         import BasisEncoding
from Encodings.qs_FRQI                  import FRQIEncoding

from Utilities.decorators import get_time

# @get_time
def encode_data(data: Union[list, np.ndarray], 
                encoding_function: Callable[[Union[list, np.ndarray]], QuantumCircuit],
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
    #  AerSimulator(method="statevector")
    job : AerJob = backend.run(transpiled_circuit)
    result : Result = job.result()    

    return qc , result


 
if __name__ == "__main__" : 

    show_plot = True
    data_to_encode : Union[list, np.ndarray]
    encoding_used : Callable


    encodings : dict[Callable[[Union[list, np.ndarray]], QuantumCircuit], dict] =  {
        AmplitudeEncoding:  {},
        # AngleEncoding:      {},
        AngleEncoding:      {'min_val': 0, 'max_val': 255},
        # AngleEncoding:      {'min_val': -10, 'max_val': 10},
        BasisEncoding:      {'use_Espresso': True},
        # FRQIEncoding:       {},
        # FRQIEncoding:       {'min_val': -10, 'max_val': 10},
        FRQIEncoding:       {'min_val': 0, 'max_val': 255},
        
    }    

    
    # encoding_used = AngleEncoding
    # data_to_encode = [2.96, -6.70 ]     # Example 1 For Angle Encoding
    # data_to_encode = [0, 172, 38, 246]  # Example 2 For Angle Encoding

    
    encoding_used = AmplitudeEncoding
    # data_to_encode = [2.96, -6.70 ]                                               # Example 1 For Amplitude Encoding
    data_to_encode = [0, 172, 38, 246]                                            # Example 2 For Amplitude Encoding
    # data_to_encode = [-1.66, -4.05, -7.76,  1.22, -1.33,  6.19,  2.25, -0.85]     # Example 3 For Amplitude Encoding


    
    # encoding_used = BasisEncoding
    # data_to_encode = [0, 0, 0, 0, 0, 0, 0, 0]                               # Only Hadamard gates For Basis Encoding
    # data_to_encode = [15, 7 ]                                               # Example 1 For Basis Encoding
    # data_to_encode = [-7, 2,5,4 ]                                           # Example 2 For Basis Encoding
    # data_to_encode = [0, 172, 38, 246]                                      # Example 3 For Basis Encoding
    # data_to_encode = [2, 3, 8, 5, 11, 13, 14, 5, 1, 8, 4, 14, 3, 6, 2, 7]   # Example 4 For Basis Encoding


    
    # encoding_used = FRQIEncoding    
    # data_to_encode = [2.96, -6.70 ]                                                                   # Example 1 For FRQI Encoding
    # data_to_encode = [0, 172, 38, 246]                                                                # Example 2 For FRQI Encoding
    # data_to_encode = [[159, 53, 139, 89], [120, 247, 40, 220], [173, 60, 89, 32], [181, 59, 13, 94]]  # Example 3 For FRQI Encoding
    # data_to_encode = [159, 53, 139, 89, 120, 247, 40, 220, 173, 60, 89, 32, 181, 59, 13, 94]          # Example 4 For FRQI Encoding

    # Randomized input
    # data_length = 16
    # data_to_encode = np.random.randint(low=0, high=15, size=data_length)

    

    kwargs : dict[str, Any] = encodings.get(encoding_used, {})
    args : tuple = kwargs.pop('args', ())  # Extracting 'args' if present, otherwise empty tuple
    
    
    qc: QuantumCircuit
    result: Result
    qc , result  = encode_data(data_to_encode ,  encoding_used , *args, **kwargs )

    state_vector = result.get_statevector().data

    
    # Print the circuit in the console
    print(qc)

    print("\n\nFinal state vector: ", state_vector)  
    # print("\n\nFinal real state vector: ", state_vector.real)    
    print("Indices of non-zero elements in the statevector:", np.nonzero(state_vector)[0])

    print("\nData to encode:" , data_to_encode)
    print(f'\nNumber of qubits {qc.num_qubits}')
    print(f"Total number of gates used {qc.size()}")
    print(f"Circuit depth/layers {qc.depth()}")
    # print("Gates used:",qc.count_ops())


    if show_plot:
        # # Print the circuit in the console
        # print(qc.draw())

        # Plot the circuit
        fig = circuit_drawer(qc, output='mpl', style="iqp")
        figure = plt.show()

