"""Figure of merit: a higher score is better

Only meaningful for designs where every flag passed.
"""

from design import LugDesign


def run(d: LugDesign):
    d.score = 57
