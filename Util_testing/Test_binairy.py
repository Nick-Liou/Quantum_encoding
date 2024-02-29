# type: ignore
def all_integers(arr):
    for element in arr:        
        # Check if the element is an integer or a float representing an integer
        if not isinstance(element, int) and not element.is_integer():
            return False
    return True
# type: ignore
def convert_to_binary_possitive(arr):
    binary_array = []
    max_length = len(bin(int(max(arr)))) - 2  # Calculate the maximum number of bits needed

    for num in arr:
        binary_num = bin(int(num))[2:]  # Convert the number to binary and remove the '0b' prefix
        binary_num = binary_num.zfill(max_length)  # Pad with leading zeros if needed
        binary_array.append(binary_num)

    return binary_array

# type: ignore
def convert_to_binary(arr):
    binary_array = []
    max_abs_value = max(map(abs, arr))
    max_length = len(np.binary_repr(int(max_abs_value)))  # Calculate the maximum number of bits needed
    
    if min(arr) < 0 :
        max_length += 1 

    for num in arr:
        binary_num = np.binary_repr(int(num), width=max_length)  # Convert the number to binary with specified width
        binary_array.append(binary_num)

    return binary_array


import numpy as np
# Example usage:
my_array = np.array([0,2,-1, 0.5])
result = all_integers(my_array)
print("All elements are integers:", result)


arr = [bin(int(i)) for i in my_array]

print(arr)

print(convert_to_binary(my_array))