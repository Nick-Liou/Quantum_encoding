# import the template
import pennylane as qml
from pennylane import numpy as np
from pennylane.templates.embeddings import AngleEmbedding


dev = qml.device('default.qubit', wires=4)
@qml.qnode(dev)
def circuit(data):
    for i in range(4):
        qml.Hadamard(i)
    for i in range(len(data)):
        AngleEmbedding(features=data[i], wires=range(4),rotation='Y')
    return  qml.state()

data = np.array([[6,-12.5,11.15,7],[8,9.5,-11,-5],[5,0.5,8,-7]])

print(circuit(data))
print()
# print(circuit.draw(show_all_wires=True))
# Print the circuit diagram
print(qml.draw(circuit, expansion_strategy="device", show_all_wires=True)(data))


#print output

# [ 0.01231807+0.j  0.08506659+0.j -0.08261645+0.j -0.57053559+0.j
#  -0.00617374+0.j -0.04263481+0.j  0.04140682+0.j  0.28594865+0.j
#   0.01432609+0.j  0.09893363+0.j -0.09608408+0.j -0.66354082+0.j
#  -0.00718014+0.j -0.04958488+0.j  0.0481567 +0.j  0.33256225+0.j]

#  0: ──H──RY(6)──────RY(8)────RY(5)────╭┤ State 
#  1: ──H──RY(-12.5)──RY(9.5)──RY(0.5)──├┤ State 
#  2: ──H──RY(11.2)───RY(-11)──RY(8)────├┤ State 
#  3: ──H──RY(7)──────RY(-5)───RY(-7)───╰┤ State 