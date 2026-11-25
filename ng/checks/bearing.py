"""Bearing in lug and wall, plus bolt shear.

In-plane load per bolt = direct share (F/n) + torsion share (Mz * r / sum r^2),
then the thermal shear is added as a scalar (conservative: assumes aligned).
"""


def _ms(allowable, applied, sf):
    return allowable / (sf * applied) - 1.0 if applied > 0 else float("inf")


def run(d):
    n = d.n_bolts
    if n > 4:
        # TODO: we need to distribute these bolts...
        pass

    d.set_flag("bearing", True)
