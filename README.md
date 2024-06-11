[![Mypy](https://github.com/Nick-Liou/Quantum_encoding/actions/workflows/mypy.yml/badge.svg)](https://github.com/Nick-Liou/Quantum_encoding/actions/workflows/mypy.yml)
[![Tests](https://github.com/Nick-Liou/Quantum_encoding/actions/workflows/pytest.yml/badge.svg)](https://github.com/Nick-Liou/Quantum_encoding/actions/workflows/pytest.yml)
# Quantum Encoding
Comparative Study and Analysis of Classical-to-Quantum Data Encoding through Embedding and Mapping Techniques
<!-- Comparative Analysis of Classical-to-Quantum Mapping Techniques in Data Encoding -->

## Description

Quantum Encoding is a research project aimed at investigating various classical-to-quantum data encoding techniques through embedding and mapping methodologies. The project explores different approaches to encode classical data into quantum states, with a focus on understanding their effectiveness and applicability in quantum information processing tasks.

## Techniques implemented
<!-- - Qubit Lattice -->
- Basis Encoding - (NEQR) Novel Enhanced Quantum Representation 
- Amplitude Encoding - (QPIE) Quantum Probability Image Encoding  
- Angle Encoding

<!-- ## Techniques to be implemented
- (FRQI) Flexible Representation of Quantum Images 
- Quantum Associative Memory
- Displacement Encoding
- IQP Encoding
- QAOA Encoding
- Squeezing Encoding
- Hybrid Encodings -->


## Installation

1. Clone this repository:   
    ```
    git clone https://github.com/Nick-Liou/Quantum_encoding.git
    ```
2. Navigate to the project directory:   
    ```
    cd quantum_encoding
    ```
3. Install the required dependencies using pip:
    ```
    pip install -r requirements.txt
    ```
<!-- Use  "pipreqs" to auto generate the requirements  -->
<!-- mypy --ignore-missing-imports --explicit-package-bases  . -->

## Usage

In the `General_encoding.py` file, users can select an encoding technique from the implemented ones, adjust optional arguments, and provide their data for encoding.

