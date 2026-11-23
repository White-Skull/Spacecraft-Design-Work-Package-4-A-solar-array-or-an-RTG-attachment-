import math
import numpy as np


Fy = 2000.0
Mz = 300.0
load_factor = 1.0

coordinates = np.array ([
    [-1, -1],
    [-1, 1],
    [1, -1],
    [1, 1]])
nf = len(coordinates)

D2 = 0.005            # Fastener diameter [m]
Dfi_2 = 0.006        # Inboard diameter, lug side
Dfi_3 = 0.006        # Inboard diameter, wall side
Dfo_2 = 0.012        # Outer head diameter
Dfo_3 = 0.012        # Outer nut diameter

# Thicknesses (m)
t2 = 0.004           # Lug backplate
t3 = 0.003           # Spacecraft wall

# Example material tensile yield strengths (Pa)
sigma_y2 = 270e6
sigma_y3 = 240e6

x = coordinates[:, 0]
z = coordinates[:, 1]

xcg = np.mean(x)             # equal diameters -> area weighting cancels (eq. 4.1)
dx = x - xcg                 # signed distance from CG; Mz varies the load with x


def calculate_axial_loads(Fy, Mz, positions, D2):

    pos = np.asarray(positions, dtype=float)

    nf = len(pos)

    x = pos[:, 0]
    z = pos[:, 1]

    # All fasteners assumed same diameter
    A = np.pi * D2**2 / 4

    # Fastener group CG
    xcg = np.mean(x)
    zcg = np.mean(z)

    dx = x - xcg

    # Direct axial force, equation 4.6
    F_direct = np.full(nf, Fy / nf)

    # Moment contribution (bending about z-axis)
    denominator = np.sum(dx**2)

    if denominator <= 0:
        raise ValueError(
            "Fastener pattern cannot resist Mz"
        )

    F_moment = Mz * dx / denominator

    # Algebraic addition, as required in 4.8
    F_total = F_direct + F_moment

    return F_direct, F_moment, F_total
