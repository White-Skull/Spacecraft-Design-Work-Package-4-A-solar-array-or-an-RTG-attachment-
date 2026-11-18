import numpy as np

#All relevant forces all placed here
#  (x being the direction of the launch vehicle (up positive), y being the solar panel axis (outwards positive), and z being the lateral
F_prelaunch = np.array([[-382.165], [0], [0]])
F_dynamiclaunch = np.array([[2295.54], [688.67], [688.67]])
F_transferburn = np.array([[0], [0], [0]])
F_micrometoroidTrans = np.array([[0], [0], [0]])
F_micrometoroidMPO = np.array([[0], [0], [0]])
F_actuation = np.array([[0], [0], [0]])

M_prelaunch = np.array([[0], [0], [0]])
M_dynamiclaunch = np.array([[1274.02], [0], [-4246.75]])
M_transferburn = np.array([[0], [0], [0]])
M_micrometeoroidTrans = np.array([[0], [0], [0]])
M_micrometeoroidMPO = np.array([[0], [0], [0]])
M_actuation = np.array([[0], [0], [0]])

#Total forces and moments for each phase of the mission
F_Launch = F_prelaunch + F_dynamiclaunch
F_Transfer = F_transferburn + F_micrometoroidTrans + F_actuation
F_Mpo = F_transferburn + F_micrometoroidMPO + F_actuation

M_Launch = M_prelaunch + M_dynamiclaunch
M_Transfer = M_transferburn + M_micrometeoroidTrans + M_actuation    
M_Mpo = M_transferburn + M_micrometeoroidMPO + M_actuation

#Bruhn analysis to determine geometrical parameters:
# w, t1, D1, h, t2, D2 of the lug

