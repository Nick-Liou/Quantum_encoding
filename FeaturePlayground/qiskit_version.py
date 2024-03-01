


import importlib.metadata as metadata

try:
    version = metadata.version("qiskit")
    print("Qiskit version:", version)
except metadata.PackageNotFoundError: 
    print("Qiskit is not installed.")



# import qiskit
# print(qiskit.__version__)




# import pkg_resources
# try:
#     version = pkg_resources.get_distribution("qiskit").version
#     print("Qiskit version:", version)
# except pkg_resources.DistributionNotFound:
#     print("Qiskit is not installed.")
