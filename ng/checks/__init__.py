"""Each module here exposes run(d: LugDesign) -> None, reads d, writes to d.

Order matters: later checks use intermediates written by earlier ones.
"""
from . import geometry, thermal_loads, bearing, pullthrough, score

CHECKS = [
    geometry.run,       # basic derived geometry (areas, bolt-pattern sums, mass)
    thermal_loads.run,  # thermal bolt loads, consumed by bearing
    bearing.run,        # bearing in lug and wall, bolt shear
    pullthrough.run,    # axial bolt loads, head pull-through, bolt tension
    score.run,          # figure of merit (last)
]
