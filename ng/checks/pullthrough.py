"""Pullthrough checks
"""
import math
import numpy as np
from design import LugDesign


def run(d: LugDesign):
    #TODO: get all values from d instead of hardcoding

    Fy = d.Fy_n
    Mz = d.Mz_nmm
    load_factor = 1.0

    coordinates = np.array ([
        [-0.1, -0.1],
        [-0.1, 0.1],
        [0.1, -0.1],
        [0.1, 0.1]])
    nf = len(coordinates)

    D2 = d.bolt_diameter_mm * 0.001     # Fastener diameter [m]
    Dfi_2 = 0.006        # Inboard diameter, lug side
    Dfi_3 = 0.006        # Inboard diameter, wall side
    Dfo_2 = 0.012        # Outer head diameter
    Dfo_3 = 0.012        # Outer nut diameter

    # Thicknesses (m)
    t2 = d.lug_thickness_mm * 0.001     # Lug backplate
    t3 = d.wall_thickness_mm * 0.001    # Spacecraft wall

    # Example material tensile yield strengths (Pa)
    sigma_y2 = 270e6
    sigma_y3 = 240e6

    x = coordinates[:, 0]
    z = coordinates[:, 1]

    def calculate_axial_loads(Fy, Mz, x):

        # All fasteners assumed same diameter
        A = np.pi * D2**2 / 4

        # Fastener group CG
        xcg = np.mean(x)
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
        F_total = F_direct + F_moment
        return F_direct, F_moment, F_total

    def pull_through(F_total, Dfi, Dfo, t, sigma_y, load_factor):

        if Dfi <= 0 or Dfo <= Dfi or t <= 0:
            raise ValueError("Invalid geometry")

        # Only tensile loads cause tensile pull-through
        F_tension = np.maximum(F_total, 0)

        # Area under fastener head/nut
        A_contact = np.pi / 4 * (Dfo**2 - Dfi**2)

        # Average normal contact stress
        sigma_normal = F_tension / A_contact

        # Cylindrical shear area
        A_shear = np.pi * Dfi * t

        # Applied shear stress
        tau = load_factor * F_tension / A_shear

        # Shear yield from von Mises
        tau_yield = sigma_y / np.sqrt(3)

        # Margin of safety
        MS = np.full(len(F_total), np.inf)
        loaded = tau > 0
        MS[loaded] = tau_yield / tau[loaded] - 1
        return sigma_normal, tau, MS

    F_direct, F_moment, F_total = calculate_axial_loads(Fy, Mz, x)

    sig2, tau2, MS2 = pull_through(F_total, Dfi_2, Dfo_2, t2, sigma_y2, load_factor)
    sig3, tau3, MS3 = pull_through(F_total, Dfi_3, Dfo_3, t3, sigma_y3, load_factor)

    print("Fastener | F_direct [N] | F_moment [N] | F_total [N] | tau lug [MPa] | tau wall [MPa] | MS lug | MS wall")
    for i in range(len(x)):
        print(f"{i+1:8d} | {F_direct[i]:12.1f} | {F_moment[i]:12.1f} | {F_total[i]:11.1f} | "
            f"{tau2[i]/1e6:13.2f} | {tau3[i]/1e6:14.2f} | {MS2[i]:6.2f} | {MS3[i]:7.2f}")

    print(f"\nMinimum lug MS : {np.min(MS2):.3f}  ->", "PASS" if np.all(MS2 >= 0) else "FAIL")
    print(f"Minimum wall MS: {np.min(MS3):.3f}  ->", "PASS" if np.all(MS3 >= 0) else "FAIL")

    d.set_flag("pullthrough_lug", np.all(MS2 >= 0))
    d.set_flag("pullthrough_wall", np.all(MS3 >= 0))

