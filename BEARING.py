import numpy as np 
import math 

% 
D_1 = 8 # test number, not real, to be corrected
D_2 = 8 # test number, not real, to be corrected
D_3 = 8# test number, not real, to be corrected
D_4 = 8 # test number, not real, to be corrected

W = 10 # test number, not real, to be corrected
L = 20 # test number, not real, to be corrected

t_2 = 3 # test number, not real, to be corrected
sigma_lug = 814000000 # test number, not real, to be corrected
sigma_wall = 814000000 # test number, not real, to be corrected

upper_right_z = W/2 - e1 
upper_left_z = W/2 - e1 
lower_right_z = -W/2 + e1
lower_left_z = -W/2 + e1

upper_right_x = -L/2 + e2 
upper_left_x = L/2 - e2 
lower_right_x = -L/2 + e2
lower_left_x = L/2 - e2

A_1 = math.pi * D_1**2 /4 # left upper 
A_2 = math.pi * D_2**2 /4 # Right upper 
A_3 = math.pi * D_3**2 /4 # left lower
A_4 = math.pi * D_4**2 /4 # right lower

A_total = A_1 + A_2 + A_3 + A_3 

x_cg = (A_1*upper_left_x + A_2*upper_right_x + A_3*lower_left_x + A_4*lower_right_x) / A_total
z_cg = (A_1*upper_left_z + A_2*upper_right_z + A_3*lower_left_z + A_4*lower_right_z) / A_total


print("TASK 4.5 RESULTS"/n)
print(f"Total area = {A_total:.3f} mm^2")
print(f"x_cg = {x_cg:.3f} mm")
print(f"z_cg = {z_cg:.3f} mm")

# starting 4.6 

#acc forces and moments 
F_x = 60 # test number, not real, to be corrected
F_z = 60 # test number, not real, to be corrected

#force position 
x_force = 0.0 #test number, not real, to be corrected
z_force = 0.0 #test number, not real, to be corrected

fasteners_num = 4 

F_cg = math.sqrt(F_x**2 + F_z**2) # in plane force/ resultant force 

#positive is ccw 
M_y = F_z(x_cg -(R+t_1)/2) + F_x(z_cg)

F_cgx = F_x
F_cgy = F_y

F_inplane_x = F_cgx/fasteners_num 
F_inplane_y = F_cgy/fasteners_num 

r_1 = math.sqrt(upper_left_x**2+upper_left_z**2)
r_2 = math.sqrt(upper_right_x**2+upper_right_z**2)
r_3 = math.sqrt(lower_left_x**2+lower_left_z**2)
r_4 = math.sqrt(lower_right_x**2+lower_right_z**2)

F_inplane_M_1 = M_y*A_1*r_1/(A_1*r_1**2+A_2*r_2**2+A_3*r_3**2+A_4*r_4**2)
F_inplane_M_2 = M_y*A_2*r_2/(A_1*r_1**2+A_2*r_2**2+A_3*r_3**2+A_4*r_4**2)
F_inplane_M_3 = M_y*A_3*r_3/(A_1*r_1**2+A_2*r_2**2+A_3*r_3**2+A_4*r_4**2)
F_inplane_M_4 = M_y*A_4*r_4/(A_1*r_1**2+A_2*r_2**2+A_3*r_3**2+A_4*r_4**2)






# starting 4.7




