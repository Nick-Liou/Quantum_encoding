import subprocess
import sys

def execute_exe_with_args(exe_path:str, args:list[str]) -> str:
    # Formulate the command as a list where the first item is the executable path
    # followed by its arguments
    command = [exe_path] + args

    # Use subprocess to run the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Wait for the process to finish and get the output
    stdout, stderr = process.communicate()

    # Check if there were any errors
    if process.returncode != 0:
        # print(f"Error executing {[exe_path] + args}: {stderr}")
        raise Exception(f"Error executing {[exe_path] + args } Got the error: {stderr}")
        
    # print(f"args: {args} Output from {[exe_path] + args}: {stdout}")
    return stdout
    # try:
    #     pass    
    # except Exception as e:
    #     print(f"An error occurred: {e}")


def parse_output( output : str ) ->list[tuple[list[int],list[int]]]:

    a = output.split(' ')

    # print("std out:" , a)

    num_terms = int(a[0])

    if num_terms == 0 : 
        return [] 

    terms = a[1].split('^')
    if (num_terms != len(terms)):
        print(f"num_terms: {num_terms}")
        print(f"len(terms): {len(terms)}")
        print(f"terms: {terms} \n")
    assert(num_terms == len(terms))

    esop : list[tuple[list[int],list[int]]] = []
    for term in terms:
        # print()
        control_qbits : tuple[list[int],list[int]] 
        if term == '(1)' :
            # print("Add a not gate !!")
            control_qbits  = ([],[])
        else:
            term_without_x = term[1:-1].replace("x",'')
            el = term_without_x.split('*')
            # print(el)
            input_list = el 
            control_qbits = (
                [int(s[1:]) for s in input_list if s.startswith('~')],
                [int(s) for s in input_list if not s.startswith('~')]   )
            
            # print(f"With '~': {control_qbits[0]}")
            # print(f"Without '~': {control_qbits[1]}")
        esop.append(control_qbits)
        
        # print(control_qbits)
    return esop 



if sys.platform.startswith('linux'):
    # print("Running on Linux")
    exe_name = "esop_static_linux.exe"
elif sys.platform.startswith('win'):
    # print("Running on Windows")
    exe_name = "esop_static_windows.exe"
else:
    print("Not running on Linux or Windows, the esop.exe utility must be recompiled for this os.")

    
folder = "Utilities/esop/"
# exe_name = "esop.exe"

# Path to executable
exe_path = f"{folder}{exe_name}"

# Example usage
if __name__ == "__main__":

    # Command-line arguments to pass to the executable
    import secrets

    n_qubits = 4
    rand_hex =''.join(secrets.choice('0123456789abcdef') for _ in range(2**(n_qubits-2)))
    args = [str(n_qubits), rand_hex]
    args = ["5", "e8a4e8a4"]
    args = ["4", "fffe"]
    args = ["3", "f9"]
    args = ["3", "05"]

    # Call the function
    output = execute_exe_with_args(exe_path, args)

    control_qubits = parse_output(output)
    print("Control qubits: \n" , control_qubits)
    print("Number of terms: \n" , len(control_qubits) )
    print(f"Variables: {n_qubits}  hex_length: {2**(n_qubits-2)}")



    
