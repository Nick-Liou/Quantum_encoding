# import the template
import pennylane as qml
from pennylane.templates.embeddings import AmplitudeEmbedding

# quantum device where you want to run and how many Qubits

dev = qml.device('default.qubit', wires=2)
@qml.qnode(dev)
def circuit(data):
    AmplitudeEmbedding(features=data, wires=range(2),normalize=True)
    return qml.state()

data = [6,-12.5,11.15,7]
circuit(data)

# print(circuit.draw(show_all_wires=True))
# Print the circuit diagram
print(qml.draw(circuit, expansion_strategy="device", show_all_wires=True)(data))

print(circuit(data))

# #Print Output
#  0: ──╭QubitStateVector(M0)──╭┤ State 
#  1: ──╰QubitStateVector(M0)──╰┤ State 
# M0 = [ 0.31380835+0.j -0.65376739+0.j  0.58316051+0.j  0.36610974+0.j]