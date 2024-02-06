import pennylane as qml
from pennylane import numpy as np

# import the template
from pennylane.templates.embeddings import BasisEmbedding

# quantum device where you want to run and how many Qubits
dev = qml.device('default.qubit', wires=6)

@qml.qnode(dev)
def circuit(data):
    for i in range(6):
        qml.Hadamard(i)
    for i in range(len(data)):
        # BasisEmbedding(features=data[i], wires=range(6),do_queue=True)
        BasisEmbedding(features=data[i], wires=range(6))
    return  qml.state()

data=[[1,0,1,1,1,0],
      [1,0,0,0,0,1]]

circuit(data)

# print(circuit.draw(show_all_wires=True))
print(qml.draw(circuit, expansion_strategy="device",show_all_wires=True)(data))

#print output

#  0: ──H──X──X──╭┤ State 
#  1: ──H────────├┤ State 
#  2: ──H──X─────├┤ State 
#  3: ──H──X─────├┤ State 
#  4: ──H──X─────├┤ State 
#  5: ──H──X─────╰┤ State 




# And, the output state is:

print(circuit(data))

for x in data :
    print("\n\nx is :" , x)
    print(circuit(x))