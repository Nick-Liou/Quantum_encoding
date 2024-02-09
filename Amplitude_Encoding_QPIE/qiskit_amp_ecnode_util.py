import numpy as np
from math import pi

def solve_spherical_angles_slow(c):
    # # Ensure c contains positive values
    # if any(val <= 0 for val in c):        
    #     raise ValueError("All elements of c must be positive")

    n = len(c) - 1
    alpha = np.zeros(n)

    alpha[0] = 2 * np.arccos(abs(c[0]))
    
    for i in range(1, n):
        alpha[i] = 2 * np.arccos(abs(c[i]) / np.prod(np.sin(alpha[:i] / 2) ))


    # Adjust the solution for the signs of c
    for i in range(n):
        if c[i] < 0 :
            alpha[i] = 2*pi - alpha[i]

    if c[-1] < 0 :
        alpha[-1] = - alpha[-1]

    return alpha

def solve_spherical_angles(c):
    
    n = len(c) - 1
    alpha = np.zeros(n)

    alpha[0] = 2 * np.arccos(abs(c[0]))
    sin_prod = 1

    # Solve the system for possitive c 
    for i in range(1, n):
        sin_prod *= np.sin(alpha[i-1] / 2)
        if sin_prod == 0 : 
            alpha[i] = pi 
        else:
            alpha[i] = 2 * np.arccos(min(abs(c[i]) / sin_prod , 1))

    # Adjust the solution for the signs of c
    for i in range(n):
        if c[i] < 0 :
            alpha[i] = 2*pi - alpha[i]

    if c[-1] < 0 :
        alpha[-1] = - alpha[-1]

    return alpha

def verify_solution(c, alpha , max_tolerance = 1e-8):    
    
    
    if abs ( c[0] -  np.cos(alpha[0]/2) ) > max_tolerance :
        print(f"c[0] = {c[0]}  cos(a[0]/2) = {np.cos(alpha[0]/2)}")
        print(f"diff = {c[0] - np.cos(alpha[0]/2)}")

    sin_prod = 1 
    for i in range(1,len(alpha)):
        
        sin_prod *= np.sin(alpha[i-1]/2)
        temp = np.cos(alpha[i]/2) * sin_prod
        if abs (c[i] -  temp ) > max_tolerance :
            print(f"c[{i}] = {c[i]}  f(a) = {temp}")
        pass

    if  abs( c[-1] - sin_prod * np.sin(alpha[-1]/2) ) > max_tolerance  :
        print(f"c[-1] = {c[-1]}  sin_prod = {sin_prod * np.sin(alpha[-1]/2)}")










if __name__ == "__main__" : 
    
    # Example usage:
   
    number_of_elements = 2 
    c = np.random.rand(number_of_elements)-0.5
    c = c / np.sqrt(sum(np.abs(c)**2))            
    alpha = solve_spherical_angles(c)
    verify_solution(c,alpha)

    # print("c = " , c)
    # print("Spherical angles:", alpha)


    # Check that it works for the default tolerance 10**-10 
    if False :
        num_runs = 1000 
        for i in range(2,100):
            print(f"i = {i} <==========")
            for _ in range(num_runs):
                c =  np.random.rand(i) -0.90
                c = c / np.sqrt(sum(np.abs(c)**2))
                alpha = solve_spherical_angles(c)
                verify_solution(c,alpha)


    # Time the slow and fast functions (The fast is about 3 times faster)
    if False : 
        import time
        num_runs = 10000  # Number of times to run the function

        
        c =  np.random.rand(32) -0.5
        c = c / np.sqrt(sum(np.abs(c)**2))
        # print("c = " , c)
        
        
        # Time solve_spherical_angles_slow
        start_time_slow = time.time()
        for _ in range(num_runs):
            alpha_slow = solve_spherical_angles_slow(c)
        end_time_slow = time.time()
        total_time_slow = (end_time_slow - start_time_slow) 
        print("Average time taken for solve_spherical_angles_slow:", total_time_slow, "seconds")
        # print("Spherical angles (slow):", alpha_slow)

        # Time solve_spherical_angles
        start_time_fast = time.time()
        for _ in range(num_runs):
            alpha_fast = solve_spherical_angles(c)
        end_time_fast = time.time()
        total_time_fast = (end_time_fast - start_time_fast) 
        print("Average time taken for solve_spherical_angles:", total_time_fast, "seconds")
        # print("Spherical angles (fast):", alpha_fast)

        print(f"Speed up: {total_time_slow/total_time_fast}")