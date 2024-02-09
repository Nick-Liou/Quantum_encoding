from qiskit.ml.circuit.library import RawFeatureVector

circuit = RawFeatureVector(4)
print(circuit.num_qubits)
# prints: 2
 
print(circuit.draw(output='text'))
# prints:
#      ┌──────┐
# q_0: ┤0     ├
#      │  Raw │
# q_1: ┤1     ├
#      └──────┘
 
print(circuit.ordered_parameters)
# prints: [Parameter(p[0]), Parameter(p[1]), Parameter(p[2]), Parameter(p[3])]
 
import numpy as np
state = np.array([1, 0, 0, 1]) / np.sqrt(2)
bound = circuit.assign_parameters(state)
print(bound.draw())
# prints:
#      ┌──────────────────────────────────┐
# q_0: ┤0                                 ├
#      │  initialize(0.70711,0,0,0.70711) │
# q_1: ┤1                                 ├
#      └──────────────────────────────────┘