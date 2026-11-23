import numpy as np
from scipy.optimize import minimize

#All relevant forces all placed here
#  (x being the direction of the launch vehicle (up positive), y being the solar panel axis (outwards positive), and z being the lateral
F_prelaunch = np.array([[-382.165], [0], [0]])
F_dynamiclaunch = np.array([[2295.54], [688.67], [688.67]])
F_transferburn = np.array([[0.29], [0], [0]])
F_micrometoroid = np.array([[0], [0], [23]])
F_actuation = np.array([[0], [0], [0]])

M_prelaunch = np.array([[0], [0], [707.3]])
M_dynamiclaunch = np.array([[1274.02], [0], [-4246.75]])
M_transferburn = np.array([[0], [0], [-0.5365]])
M_micrometeoroid = np.array([[44.75], [42.55], [0]])
M_actuation = np.array([[0], [0], [0]])

#Total forces and moments for each phase of the mission
F_Launch = F_prelaunch + F_dynamiclaunch
F_Transfer = F_transferburn + F_micrometoroid + F_actuation
F_Mpo = F_micrometoroid + F_actuation

M_Launch = M_prelaunch + M_dynamiclaunch
M_Transfer = M_transferburn + M_micrometeoroid + M_actuation    
M_Mpo = M_micrometeoroid + M_actuation

print("Total Launch Forces: ", F_Launch)
print("Total Launch Moments: ", M_Launch)
print("Total Transfer Forces: ", F_Transfer)
print("Total Transfer Moments: ", M_Transfer)
print("Total MPO Forces: ", F_Mpo)
print("Total MPO Moments: ", M_Mpo)
#Bruhn analysis to determine geometrical parameters:
# w, t1, D1, h, t2, D2 of the lug


# Tension across net section
k_u = 0.85
F_tu = 400 * 10**6 #Pa
A_t = 0.0001 #m^2
P_u  = k_u * F_tu * A_t

# Shear Out-bearing strength

# 

