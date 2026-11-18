

#All relevant forces all placed here:
F_prelaunch = 
F_dynamiclaunch = 
F_transferburn = 
F_micrometoroid = 
F_actuation = 

M_prelaunch = 
M_dynamiclaunch = 
M_transferburn = 
M_micrometeoroid = 
M_actuation = 

Fx = 
Fy =
Fz =

Mx =
My =
Mz =

F_external = np.array([[Fx], [Fy], [Fz]])
M_external = np.array([[Mx], [My], [Mz]])

F_reaction = -F_external
M_reaction = -M_external