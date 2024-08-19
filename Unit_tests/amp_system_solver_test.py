# from pathlib import Path
# print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())


# Add the parent directory of the current script's directory to the Python path
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
sys.path.append(os.path.dirname(SCRIPT_DIR))  # Add the parent directory to the Python path

import numpy as np
from math import pi

import pytest

from Encodings.qs_AmplitudeEncoding import solve_spherical_angles

def verify_solution(c: np.ndarray, alpha: np.ndarray , max_tolerance:float = 1e-8) -> None:    
    
    if abs ( c[0] -  np.cos(alpha[0]/2) ) > max_tolerance :
        print(f"c[0] = {c[0]}  cos(a[0]/2) = {np.cos(alpha[0]/2)}")
        print(f"diff = {c[0] - np.cos(alpha[0]/2)}")

    assert abs ( c[0] -  np.cos(alpha[0]/2) ) < max_tolerance 

    if c.size != 1:

        sin_prod = 1 
        for i in range(1,len(alpha)):
            
            sin_prod *= np.sin(alpha[i-1]/2)
            temp = np.cos(alpha[i]/2) * sin_prod
            if abs (c[i] -  temp ) > max_tolerance :
                print(f"c[{i}] = {c[i]}  f(a) = {temp}")

            assert abs (c[i] -  temp ) < max_tolerance 

        if  abs( c[-1] - sin_prod * np.sin(alpha[-1]/2) ) > max_tolerance  :
            print(f"c[-1] = {c[-1]}  sin_prod = {sin_prod * np.sin(alpha[-1]/2)}")
        
        assert abs( c[-1] - sin_prod * np.sin(alpha[-1]/2) ) < max_tolerance 



def test_solve_spherical_angles_default() -> None :
    
    c = np.array([2.96, -6.70 ])
    c = c / np.sqrt(sum(np.abs(c)**2))
    alpha = solve_spherical_angles(c)
    verify_solution(c,alpha)



@pytest.mark.parametrize("input", 
                         [([42 ]   ),
                          ([2.96, -6.70 ]   ),
                          ([0, 172, 38, 246]),
                          ([-1.66, -4.05, -7.76,  1.22, -1.33,  6.19,  2.25, -0.85])])
def test_solve_spherical_angles_parametric(input : np.ndarray ) -> None :
    c = input    
    c = c / np.sqrt(sum(np.abs(c)**2))            
    alpha = solve_spherical_angles(c)
    verify_solution(c,alpha)



def test_solve_spherical_angles_radomized() -> None :
    
    num_runs_per_size = 100 
    max_system_test_size = 100
    for system_size in range(1,max_system_test_size):
        for _ in range(num_runs_per_size):
            c =  np.random.rand(system_size) - np.random.rand(1)
            c = c / np.sqrt(sum(np.abs(c)**2))
            alpha = solve_spherical_angles(c)
            verify_solution(c,alpha)


if __name__ == "__main__" : 
    
   
    # number_of_elements = 200 
    # c = np.random.rand(number_of_elements)-0.5
    
    c = np.array([-1,0,0,0,-5,0,0,0])
    c = c / np.sqrt(sum(np.abs(c)**2))            
    alpha = solve_spherical_angles(c)
    verify_solution(c,alpha)

    # print("c = " , c)
    # print("Spherical angles:", alpha)
