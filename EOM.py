import numpy as np

#All relevant forces all placed here:
F_prelaunch = np.array([[0], [0], [0]])
F_dynamiclaunch = np.array([[0], [0], [0]])
F_transferburn = np.array([[0], [0], [0]])
F_micrometoroid = np.array([[0], [0], [0]])
F_actuation = np.array([[0], [0], [0]])

M_prelaunch = np.array([[0], [0], [0]])
M_dynamiclaunch = np.array([[0], [0], [0]])
M_transferburn = np.array([[0], [0], [0]])
M_micrometeoroid = np.array([[0], [0], [0]])
M_actuation = np.array([[0], [0], [0]])

F_external = F_prelaunch + F_dynamiclaunch + F_transferburn + F_micrometoroid + F_actuation
M_external = M_prelaunch + M_dynamiclaunch + M_transferburn + M_micrometeoroid + M_actuation

