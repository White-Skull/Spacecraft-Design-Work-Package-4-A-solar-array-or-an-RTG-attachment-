"""
AE2111-I WP4 - Task 4.3: Design of the lugs
===========================================

Method: Bruhn, "Analysis and Design of Flight Vehicle Structures", section D1.13
(lugs under oblique loads), using the axial (D1.12) and transverse (D1.15) lug data.

  1. Loads from 4.1  ->  in-plane load P per flange and its angle alpha
  2. P is split into an axial part (along the lug, y) and a transverse part (in the
     lug plane, perpendicular to y)
  3. Axial allowable      = min(net-section, shear-bearing)    Figs D1.12, D1.13/D1.14
     Transverse allowable = K * A_br * F                        Fig  D1.15
  4. Interaction:  MS = 1 / (Ra^1.6 + Rtr^1.6)^0.625 - 1  >= 0          Eq. (13)
  5. Extra checks: out-of-plane / root bending of the flange (brief), pin shear
  6. Grid sweep over D1, t1, e/D (w = 2e) for every material -> lightest design

Two versions of step 3/4 are evaluated:
  * YIELD   (what the brief asks for): F_ty, K_bry (Fig D1.14), K_ty (curve 3 of D1.15),
            net section with K_t * F_ty           -> loads x FOS_Y x FITTING
  * ULTIMATE (Bruhn as written):       F_tu, K_br (Fig D1.13), K_tu (material curve),
            net section with K_t * F_tu           -> loads x FOS_U x FITTING

Coordinate system (same as your 4.1 script):
  x = launch-vehicle axis (up +), y = solar-panel axis (outward +, normal to the wall),
  z = lateral.  The lug's axial direction is y.  The pin / hinge runs along HINGE_AXIS
  (x or z); the remaining axis is the in-plane transverse direction.

ASSUMPTIONS (quote these IDs in the report, with result / validity / conservatism)
  A1  The panel is attached by N_FLANGES = 2 flanges whose centre-planes are D_COUPLE
      apart along the hinge axis. Forces are shared equally; the moment about the axis
      perpendicular to the hinge and to y is reacted as a force couple (F1 = M / d).
  A2  The moment about the hinge axis itself is carried by the attachment (brief, 4.1).
  A3  Load components are taken as absolute values, so both load directions are
      covered (envelope). Compressive axial load is treated like tension (conservative).
  A4  Launch quasi-static loads already include gravity, so the pre-launch (1 g) case
      is NOT added to the dynamic launch case.
  A5  Round-ended lug with a concentric hole: e = w/2, so W/D = 2 e/D.
  A6  A_av: all four sections A1..A4 are set to the smallest radial section
      t(w-D)/2, so A_av = t(w-D)/2 (conservative: lowers A_av and K_tu/K_ty).
  A7  Yield version of the net-section check uses K_t * F_ty (Bruhn gives F_tu only).
  A8  Lugs are machined flat from plate (lug thickness = plate thickness, short-
      transverse grain through the thickness), so cut-off curves A/B of Fig D1.13 do
      not apply; Note 3 (K_br <= 2.0) applies for aluminium plate >= 0.5 in thick.
  A9  Out-of-plane load is at least 10 % of P (brief). Root of the flange is checked
      as a cantilever under combined axial + in-plane + out-of-plane bending.
  A10 Pin is in double shear (double lug with the panel fitting in between).
  A11 Bruhn chart values were digitised from the scanned appendix (accuracy roughly
      +/- 0.02-0.03). In Fig D1.12 the curves 2/3 overlap beyond W/D = 3.6; curve 2 is
      taken as the lower of the two branches (conservative).
  A12 Room-temperature allowables (Bruhn charts are RT only). Set strength_factor per
      load case to F(T)/F(RT) for hot in-orbit cases at Mercury.
  A13 Distance from hole centre to the backplate is L = max(L_ROOT_MIN, e), so there is
      at least as much material below the hole as above it.
  A14 The brief only requires the 10 % P out-of-plane load when Fx/Fz = 0; here the
      larger of the actual load and 10 % P is used (covers misalignment, conservative).
"""

import numpy as np
from scipy.interpolate import RegularGridInterpolator

# =============================================================================
# 1. INPUTS
# =============================================================================

# --- Loads from 4.1 (limit loads, N and N*m), frame: [x, y, z] ----------------
F_prelaunch = np.array([-382.165, 0.0, 0.0])
F_dynamiclaunch = np.array([2295.54, 688.67, 688.67])
F_transferburn = np.array([0.29, 0.0, 0.0])
F_micrometeoroid = np.array([0.0, 0.0, 23.0])
F_actuation = np.array([7.46, 0.0, 3.71])

M_prelaunch = np.array([0.0, 0.0, 707.3])
M_dynamiclaunch = np.array([1274.02, 0.0, -4246.75])
M_transferburn = np.array([0.0, 0.0, -0.5365])
M_micrometeoroid = np.array([44.75, 42.55, 0.0])
M_actuation = np.array([9.72, 11.15, 41.26])

INCLUDE_PRELAUNCH_IN_LAUNCH = False   # A4: QSL factors normally already include 1 g

LOAD_CASES = [
    # strength_factor = F(T)/F(RT) for that phase (A12); 1.0 = room temperature
    {"name": "launch",
     "F": F_dynamiclaunch + (F_prelaunch if INCLUDE_PRELAUNCH_IN_LAUNCH else 0),
     "M": M_dynamiclaunch + (M_prelaunch if INCLUDE_PRELAUNCH_IN_LAUNCH else 0),
     "strength_factor": 1.0},
    {"name": "transfer",
     "F": F_transferburn + F_micrometeoroid + F_actuation,
     "M": M_transferburn + M_micrometeoroid + M_actuation,
     "strength_factor": 1.0},
    {"name": "in-orbit",
     "F": F_micrometeoroid + F_actuation,
     "M": M_micrometeoroid + M_actuation,
     "strength_factor": 1.0},   # TODO: knock-down for Mercury orbit temperature
]

# --- Attachment configuration (from 4.2) ----------------------------------------
HINGE_AXIS = "x"      # axis of the pin / hinge: "x" or "z"  <-- CHECK against your 4.2
N_FLANGES = 2         # flanges sharing the load (double lug = 2)
D_COUPLE = 0.10       # [m] distance between the flanges' centre-planes (couple arm) <-- your h + t
L_ROOT_MIN = 0.020    # [m] hole centre to backplate (from your drawing); A13 uses max(L, e)

# --- Safety factors -----------------------------------------------------------------
# ECSS-E-ST-32-10 (metallic parts, verification by analysis only): FOSY 1.25, FOSU 2.0.
# If the structure is qualified by test: FOSY 1.1, FOSU 1.25. Verify against the standard.
FOS_Y = 1.25
FOS_U = 2.0
FITTING = 1.15        # fitting factor (Bruhn notes: extra M.S. of 0.15 for fittings)
CHECK_ULTIMATE = True  # also require the ultimate Bruhn check (recommended)

# --- Design space (grid sweep) --------------------------------------------------------
D_RANGE = np.arange(3.0, 40.01, 0.5) * 1e-3     # pin / hole diameter D1 [m]
T_RANGE = np.arange(1.0, 25.41, 0.25) * 1e-3    # flange thickness t1 [m] (<= 1 in, chart limit)
ED_RANGE = np.arange(0.60, 2.501, 0.02)          # e/D  (W/D = 2 e/D <= 5, chart limit)
E_D_MIN = 1.5         # minimum e/D you require (your earlier script used 1.5); Bruhn allows 0.5

# --- Materials ------------------------------------------------------------------------
# Typical room-temperature values (ASM/MatWeb). Replace with MMPDS A/B-basis values if
# your course requires design allowables.
# kt_curve / ktu_curve: list of (max plate thickness [m], Bruhn curve id) from
# Table D1.3 (Fig D1.12) and Table D1.4 (Fig D1.15). None = no curve available.
INCH = 25.4e-3
MATERIALS = {
    "Al 7075-T6 plate": dict(rho=2810, Fty=503e6, Ftu=572e6, aluminium=True,
                             kt_curve=[(0.5*INCH, "1"), (1.0*INCH, "2")],
                             ktu_curve=[(0.5*INCH, "8"), (1.0*INCH, "11")]),
    "Al 2014-T6 plate": dict(rho=2800, Fty=414e6, Ftu=483e6, aluminium=True,
                             kt_curve=[(0.5*INCH, "1"), (1.0*INCH, "2")],
                             ktu_curve=[(0.5*INCH, "8"), (1.0*INCH, "11")]),
    "Al 2024-T3 plate": dict(rho=2780, Fty=345e6, Ftu=483e6, aluminium=True,
                             kt_curve=[(1.0*INCH, "4")],
                             ktu_curve=[(0.5*INCH, "6"), (1.0*INCH, "9")]),
    "Steel 4130 (normalised)": dict(rho=7850, Fty=435e6, Ftu=670e6, aluminium=False,
                                    kt_curve=[(1.0*INCH, "1")],
                                    ktu_curve=[(1.0*INCH, "1")]),
}

# Pin material (Ti-6Al-4V annealed, typical)
PIN = dict(name="Ti-6Al-4V", Fty=880e6, Fsu=550e6)

# =============================================================================
# 2. BRUHN CHART DATA (digitised from the WP4 appendix, see A11)
# =============================================================================

# Fig D1.12 - K_t (axial, net section) vs W/D
KT_WD = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
KT = {
    "1": np.array([1.00, 0.99, 0.97, 0.95, 0.93, 0.912, 0.89, 0.85, 0.77]),
    "2": np.array([1.00, 0.98, 0.947, 0.909, 0.87, 0.845, 0.80, 0.71, 0.69]),
    "4": np.array([1.00, 0.955, 0.90, 0.848, 0.80, 0.765, 0.73, 0.71, 0.69]),
}

# Fig D1.13 - K_br (axial, shear-bearing, ULTIMATE) vs e/D for D/t curves
KBR_ED = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4,
                   2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0])
_E = [0, .19, .37, .54, .69, .83, .96, 1.08, 1.31, 1.50, 1.68, 1.84, 1.99, 2.12]  # common envelope to e/D=2.4
KBR_DT = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30])
KBR_TABLE = np.array([
    _E + [2.25, 2.38, 2.49, 2.60, 2.71, 2.75, 2.75, 2.75],                                   # D/t <= 2
    _E + [2.25, 2.33, 2.41, 2.49, 2.57, 2.63, 2.70, 2.75],                                   # 3
    _E[:11] + [1.82, 1.94, 2.03, 2.11, 2.19, 2.26, 2.32, 2.38, 2.44, 2.48, 2.53],           # 4
    _E[:10] + [1.67, 1.77, 1.86, 1.94, 2.00, 2.06, 2.11, 2.16, 2.20, 2.23, 2.26, 2.29],     # 5
    _E[:9] + [1.45, 1.57, 1.67, 1.75, 1.82, 1.87, 1.92, 1.95, 1.98, 2.00, 2.03, 2.04, 2.05],  # 6
    _E[:8] + [1.27, 1.39, 1.49, 1.56, 1.62, 1.67, 1.70, 1.73, 1.75, 1.76, 1.77, 1.78, 1.78, 1.78],  # 7
    _E[:7] + [1.05, 1.19, 1.29, 1.37, 1.43, 1.47, 1.50, 1.52, 1.53] + [1.54]*6,             # 8
    _E[:6] + [0.94, 1.01, 1.12, 1.20, 1.27, 1.32, 1.36, 1.38] + [1.39]*8,                   # 9
    _E[:6] + [0.91, 0.96, 1.04, 1.11, 1.17, 1.20, 1.23, 1.245] + [1.245]*8,                 # 10
    [0, .18, .34, .42, .50, .56, .61, .65, .71, .76, .79, .81, .81, .81] + [.81]*3 + [.82]*5,   # 15
    [0, .15, .24, .30, .36, .40, .44, .47, .53, .57, .59, .60, .61, .60] + [.60]*8,          # 20
    [0, .11, .18, .22, .27, .31, .35, .37, .41, .44, .46, .46, .47, .47] + [.46]*8,          # 25
    [0, .07, .13, .18, .22, .26, .29, .31, .34, .36, .37, .38, .38, .38] + [.38]*8,          # 30
])

# Fig D1.14 - K_bry (axial, shear-bearing, YIELD) vs e/D for t/D curves
KBRY_ED = np.array([0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.5,
                    3.0, 3.5, 4.0])
KBRY_TD = np.array([0.06, 0.08, 0.10, 0.12, 0.15, 0.20, 0.30, 0.40, 0.60])
KBRY_TABLE = np.array([
    [0, .22, .40, .55, .61, .67, .72, .76, .83, .885, .92, .945, .962, .979, .993, 1.0, 1.0],
    [0, .22, .406, .59, .68, .76, .82, .866, .946, 1.008, 1.055, 1.086, 1.105, 1.123, 1.139, 1.146, 1.147],
    [0, .22, .406, .60, .70, .80, .90, .94, 1.031, 1.095, 1.143, 1.176, 1.194, 1.223, 1.249, 1.26, 1.26],
    [0, .22, .406, .60, .70, .807, .90, .955, 1.071, 1.141, 1.196, 1.232, 1.257, 1.287, 1.315, 1.33, 1.331],
    [0, .22, .406, .60, .70, .81, .91, .977, 1.139, 1.218, 1.276, 1.315, 1.343, 1.373, 1.406, 1.42, 1.426],
    [0, .22, .406, .60, .70, .83, .95, 1.03, 1.209, 1.30, 1.365, 1.414, 1.444, 1.476, 1.509, 1.524, 1.527],
    [0, .22, .406, .60, .702, .842, .962, 1.052, 1.259, 1.373, 1.449, 1.507, 1.551, 1.594, 1.631, 1.649, 1.654],
    [0, .22, .406, .60, .702, .842, .962, 1.052, 1.259, 1.40, 1.49, 1.554, 1.599, 1.653, 1.692, 1.713, 1.717],
    [0, .22, .406, .60, .702, .842, .962, 1.052, 1.259, 1.401, 1.501, 1.58, 1.633, 1.688, 1.736, 1.761, 1.775],
])

# Fig D1.15 - K_tu (transverse, ULTIMATE) and K_ty (curve 3, YIELD) vs A_av/A_br
KTU_X = np.round(np.arange(0.0, 1.401, 0.1), 2)
KTU = {
    "1": np.array([0, .135, .292, .436, .571, .705, .832, .956, 1.07, 1.19, 1.298, 1.406, 1.506, 1.602, 1.683]),
    "3": np.array([0, .135, .26, .392, .51, .635, .74, .828, .91, .988, 1.059, 1.127, 1.194, 1.255, 1.305]),
    "6": np.array([0, .135, .25, .38, .50, .585, .669, .756, .835, .907, .971, 1.028, 1.075, 1.11, 1.135]),
    "8": np.array([0, .135, .248, .364, .465, .57, .619, .657, .667, .68, .689, .696, .70, .70, .70]),
    "9": np.array([0, .135, .248, .36, .414, .455, .502, .539, .57, .594, .605, .62, .63, .636, .638]),
    "10": np.array([0, 0, .014, .037, .067, .102, .144, .199, .259, .33, .411, .51, .607, .709, .812]),
    "11": np.array([0, .135, .248, .345, .40, .44, .474, .49, .503, .512, .516, .522, .528, .53, .531]),
}

_kbr = RegularGridInterpolator((KBR_DT, KBR_ED), KBR_TABLE)
_kbry = RegularGridInterpolator((KBRY_TD, KBRY_ED), KBRY_TABLE)


def k_t(curve, WD):
    return np.interp(WD, KT_WD, KT[curve])


def k_br(eD, Dt):
    # curve "<= 2" is used for D/t < 2; D/t > 30 is outside the chart (masked elsewhere)
    pts = np.stack([np.clip(Dt, 2, 30), np.clip(eD, 0.5, 4.0)], axis=-1)
    return _kbr(pts)


def k_bry(eD, tD):
    # "0.6 and higher t/D" curve for t/D > 0.6; t/D < 0.06 is masked elsewhere
    pts = np.stack([np.clip(tD, 0.06, 0.6), np.clip(eD, 0.5, 4.0)], axis=-1)
    return _kbry(pts)


def k_tu(curve, X):
    # curves rise monotonically, so holding the value at 1.4 beyond the chart is conservative
    return np.interp(np.clip(X, 0, 1.4), KTU_X, KTU[curve])


def by_thickness(table, t, func, *args):
    """Pick the Bruhn curve per plate thickness (table = [(t_max, curve), ...])."""
    out = np.full(t.shape, np.nan)
    t_lo = 0.0
    for t_max, curve in table:
        sel = (t > t_lo) & (t <= t_max + 1e-12)
        if curve is not None and sel.any():
            out[sel] = func(curve, *[a[sel] for a in args])
        t_lo = t_max
    return out  # NaN where no curve exists -> infeasible


# =============================================================================
# 3. LOADS PER FLANGE
# =============================================================================
AX = {"x": 0, "y": 1, "z": 2}


def flange_loads(F, M, hinge=HINGE_AXIS, n=N_FLANGES, d=D_COUPLE):
    """Limit loads on the most loaded flange: axial (y), in-plane transverse, out-of-plane."""
    h = AX[hinge]
    q = AX["z"] if hinge == "x" else AX["x"]       # in-plane transverse axis
    P_ax = abs(F[1]) / n + abs(M[q]) / d             # force + couple from moment about q  (A1)
    P_tr = abs(F[q]) / n + abs(M[1]) / d             # force + couple from torsion about y
    P_oop = abs(F[h]) / n                            # along the pin -> flange bending
    P = np.hypot(P_ax, P_tr)
    P_oop = max(P_oop, 0.1 * P)                      # A14 / brief: at least 10 % of P
    alpha = np.degrees(np.arctan2(P_tr, P_ax))       # angle of P from the lug (y) axis
    return dict(P_ax=P_ax, P_tr=P_tr, P_oop=P_oop, P=P, alpha=alpha, M_hinge=M[h])


# =============================================================================
# 4. LUG CHECKS (vectorised over the design grid)
# =============================================================================
def interaction_ms(Ra, Rtr):
    with np.errstate(divide="ignore", invalid="ignore"):
        return 1.0 / (Ra**1.6 + Rtr**1.6) ** 0.625 - 1.0


def evaluate(mat, D, t, eD, cases):
    """Return mass and all margins of safety for arrays of D, t, e/D."""
    e = eD * D
    w = 2 * e                                  # A5
    L = np.maximum(L_ROOT_MIN, e)              # A13
    A_br = D * t
    A_t = (w - D) * t
    X = (w - D) / (2 * D)                      # A_av / A_br with A6
    WD, tD, Dt = w / D, t / D, D / t

    valid = (tD >= 0.06) & (Dt <= 30) & (WD <= 5.0) & (WD >= 1.0) & (eD >= E_D_MIN - 1e-9)

    # --- efficiency factors ---
    Kt = by_thickness(mat["kt_curve"], t, k_t, WD)
    Kbry = k_bry(eD, tD)
    Kty = k_tu("3", X)
    Kbr = k_br(eD, Dt)
    if mat["aluminium"]:
        Kbr = np.where(t >= 0.5 * INCH, np.minimum(Kbr, 2.0), Kbr)   # Fig D1.13 note 3
    Ktu = by_thickness(mat["ktu_curve"], t, k_tu, X)
    valid &= ~np.isnan(Kt) & ~np.isnan(Ktu)

    res = {"w": w, "L": L, "valid": valid,
           "mass": N_FLANGES * mat["rho"] * t * (w * L + np.pi * w**2 / 8 - np.pi * D**2 / 4)}
    ms = {k: np.full(D.shape, np.inf) for k in
          ("lug_yield", "lug_ult", "root_bending", "pin_yield", "pin_ult")}

    for lc in cases:
        fl = lc["flange"]
        sf = lc["strength_factor"]
        Fty, Ftu = mat["Fty"] * sf, mat["Ftu"] * sf

        # ----- YIELD (brief) -----
        ky = FOS_Y * FITTING
        Pax_allow_y = np.minimum(Kt * Fty * A_t, Kbry * Fty * A_br)      # Eq 6 (A7) & Eq 8
        Ptr_allow_y = Kty * Fty * A_br                                   # Eq 11, curve 3
        ms["lug_yield"] = np.minimum(ms["lug_yield"], interaction_ms(
            ky * fl["P_ax"] / Pax_allow_y, ky * fl["P_tr"] / Ptr_allow_y))

        # root of the flange: axial + in-plane bending + out-of-plane bending (A9)
        sigma = ky * (fl["P_ax"] / (w * t)
                      + 6 * fl["P_tr"] * L / (t * w**2)
                      + 6 * fl["P_oop"] * L / (w * t**2))
        ms["root_bending"] = np.minimum(ms["root_bending"], Fty / sigma - 1)

        # pin, double shear (A10): each shear plane carries one flange load
        tau_y = ky * fl["P"] / (np.pi * D**2 / 4)
        ms["pin_yield"] = np.minimum(ms["pin_yield"], 0.577 * PIN["Fty"] / tau_y - 1)

        # ----- ULTIMATE (Bruhn as written) -----
        ku = FOS_U * FITTING
        Pax_allow_u = np.minimum(Kt * Ftu * A_t, Kbr * Ftu * A_br)       # Eq 6 & Eq 7
        Ptr_allow_u = Ktu * Ftu * A_br                                   # Eq 10
        ms["lug_ult"] = np.minimum(ms["lug_ult"], interaction_ms(
            ku * fl["P_ax"] / Pax_allow_u, ku * fl["P_tr"] / Ptr_allow_u))
        tau_u = ku * fl["P"] / (np.pi * D**2 / 4)
        ms["pin_ult"] = np.minimum(ms["pin_ult"], PIN["Fsu"] / tau_u - 1)

    res["ms"] = ms
    res["below_curve10"] = Ktu < k_tu("10", X)   # Fig D1.15 note: check as cantilever
    res["factors"] = dict(Kt=Kt, Kbry=Kbry, Kty=Kty, Kbr=Kbr, Ktu=Ktu, X=X)
    return res


# =============================================================================
# 5. SWEEP AND REPORT
# =============================================================================
def run(verbose=True):
    cases = []
    for lc in LOAD_CASES:
        cases.append(dict(lc, flange=flange_loads(lc["F"], lc["M"])))

    if verbose:
        print("=" * 78)
        print(f"Hinge axis: {HINGE_AXIS}   flanges: {N_FLANGES}   couple arm d = {D_COUPLE*1e3:.0f} mm")
        print(f"FOS_Y = {FOS_Y}, FOS_U = {FOS_U}, fitting factor = {FITTING}")
        print("Limit loads on the most loaded flange:")
        print(f"  {'case':10s}{'P_ax [N]':>11s}{'P_tr [N]':>11s}{'P [N]':>11s}"
              f"{'alpha [deg]':>13s}{'P_oop [N]':>11s}{'M_hinge [Nm]':>14s}")
        for lc in cases:
            f = lc["flange"]
            print(f"  {lc['name']:10s}{f['P_ax']:11.1f}{f['P_tr']:11.1f}{f['P']:11.1f}"
                  f"{f['alpha']:13.1f}{f['P_oop']:11.1f}{f['M_hinge']:14.1f}")

    Dg, tg, eg = np.meshgrid(D_RANGE, T_RANGE, ED_RANGE, indexing="ij")
    Dg, tg, eg = Dg.ravel(), tg.ravel(), eg.ravel()

    results = {}
    for name, mat in MATERIALS.items():
        r = evaluate(mat, Dg, tg, eg, cases)
        checks = ["lug_yield", "root_bending", "pin_yield"]
        if CHECK_ULTIMATE:
            checks += ["lug_ult", "pin_ult"]
        ok = r["valid"].copy()
        for c in checks:
            ok &= r["ms"][c] >= 0
        if not ok.any():
            results[name] = None
            continue
        i = np.flatnonzero(ok)[np.argmin(r["mass"][ok])]
        results[name] = dict(
            D=Dg[i], t=tg[i], eD=eg[i], w=r["w"][i], L=r["L"][i], mass=r["mass"][i],
            ms={k: v[i] for k, v in r["ms"].items()},
            factors={k: v[i] for k, v in r["factors"].items()},
            below_curve10=bool(r["below_curve10"][i]))

    if verbose:
        print("\nLightest feasible design per material (all margins >= 0):")
        hdr = (f"  {'material':25s}{'D1':>7s}{'t1':>7s}{'w':>7s}{'e/D':>6s}{'L':>6s}"
               f"{'mass':>8s}  {'MS: lug_y':>9s}{'lug_u':>7s}{'root':>7s}{'pin_y':>7s}{'pin_u':>7s}")
        print(hdr)
        print(f"  {'':25s}{'[mm]':>7s}{'[mm]':>7s}{'[mm]':>7s}{'':>6s}{'[mm]':>6s}{'[g]':>8s}")
        for name, d in results.items():
            if d is None:
                print(f"  {name:25s}  no feasible design in the grid")
                continue
            m = d["ms"]
            print(f"  {name:25s}{d['D']*1e3:7.1f}{d['t']*1e3:7.2f}{d['w']*1e3:7.1f}{d['eD']:6.2f}"
                  f"{d['L']*1e3:6.1f}{d['mass']*1e3:8.1f}  {m['lug_yield']:9.2f}{m['lug_ult']:7.2f}"
                  f"{m['root_bending']:7.2f}{m['pin_yield']:7.2f}{m['pin_ult']:7.2f}"
                  + ("   (K_tu below curve 10)" if d["below_curve10"] else ""))
        feas = {k: v for k, v in results.items() if v is not None}
        if feas:
            best = min(feas, key=lambda k: feas[k]["mass"])
            d = feas[best]
            f = d["factors"]
            print(f"\nLightest overall: {best}")
            print(f"  D1 = {d['D']*1e3:.1f} mm, t1 = {d['t']*1e3:.2f} mm, w = {d['w']*1e3:.1f} mm, "
                  f"mass of {N_FLANGES} flanges = {d['mass']*1e3:.1f} g")
            print(f"  Chart factors: K_t = {f['Kt']:.3f}, K_bry = {f['Kbry']:.3f}, K_ty = {f['Kty']:.3f}, "
                  f"K_br = {f['Kbr']:.3f}, K_tu = {f['Ktu']:.3f}, A_av/A_br = {f['X']:.2f}")
    return cases, results


if __name__ == "__main__":
    run()
