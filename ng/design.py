"""The single data blob passed through every check.

Units: mm, N, MPa, N*mm, degC, 1/K, g/cm^3.

Fields are tagged with metadata kind = "input" | "intermediate" | "output"
so that loaders (CSV) and reports can tell them apart. Order in the class:
inputs first, then intermediates, then outputs last.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field, fields


def _f(kind, default=0.0, unit="", factory=None):
    md = {"kind": kind, "unit": unit}
    if factory is not None:
        return field(default_factory=factory, metadata=md)
    return field(default=default, metadata=md)


def _in(default=0.0, unit="", factory=None):
    return _f("input", default, unit, factory)


def _mid(default=0.0, unit="", factory=None):
    return _f("intermediate", default, unit, factory)


def _out(default=0.0, unit="", factory=None):
    return _f("output", default, unit, factory)


@dataclass
class LugDesign:
    name: str = _in("baseline")

    # ------------------------------------------------------------------
    # INPUTS: lug / backing plate
    # ------------------------------------------------------------------
    lug_material: str = _in("Al 7075-T73")
    lug_E_mpa: float = _in(71_700.0, "MPa")
    lug_cte: float = _in(23.4e-6, "1/K")
    lug_yield_mpa: float = _in(435.0, "MPa")
    lug_thickness_mm: float = _in(6.0, "mm")
    plate_width_mm: float = _in(100.0, "mm")    # backing plate, x direction
    plate_height_mm: float = _in(100.0, "mm")   # backing plate, y direction

    # INPUTS: fixtures (bolts)
    bolt_material: str = _in("A286")
    bolt_E_mpa: float = _in(201_000.0, "MPa")
    bolt_cte: float = _in(16.5e-6, "1/K")
    bolt_yield_mpa: float = _in(590.0, "MPa")
    bolt_diameter_mm: float = _in(6.0, "mm")
    bolt_head_diameter_mm: float = _in(10.0, "mm")
    n_bolts: int = _mid(0)

    # INPUTS: spacecraft wall (not part of the design, but lives here)
    wall_material: str = _in("Al 6061-T6 facesheet")
    wall_E_mpa: float = _in(68_900.0, "MPa")
    wall_cte: float = _in(23.6e-6, "1/K")
    wall_yield_mpa: float = _in(240.0, "MPa")
    wall_thickness_mm: float = _in(10.0, "mm")

    # INPUTS: loads, environment, policy (applied at plate centre)
    Fx_n: float = _in(800.0, "N")      # in-plane
    Fy_n: float = _in(1000.0, "N")     # normal to wall (positive = pull-off)
    Fz_n: float = _in(1500.0, "N")     # in-plane
    Mx_nmm: float = _in(20_000.0, "N*mm")  # bending about x (out of plane)
    My_nmm: float = _in(15_000.0, "N*mm")  # bending about y (out of plane)
    Mz_nmm: float = _in(10_000.0, "N*mm")  # torsion (in plane)
    ####################
    temp_min_c: float = _in(-120.0, "degC")
    temp_max_c: float = _in(110.0, "degC")
    temp_assembly_c: float = _in(15.0, "degC")
    # safety_factor: float = _in(1.5)

    # ------------------------------------------------------------------
    # INTERMEDIATE VALUES (filled in by the checks)
    # ------------------------------------------------------------------
    bolt_area_tensile_mm2: float = _mid(0.0, "mm2")   # TODO effective area for axial stress checks
    lug_mass_g: float = _mid(0.0, "g")      # TODO - can be used for scoring

    # ------------------------------------------------------------------
    # OUTPUTS (last)
    # ------------------------------------------------------------------
    # pure numbers: margins of safety, MS = allowable / (SF * applied) - 1
    # ms_bearing_lug: float = _out(0.0)
    # ms_bearing_wall: float = _out(0.0)
    # min_ms: float = _out(0.0)
    # pass/fail flags: any False -> design is rejected
    flags: dict = _out(factory=dict)
    # single figure of merit (higher is better)
    score: float = _out(0.0)

    # ------------------------------------------------------------------
    def set_flag(self, name: str, ok: bool) -> None:
        self.flags[name] = bool(ok)

    @property
    def passed(self) -> bool:
        return bool(self.flags) and all(self.flags.values())

    @property
    def failed_flags(self) -> list:
        return [k for k, v in self.flags.items() if not v]

    def variant(self, **changes) -> "LugDesign":
        """Independent copy with some inputs changed."""
        names = {f.name for f in fields(self)}
        bad = set(changes) - names
        if bad:
            raise KeyError(f"unknown field(s): {sorted(bad)}")
        d = copy.deepcopy(self)
        for k, v in changes.items():
            setattr(d, k, v)
        return d

    def report(self) -> str:
        lines = []
        for kind in ("input", "intermediate", "output"):
            lines.append(f"--- {kind.upper()} ---")
            for f in fields(self):
                if f.metadata["kind"] != kind:
                    continue
                v = getattr(self, f.name)
                if isinstance(v, float):
                    v = f"{v:.4g}"
                elif isinstance(v, list):
                    v = "[" + ", ".join(
                        f"{x:.4g}" if isinstance(x, float) else str(x) for x in v) + "]"
                unit = f.metadata["unit"]
                lines.append(f"  {f.name:24s} = {v} {unit}")
        return "\n".join(lines)
