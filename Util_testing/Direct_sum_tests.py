import numpy as np

def direct_sum(A, B):
    """
    Computes the direct sum of two matrices A and B.
    Args:
        A (np.ndarray): First matrix.
        B (np.ndarray): Second matrix.
    Returns:
        np.ndarray: Direct sum of matrices A and B.
    """
    if np.array_equal(A, np.array([])) :
        return B 

    # Get dimensions of input matrices
    m, n = A.shape
    p, q = B.shape

    # Create a zero matrix of appropriate size
    direct_sum_matrix = np.zeros((m + p, n + q))

    # Insert matrices A and B into the direct sum matrix
    direct_sum_matrix[:m, :n] = A
    direct_sum_matrix[m:, n:] = B

    return direct_sum_matrix


def amplitude_embedding_sub_matrix ( p_arr ):
    """
    Computes a matrix for amplitude embedding.
    Args:
        p_arr (np.ndarray): Array with probabilites to generate matrices for the direct sum.
    Returns:
        np.ndarray: Direct sum of matrices, one 2x2 for each element of p_arr.
    """

    # result = np.array([[],[]]) 
    result = np.array([])
    for p in p_arr :
        A = np.array([[np.sqrt(p), np.sqrt(1-p)],
                       [np.sqrt(1-p), -np.sqrt(p)]])
        # print(A)
        # print()
        # print(np.dot(A, np.conjugate(np.transpose(A)) ))
        # print()

        result = direct_sum(result , A )        
        # print(result)
        # print()

    # print(np.dot(result, np.conjugate(np.transpose(result)) ))
    # print()
        
    return result

def generate_p(data,qubit_id):

    prob_size = 2**qubit_id
    p = np.zeros((1,prob_size))
    sums = np.zeros((1,prob_size))

    # Simple way
    for i in range(prob_size):
        sum_var = 0 
        for j, element in enumerate(data):
            
            if j % prob_size == i :
                sum_var += element 

        p[i] = data[i] / sum_var

    print(p)

    # Alternative way
    for j, element in enumerate(data):         
        sums[ j % prob_size ] += element
    print(data[1:prob_size]/sums)

    return p 

# amplitude_embedding_sub_matrix([0.5, 0.25, 0.47 ])

generate_p([2,3,3,2],1)

# # Example usage:
# A = np.array([[1, 2], [3, 4]])
# B = np.array([[5, 6], [7, 8]])
# print(A)
# print(B)

# direct_sum_matrix = direct_sum(A, B)
# print("Direct sum of A and B:")
# print(direct_sum_matrix)
