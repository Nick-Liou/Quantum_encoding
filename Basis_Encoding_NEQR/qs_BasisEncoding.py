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


from pyeda.inter import exprvars, truthtable, espresso_tts
import pyeda.boolalg.minimization

# Monkey-patching
def my_modified__cover2exprs(inputs:list, noutputs:int, cover:Any) -> list[tuple[list[int],list[int]]]:
    """
    Convert a cover to a tuple of Expression instances with modifications.

    This function is a modified version of `pyeda.boolalg.minimization._cover2exprs`.
    It only supports the case where `noutputs` is 1.

    Args:
        inputs (tuple): A tuple of input variables.
        noutputs (int): Number of output variables (should be 1 for this function).
        cover (list): List of cover tuples.

    Returns:
        list: A list of terms where each term is represented as a list containing two lists:
            - The first list represents the positive literals (minterms).
            - The second list represents the negative literals .
    """

    if noutputs != 1 : 
        raise ValueError("noutputs should be 1 for my custom implementation")
    
    for i in range(noutputs):
        terms = []
        for invec, outvec in cover:
            if outvec[i]:
                # Initialize a tuple to store positive and negative literals, 
                # my_term[0] has the positive literal and my_term[1] the negative literal
                my_term : tuple[list[int],list[int]] = ([],[])
                for j, v in enumerate(inputs):
                    if invec[j] == 1:
                        # Add index of input variable for negative literal
                        my_term[1].append(j)    # ~v
                    elif invec[j] == 2:         
                        # Add index of input variable for positive literal               
                        my_term[0].append(j)    # v
                terms.append(my_term)

    return terms

# Monkey-patching
pyeda.boolalg.minimization._cover2exprs = my_modified__cover2exprs

        


def BasisEncoding(data : Union[list, np.ndarray] , use_Espresso:bool = False ) -> QuantumCircuit :
    """
    Encodes the given data into a quantum circuit using Basis Encoding.

    Args:
        data (list): The list of integers to be encoded.
        use_Espresso (bool, optional): Flag to indicate whether to use Espresso for optimization. Defaults to True.

    Returns:
        QuantumCircuit: The quantum circuit representing the Basis Encoding of the data.


    Example 1 (possitive integers):
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

    Example 2 (with negative integers):  
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
        q_0: ┤ H ├────────────■─────────o──
             ├───┤            │         │
        q_1: ┤ H ├──o────■────┼────o────┼──
             └───┘  │    │    │  ┌─┴─┐┌─┴─┐
        a_0: ───────┼────┼────┼──┤ X ├┤ X ├
                    │  ┌─┴─┐┌─┴─┐└───┘└───┘
        a_1: ───────┼──┤ X ├┤ X ├──────────
                  ┌─┴─┐└───┘└───┘
        a_2: ─────┤ X ├────────────────────
                  └───┘

        Please note that in this context, the last qubit, denoted as a_2, serves as the two's complement bit,
        representing -4 (i.e., -2^2). The preceding qubits, a_0 and a_1, represent binary numbers,
        where a_0 corresponds to 2^0 (equal to 1) and a_1 to 2^1 (equal to 2).

    """

    # pad with zeros if needed
    padded_data = pad_with_zeros(np.array(data))
    
    number_of_qubits = int ( np.ceil(np.log2(len(padded_data))) )
    
    # For now only works for integeres
    bin_data , bit_depth = convert_to_bin(padded_data)

    
    # Indices of data
    qr1 = QuantumRegister(number_of_qubits, "q") 
    # Data
    qr2 = QuantumRegister(bit_depth, "a")    

    # Create a quantum circuit with multipule qubits
    qc = QuantumCircuit(qr1 ,qr2 )


    # Create a superposition for all the indices 
    qc.h(range(number_of_qubits))
    
    if not use_Espresso:
        # Set up the data 
        for i in range(len(padded_data)):
            for j in range(bit_depth):            
                if bin_data[i][j] == '1' :
                    qubits_ids = list(range(number_of_qubits)) + [number_of_qubits + bit_depth - j - 1]
                    qc.append(MCXGate(num_ctrl_qubits=number_of_qubits, ctrl_state=i), qubits_ids )
    else:        
        
        # import warnings
        # warnings.warn("The espresso optimization is not yet implemented correctly", category=RuntimeWarning)
        raise Exception("The espresso optimization is not yet implemented correctly")
        
        # Define the variables x[0], x[1],..., and x[number_of_qubits]
        X = exprvars('x', number_of_qubits)

        # Set up the data 
        for j in range(bit_depth):            
            truth_table = ""
            for i in range(len(padded_data)):
                truth_table += bin_data[i][j]
                
            # Define the truth table
            f = truthtable(X, truth_table)
            
            # Minimize the truth table using Espresso
            fm = espresso_tts(f)

            for contition in fm:
                pos_ctrl_qubits_ids = contition[0]
                neg_ctrl_qubits_ids = contition[1]
                target_qubit = number_of_qubits + bit_depth - j - 1
                # print(len(kkk)-1)
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


def int_to_binary(arr: Union[list, np.ndarray]) -> tuple[list[str],int]:
    """
    Converts a list of integers to their binary representations with a given bit width.

    Args:
        arr (list): The list of integers to be converted.

    Returns:
        tuple: A tuple containing the binary representations of the integers in `arr` and the maximum length of binary strings.
    """
    binary_array = []  # Initialize an empty list to store binary representations
    max_abs_value = max(map(abs, arr))  # Find the maximum absolute value in the array
    max_length = len(np.binary_repr(int(max_abs_value)))  # Calculate the maximum number of bits needed for any integer
    
    # Add one bit for the "sign" bit if there are negative numbers in the array
    if min(arr) < 0:        
        max_length += 1 
        # This could be optimized in special cases, when -2**i is in arr but 2**i is not, to use one less bit 

    # Convert each integer to binary representation with the specified width
    binary_array = list(map(lambda num: np.binary_repr(int(num), width=max_length), arr))
    
    return binary_array, max_length





if __name__=="__main__": 

    # array = [0, 1, 2, -1.00 , -4 ]


    # data_length = 4
    # data = np.random.randint(low=0, high=3, size=data_length)

    data = [1, -1, 3, 5, -1, 4, 6, 7]  # Example input data   
    data = [1, 1, 1, 1, 1, 0, 0, 1]  # Example input data     
    data = [1, 1, 0, 1]  # Example input data     
    qc = BasisEncoding(data , use_Espresso=False)
    print(qc)
    qc = BasisEncoding(data , use_Espresso=True)
    print(qc)

    # print(all_integers(array) ) 

    # print( int_to_binary(array) )

