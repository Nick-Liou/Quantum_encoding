import numpy as np
from qiskit import QuantumCircuit , QuantumRegister
from qiskit.circuit.library import MCXGate

# Add the parent directory of the current script's directory to the Python path
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path

# Import Local modules
from Utilities.utils import pad_with_zeros

# Typing stuff
from typing import Any, Union

import warnings
from Utilities.esop import call_esop_exe

 


def BasisEncoding(data : Union[list, np.ndarray] , use_Espresso:bool = True ) -> QuantumCircuit :
    """
    Encodes the given data into a quantum circuit using Basis Encoding.

    Args:
        data (list): The list of integers to be encoded.
        use_Espresso (bool, optional): Flag to indicate whether to use Espresso for optimization. Defaults to True. 
                                        Can only be used for data length up to 2^16 

    Returns:
        QuantumCircuit: The quantum circuit representing the Basis Encoding of the data.


    Examples:
    Example 1 (possitive integers):
        >>> data = [1, 1, 0, 1]  # Example input data      
        # Without Espresso:
        >>> qc = BasisEncoding(data , use_Espresso=False)
        >>> print(qc)
             ┌───┐
        q_0: ┤ H ├──o────■────■──
             ├───┤  │    │    │
        q_1: ┤ H ├──o────o────■──
             └───┘┌─┴─┐┌─┴─┐┌─┴─┐
          a: ─────┤ X ├┤ X ├┤ X ├
                  └───┘└───┘└───┘

        # With Espresso:
        >>> qc = BasisEncoding(data , use_Espresso=True)
        >>> print(qc)
             ┌───┐
        q_0: ┤ H ├──o──
             ├───┤  │
        q_1: ┤ H ├──■──
             ├───┤┌─┴─┐
          a: ┤ X ├┤ X ├
             └───┘└───┘
    
    Example 2 (possitive integers):
        >>> data = [1, 5, 3, 7]  # Example input data      
        # Without Espresso:
        >>> qc = BasisEncoding(data , use_Espresso=False)
        >>> print(qc)
             ┌───┐
        q_0: ┤ H ├──o────■────■────o────o────■────■────■──
             ├───┤  │    │    │    │    │    │    │    │  
        q_1: ┤ H ├──o────o────o────■────■────■────■────■──
             └───┘┌─┴─┐  │  ┌─┴─┐  │  ┌─┴─┐  │    │  ┌─┴─┐
        a_0: ─────┤ X ├──┼──┤ X ├──┼──┤ X ├──┼────┼──┤ X ├
                  └───┘  │  └───┘┌─┴─┐└───┘  │  ┌─┴─┐└───┘
        a_1: ────────────┼───────┤ X ├───────┼──┤ X ├─────
                       ┌─┴─┐     └───┘     ┌─┴─┐└───┘     
        a_2: ──────────┤ X ├───────────────┤ X ├──────────
                       └───┘               └───┘

        # With Espresso:
        >>> qc = BasisEncoding(data , use_Espresso=True)
        >>> print(qc)
             ┌───┐
        q_0: ┤ H ├──■───────
             ├───┤  │
        q_1: ┤ H ├──┼────■──
             ├───┤  │    │
        a_0: ┤ X ├──┼────┼──
             └───┘  │  ┌─┴─┐
        a_1: ───────┼──┤ X ├
                  ┌─┴─┐└───┘
        a_2: ─────┤ X ├─────
                  └───┘

    Example 3 (with negative integers):  
        >>> data = [-3, -1, 3, 2]  # Example input data   
        # Without Espresso:
        >>> qc = BasisEncoding(data , use_Espresso=False)
        >>> print(qc)   
             ┌───┐
        q_0: ┤ H ├──o────o────■────■────■────o────o────■──
             ├───┤  │    │    │    │    │    │    │    │
        q_1: ┤ H ├──o────o────o────o────o────■────■────■──
             └───┘  │  ┌─┴─┐  │    │  ┌─┴─┐  │  ┌─┴─┐  │
        a_0: ───────┼──┤ X ├──┼────┼──┤ X ├──┼──┤ X ├──┼──
                    │  └───┘  │  ┌─┴─┐└───┘┌─┴─┐└───┘┌─┴─┐
        a_1: ───────┼─────────┼──┤ X ├─────┤ X ├─────┤ X ├
                  ┌─┴─┐     ┌─┴─┐└───┘     └───┘     └───┘
        a_2: ─────┤ X ├─────┤ X ├─────────────────────────
                  └───┘     └───┘
        
        # With Espresso:
        >>> qc = BasisEncoding(data , use_Espresso=True)
        >>> print(qc)
             ┌───┐
        q_0: ┤ H ├───────o────■──
             ├───┤       │    │
        q_1: ┤ H ├──o────o────■──
             ├───┤  │    │  ┌─┴─┐
        a_0: ┤ X ├──┼────┼──┤ X ├
             ├───┤  │  ┌─┴─┐└───┘
        a_1: ┤ X ├──┼──┤ X ├─────
             └───┘┌─┴─┐└───┘
        a_2: ─────┤ X ├──────────
                  └───┘

        Please note that in this context, the last qubit, denoted as a_2, serves as the two's complement bit,
        representing -4 (i.e., -2^2). The preceding qubits, a_0 and a_1, represent binary numbers,
        where a_0 corresponds to 2^0 (equal to 1) and a_1 to 2^1 (equal to 2).

    """

    # pad with zeros if needed
    padded_data = pad_with_zeros(np.array(data))
    
    number_of_qubits = int ( np.ceil(np.log2(len(padded_data))) )

    if (number_of_qubits > 16 and use_Espresso ):
        use_Espresso = False        
        warnings.warn("Espresso optimization can not be used (in this version) for when the length of the input data is greater than 2^16", UserWarning)
    
    # For now only works for integeres
    bin_data , bit_depth = convert_to_bin(padded_data)
    
    # Indices of data
    qr1 = QuantumRegister(number_of_qubits, "a") 
    # Data
    qr2 = QuantumRegister(bit_depth, "d")    

    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(qr1 ,qr2 )

    # Create a superposition for all the addresses
    qc.h(range(number_of_qubits))
    
    if not use_Espresso:
        # Set up the data 
        for i in range(len(padded_data)):
            for j in range(bit_depth):            
                if bin_data[i][j] == '1' :
                    qubits_ids = list(range(number_of_qubits)) + [number_of_qubits + bit_depth - j - 1]
                    qc.append(MCXGate(num_ctrl_qubits=number_of_qubits, ctrl_state=i), qubits_ids )
    else:        
        # Set up the data 
        not_dict = {"0":"1" , "1":"0"}
        for j in range(bit_depth):            
            truth_table = ""
            inv_truth_table = ""
            for i in range(len(padded_data)):
                truth_table += bin_data[i][j]
                inv_truth_table += not_dict[bin_data[i][j]]
            

            hex_truth_table = bin_str_to_hex_str(truth_table)
            inv_hex_truth_table = bin_str_to_hex_str(inv_truth_table)
            
            output = call_esop_exe.execute_exe_with_args(call_esop_exe.exe_path , [str(number_of_qubits),hex_truth_table])
            output_inv = call_esop_exe.execute_exe_with_args(call_esop_exe.exe_path , [str(number_of_qubits),inv_hex_truth_table])
            
            minimized_expretion =  call_esop_exe.parse_output(output)
            minimized_expretion_inv =  call_esop_exe.parse_output(output_inv)

            optimal_minimized_expretion :  list[tuple[list[int], list[int]]]

            if (len(minimized_expretion_inv) < len(minimized_expretion) ):           
                start_pad : list[tuple[list[int], list[int]]] = [([],[])]
                optimal_minimized_expretion = start_pad + minimized_expretion_inv  # Insert ([],[]) at index 0 (This adds a NOT gate)
            else:
                optimal_minimized_expretion = minimized_expretion
            
            for contition in optimal_minimized_expretion:
                pos_ctrl_qubits_ids = contition[0]
                neg_ctrl_qubits_ids = contition[1]
                target_qubit = number_of_qubits + bit_depth - j - 1

                if len(pos_ctrl_qubits_ids) == 0 and len(neg_ctrl_qubits_ids) == 0 :
                    qc.x(target_qubit)
                else:
                    kkk =  pos_ctrl_qubits_ids + neg_ctrl_qubits_ids + [target_qubit]
                    qc.append(MCXGate(num_ctrl_qubits=len(kkk)-1, ctrl_state= 2**(len(pos_ctrl_qubits_ids))-1 ), kkk )
    
    # Return the final quantum circuit
    return qc 


def convert_to_bin(arr: Union[list, np.ndarray]) -> tuple[list[str],int]:
    """
    Converts a list of integers to their binary representations with a given bit width.

    Args:
        arr (list): The list of integers to be converted.

    Returns:
        tuple: A tuple containing the binary representations of the integers in `arr` and the maximum length of binary strings.
    """
    if all_integers(arr):  # Check if all elements in the array are integers
        return int_to_binary(arr)  # Convert integers to binary
    else:
        # If the array contains non-integer elements, raise a ValueError
        raise ValueError(
            "Float representation is not yet supported, please input integers. \n"
            "Hint: You can multiply your numbers by a constant such as 2**k before "
            "casting them into int to increase the number of decimals used."
        )

        # Future expansion: Add handling for floating-point numbers

    

def all_integers(arr: Union[list, np.ndarray]) -> bool :
    """
    Checks if all elements in the given array are integers or floats representing integers.

    Args:
        arr (list): The array to be checked.

    Returns:
        bool: True if all elements are integers or floats representing integers, False otherwise.
    """
    for element in arr:
        # Check if the element is an integer or a float representing an integer
        if not isinstance(element, int) and not element.is_integer():
            return False
    return True



def int_to_binary(arr: Union[list[int], np.ndarray[np.int_,Any]]) -> tuple[list[str],int]:
    """
    Converts a list of integers to their binary representations with a given bit width.

    Args:
        arr (list): The list of integers to be converted.

    Returns:
        tuple: A tuple containing the binary representations of the integers in `arr` and the maximum length of binary strings.
    """
    binary_array = []  # Initialize an empty list to store binary representations
    max_abs_value : int = max(map(abs, arr)) # type: ignore # Find the maximum absolute value in the array 
    max_length = len(np.binary_repr(int(max_abs_value)))  # Calculate the maximum number of bits needed for any integer
    
    # Add one bit for the "sign" bit if there are negative numbers in the array
    if min(arr) < 0:        
        max_length += 1 
        # This could be optimized in special cases, when -2**i is in arr but 2**i is not, to use one less bit 

    # Convert each integer to binary representation with the specified width
    binary_array = list(map(lambda num: np.binary_repr(int(num), width=max_length), arr))
    
    return binary_array, max_length

def bin_str_to_hex_str(binary_num: str) -> str:
    """
    Convert a binary string to a hexadecimal string.

    Args:
        binary_num (str): A binary string consisting of '0's and '1's.

    Returns:
        str: A hexadecimal string representing the converted binary number.

    Examples:
        >>> bin_str_to_hex_str("110101")
        'd1'
        >>> bin_str_to_hex_str("10101011")
        'ab'
        >>> bin_str_to_hex_str("111100001111")
        'f0f'
    """
    lookup_table = {
        "0000": "0", "0001": "1", "0010": "2", "0011": "3",
        "0100": "4", "0101": "5", "0110": "6", "0111": "7",
        "1000": "8", "1001": "9", "1010": "a", "1011": "b",
        "1100": "c", "1101": "d", "1110": "e", "1111": "f",
        "00": "0", "01": "1", "10": "2", "11": "3"
    }
    hex_num = ""
    for i in range(0, len(binary_num), 4):
        chunk = binary_num[i:i + 4]
        hex_num += lookup_table[chunk]
    return hex_num





if __name__=="__main__": 

    show_plot = True

    # data_length = 4
    # data = np.random.randint(low=0, high=3, size=data_length)

    data = [1, -1, 3, 5, -1, 4, 6, 7]  # Example input data   
    data = [1, 1, 1, 1, 1, 0, 0, 1]  # Example input data     
    data = [1, 1, 0, 1]  # Example input data    

    print("\nData to encode:" , data)

    qc_simple = BasisEncoding(data , use_Espresso=False)
    print("Simple quantum circuit: \n" , qc_simple)

    qc_optimized = BasisEncoding(data , use_Espresso=True)
    print("Optimized quantum circuit: \n" ,qc_optimized)



    if show_plot:
        from qiskit.visualization import circuit_drawer
        import matplotlib.pyplot as plt
        
        # Plot the circuit
        fig_1 = circuit_drawer(qc_simple, output='mpl', style="iqp")
        fig_2 = circuit_drawer(qc_optimized, output='mpl', style="iqp")
        plt.show()
        