import subprocess

def execute_exe_with_args(exe_path, args):
    try:
        # Formulate the command as a list where the first item is the executable path
        # followed by its arguments
        command = [exe_path] + args

        # Use subprocess to run the command
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Wait for the process to finish and get the output
        stdout, stderr = process.communicate()

        # Check if there were any errors
        if process.returncode != 0:
            print(f"Error executing {exe_path}: {stderr}")
        else:
            print(f"Output from {exe_path}:")
            print(stdout)
            return stdout
    
    except Exception as e:
        print(f"An error occurred: {e}")

def parse_output( output : str ):

    a = output.split(' ')

    print("std out:" , a)

    num_terms = int(a[0])

    terms = a[1].split('^')
    print(f"terms: {terms} \n")
    assert(num_terms == len(terms))


    for term in terms:
        print()
        if term == '(1)' :
            print("Add a not gate !!")
            control_qbits : list[list[int]] = [[],[]]
        else:
            el = term[1:-1].replace("x",'')
            el = el.split('*')
            print(el)
            input_list = el 
            control_qbits = [[int(s[1:]) for s in input_list if s.startswith('~')],
                            [int(s) for s in input_list if not s.startswith('~')]   ]
            
            print(f"With '~': {control_qbits[0]}")
            print(f"Without '~': {control_qbits[1]}")
        
        print(control_qbits)



    

# Example usage
if __name__ == "__main__":
    # Path to executable
    folder = "Utilities/esop/"
    exe_name = "esop.exe"

    exe_path = f"{folder}{exe_name}"

    # Command-line arguments to pass to the executable
    args = ["5", "e8a4e8a4"]
    # args = ["3", "ff"]

    # Call the function
    output = execute_exe_with_args(exe_path, args)

    parse_output(output)
