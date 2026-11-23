import numpy as np 
import math 

% 
x_cg = 0
z_cg = 0
D_1 = 8 # test number, not real, to be corrected
D_2 = 8
D_3 = 8
D_4 = 8

upper_right_z = W/2 - e1 
upper_left_z = W/2 - e1 
lower_right_z = -W/2 + e1
lower_left_z = -W/2 + e1

upper_right_x = -L/2 + e2 
upper_left_x = L/2 - e2 
lower_right_x = -L/2 + e2
lower_left_x = L/2 - e2

A_1 = math.pi * D_1**2 /4
A_2 = math.pi * D_2**2 /4
A_3 = math.pi * D_3**2 /4
A_4 = math.pi * D_4**2 /4
