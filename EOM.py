import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import RegularGridInterpolator


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

# =====================================================================
# 1. INPUTS
# =====================================================================
n_lugs = 2            # number of lugs (2 in your sketch)
L      = 0.020        # [m] straight length from hole centre to backplate (from your drawing)
e_D_min = 1.5         # minimum e/D requirement (check your own requirements)

# ---------------- MATERIAL (7075-T7351 plate, room temperature) ----------------
# APPROXIMATE values: replace with MMPDS / course data before using in a report
F_TU  = 480e6   # [Pa] ultimate tensile strength
F_BRU = 740e6   # [Pa] ultimate bearing strength at e/D = 1.5 (matches e_D_min)

# ---------------- FACTORS OF SAFETY ----------------
# Set to the values your requirements specify for each case
FS = {"launch": 1.25, "transfer": 1.25, "in_orbit": 1.25}   # PLACEHOLDERS

# ---------------- LOAD CASES ----------------
# Magnitudes are used (abs) because the capacity formulas take unsigned loads.
# Assumes F_* entries are LIMIT loads in newtons.
load_cases = [
    {"name": "launch",
     "P_axial": abs(F_Launch[0][0])   * FS["launch"],
     "P_trans": abs(F_Launch[1][0])   * FS["launch"],
     "F_tu": F_TU, "F_bru": F_BRU},
    {"name": "transfer",
     "P_axial": abs(F_Transfer[0][0]) * FS["transfer"],
     "P_trans": abs(F_Transfer[1][0]) * FS["transfer"],
     "F_tu": F_TU, "F_bru": F_BRU},
    {"name": "in_orbit",
     "P_axial": abs(F_Mpo[0][0])      * FS["in_orbit"],
     "P_trans": abs(F_Mpo[1][0])      * FS["in_orbit"],
     "F_tu": F_TU, "F_bru": F_BRU},   # reduce if the in-orbit temperature is extreme
]
# =====================================================================
# 2. BRUHN CHART DATA (digitise from your edition of Bruhn, lug analysis)
# =====================================================================
# These MUST be filled in before running; the "..." placeholders will crash.
# Axial chart:      K_bru as a function of e/D and D/t
# Transverse chart: K_tu  as a function of e/D and t/D
eD_ax = np.array([...])          # TODO: e/D grid points (ascending)
Dt_ax = np.array([...])          # TODO: D/t grid points (ascending)
K_bru_table = np.array([[...]])  # TODO: shape (len(eD_ax), len(Dt_ax))

eD_tr = np.array([...])          # TODO
tD_tr = np.array([...])          # TODO
K_tu_table = np.array([[...]])   # TODO: shape (len(eD_tr), len(tD_tr))

# NET TENSION: K_t(W/D) for YOUR material group's curve
WD_t   = np.array([1.0, 1.5, 2.0, 3.0, 4.0])   # x-axis of chart (dummy grid)
K_t_vals = np.array([1.0,0.88, 0.7, 0.48, 0.28]) # REPLACE with values read from the chart

K_t_f = lambda r: np.interp(r, WD_t, K_t_vals)
K_bru_f = RegularGridInterpolator((eD_ax, Dt_ax), K_bru_table, bounds_error=True)
K_tu_f  = RegularGridInterpolator((eD_tr, tD_tr), K_tu_table,  bounds_error=True)

# =====================================================================
# 3. MODEL
# =====================================================================
def volume(x):
    """Total lug volume [m^3]. Mass = density * volume (density is constant)."""
    w, D, t = x
    return n_lugs * t * (np.pi * (w/2)**2 / 2 + w * L - np.pi * D**2 / 4)

def margins_case(x, lc):
    w, D, t = x
    e = w / 2
    A_br = D * t
    A_t  = (w - D) * t

    P_bru = K_bru_f([[e/D, D/t]])[0] * lc["F_tu"] * A_br   # shear-out/bearing
    P_t   = K_t_f(w/D) * lc["F_tu"] * A_t                  # net-section tension
    Pu_ax = min(P_bru, P_t)                                # governing axial capacity

    Pu_tr = K_tu_f(A_av(w, D, t) / A_br) * lc["F_tu"] * A_br

    Ra, Rtr = lc["P_axial"]/Pu_ax, lc["P_trans"]/Pu_tr
    MS_int = 1.0/(Ra**1.6 + Rtr**1.6)**0.625 - 1.0

    P_res  = np.hypot(lc["P_axial"], lc["P_trans"])
    MS_brg = lc["F_bru"]*A_br/P_res - 1.0
    MS_t   = P_t/lc["P_axial"] - 1.0                       # explicit net-tension margin
    return [MS_int, MS_brg, MS_t]

def margins(x):
    """All constraints stacked in one vector; every entry must be >= 0."""
    w, D, t = x
    try:
        out = []
        for lc in load_cases:
            out += margins_case(x, lc)
        out.append(w / 2 / D - e_D_min)                    # geometry constraint
        return np.array(out)
    except ValueError:
        # Outside the digitised chart range: treat as infeasible
        return -np.ones(2 * len(load_cases) + 1)

# =====================================================================
# 4. OPTIMISATION (one run, all load cases at once)
# =====================================================================
x0     = np.array([0.030, 0.010, 0.005])                    # initial guess [w, D1, t1] in m
bounds = [(0.015, 0.060), (0.005, 0.020), (0.002, 0.015)]   # keep inside chart ranges!

res = minimize(volume, x0, method="SLSQP", bounds=bounds,
               constraints=[{"type": "ineq", "fun": margins}],
               options={"ftol": 1e-10, "maxiter": 500})

# =====================================================================
# 5. RESULTS
# =====================================================================
w, D1, t1 = res.x
print(res.message)
print(f"w  = {w*1e3:.2f} mm")
print(f"D1 = {D1*1e3:.2f} mm")
print(f"t1 = {t1*1e3:.2f} mm")
print(f"Volume = {volume(res.x)*1e9:.1f} mm^3")
print(f"e/D = {w/2/D1:.2f}\n")

for lc in load_cases:
    ms = margins_case(res.x, lc)
    print(f"{lc['name']:9s} MS_interaction = {ms[0]:.3f}   MS_bearing = {ms[1]:.3f}")
# The case with a margin close to 0 is the sizing (critical) case.
