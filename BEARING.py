import numpy as np 
import math 

% 
x_cg = 0
z_cg = 0
D_1 = 8 # test number, not real, to be corrected
D_2 = 8 # test number, not real, to be corrected
D_3 = 8# test number, not real, to be corrected
D_4 = 8 # test number, not real, to be corrected

W = 10 # test number, not real, to be corrected
L = 20 # test number, not real, to be corrected

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

x_cg = (A_1*upper_left_x + A_2*upper_right_x + A_3*lower_left_x + A_4*lower_right_x) / A_total
z_cg = (A_1*upper_left_z + A_2*upper_right_z + A_3*lower_left_z + A_4*lower_right_z) / A_total
