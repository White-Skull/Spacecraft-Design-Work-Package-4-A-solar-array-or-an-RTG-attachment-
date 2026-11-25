"""Candidate designs defined in python. Must expose CANDIDATES."""
from design import LugDesign

BASE = LugDesign(name="baseline")  # all defaults

CANDIDATES = [
    BASE,
    BASE.variant(name="six_bolts", n_bolts=6),
    BASE.variant(name="thick_plate", lug_thickness_mm=10.0),
    BASE.variant(name="small_bolts", bolt_diameter_mm=4.0, bolt_head_diameter_mm=7.0),
]
