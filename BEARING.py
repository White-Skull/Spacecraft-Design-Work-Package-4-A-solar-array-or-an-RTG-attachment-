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
M_y = -F_z(x_cg -(R+t_1)/2) + F_x(z_cg)

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
x_1 = upper_left_x
x_2 = upper_right_x
x_3 = lower_left_x
x_4 = lower_right_x
z_1 =upper_left_z
z_2 =upper_right_z
z_3 =lower_left_z
z_4 =lower_right_z


F_M_x_1 = F_inplane_M_1*(x_1-x_cg)/r_1
F_M_z_1 = F_inplane_M_1*(z_1-z_cg)/r_1

F_M_x_2 = F_inplane_M_2*(x_2-x_cg)/r_2
F_M_z_2 = F_inplane_M_2*(z_2-z_cg)/r_2

F_M_x_3 = F_inplane_M_3*(x_3-x_cg)/r_3
F_M_z_3 = F_inplane_M_3*(z_3-z_cg)/r_3

F_M_x_4 = F_inplane_M_4*(x_4-x_cg)/r_4
F_M_z_4 = F_inplane_M_4*(z_4-z_cg)/r_4

P_1 = math.sqrt((F_inplane_x+F_M_x_1)**2+(F_inplane_z+F_M_z_1)**2)
P_2 = math.sqrt((F_inplane_x+F_M_x_2)**2+(F_inplane_z+F_M_z_2)**2)
P_3 = math.sqrt((F_inplane_x+F_M_x_3)**2+(F_inplane_z+F_M_z_3)**2)
P_4 = math.sqrt((F_inplane_x+F_M_x_4)**2+(F_inplane_z+F_M_z_4)**2)

bearing_stress_1 = P_1/(D_1*t_2)
bearing_stress_2 = P_2/(D_2*t_2)
bearing_stress_3 = P_3/(D_3*t_2)
bearing_stress_4 = P_4/(D_4*t_2)


