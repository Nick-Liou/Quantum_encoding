import numpy as np
from qiskit import QuantumCircuit

# Typing stuff
from typing import Optional, Union
 
def AngleEncoding(data : Union[list, np.ndarray] , min_val : Optional[float] = None , max_val : Optional[float]= None ) -> QuantumCircuit:
    """
    Encodes the given data into a quantum circuit using Angle Encoding.

    Args:
        data (list or numpy.ndarray): The list or array of values to be encoded.
        min_val (float, optional): The minimum value of the data. If not provided, it will be calculated from the data. Defaults to None.
        max_val (float, optional): The maximum value of the data. If not provided, it will be calculated from the data. Defaults to None.

    Returns:
        QuantumCircuit: The quantum circuit representing the Angle Encoding of the data.

    Examples:
    Example 1 (floating numbers):
        >>> data = [0.5, 0.8, 0.3, 0.6]  # Example input data
        >>> min_val = 0.0  # Minimum value
        >>> max_val = 1.0  # Maximum value
        >>> qc = AngleEncoding(data, min_val, max_val)
        >>> print(qc)

              ┌─────────┐ 
        q_0: ─┤ Ry(π/2) ├─
              ├─────────┴┐
        q_1: ─┤ Ry(4π/5) ├
             ┌┴──────────┤
        q_2: ┤ Ry(3π/10) ├
             └┬──────────┤
        q_3: ─┤ Ry(3π/5) ├
              └──────────┘

              
    Example 2 (positive integers):
        >>> data = [0, 172, 38, 246]   # Example input data
        >>> min_val = 0     # Minimum value
        >>> max_val = 255   # Maximum value
        >>> qc = AngleEncoding(data, min_val, max_val)
        >>> print(qc)

                    ┌───────┐
            q_0: ───┤ Ry(0) ├───
                  ┌─┴───────┴─┐
            q_1: ─┤ Ry(2.119) ├─
                 ┌┴───────────┴┐
            q_2: ┤ Ry(0.46816) ├
                 └┬────────────┤
            q_3: ─┤ Ry(3.0307) ├
                  └────────────┘

    """


    number_of_qubits = len(data)

    data = np.array(data)

    # Calculate min_val if it is None, otherwise use the provided value
    min_val = np.min(data) if min_val is None else min_val
    # Calculate max_val if it is None, otherwise use the provided value
    max_val = np.max(data) if max_val is None else max_val

    theta : Union[list, np.ndarray]
    if number_of_qubits == 1 and min_val == max_val :
        theta = [0]
    else:
        # Normalize to the range [0, pi/2]
        theta  = (data - min_val) * (np.pi / 2) / (max_val - min_val)
    
    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(number_of_qubits)


    # Apply rotations based on the normalized angles
    for i in range(number_of_qubits):
        qc.ry(2 * theta[i] , i)


    # Return the final quantum circuit
    return qc 



# Example usage:
if __name__ == "__main__" : 
    
    show_plot = True

    data = [0.5, 0.8, 0.3, 0.6]  # Example input data
    min_val = 0.0  # Minimum value
    max_val = 1.0  # Maximum value
    qc = AngleEncoding(data, min_val, max_val)

    print(qc)

    
    if show_plot:
        from qiskit.visualization import circuit_drawer
        import matplotlib.pyplot as plt
        
        # Plot the circuit
        fig = circuit_drawer(qc, output='mpl', style="iqp")
        plt.show()
        