#!/usr/bin/env python3
"""Solar-panel lug design selector.

  python main.py                       # single design (first in candidates.py), full report
  python main.py --name thick_plate    # single named design
  python main.py --all                 # every design in candidates.py, pick the best
  python main.py --all --csv candidates.csv     # same, but values come from CSV
  python main.py --py my_candidates.py --all    # alternative python file
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from checks import CHECKS          # noqa: E402
from loaders import load_csv, load_python  # noqa: E402


def evaluate(d):
    for check in CHECKS:
        check(d)
    return d


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--csv", metavar="FILE", help="read candidates from a CSV file")
    src.add_argument("--py", metavar="FILE", help="read candidates from a python file (default: candidates.py)")
    ap.add_argument("--all", action="store_true", help="evaluate every candidate (default: only one)")
    ap.add_argument("--name", help="single mode: pick the candidate with this name")
    ap.add_argument("-v", "--verbose", action="store_true", help="print the full report for every design")
    args = ap.parse_args(argv)

    designs = load_csv(args.csv) if args.csv else load_python(args.py)
    if not designs:
        ap.error("no candidates found")

    if not args.all:
        if args.name:
            matches = [d for d in designs if d.name == args.name]
            if not matches:
                ap.error(f"no candidate named {args.name!r}; have {[d.name for d in designs]}")
            designs = matches[:1]
        else:
            designs = designs[:1]

    single = len(designs) == 1
    for d in designs:
        evaluate(d)
        if single or args.verbose:
            print(f"===== {d.name} =====")
            print(d.report())
            print()

    print(f"{'name':26s}{'mass_g':>9s}{'score':>9s}  status")
    for d in designs:
        status = "PASS" if d.passed else "FAIL: " + ", ".join(d.failed_flags)
        print(f"{d.name:26s}{d.lug_mass_g:9.1f}{d.score:9.2f}  {status}")

    passing = [d for d in designs if d.passed]
    if not single:
        if passing:
            best = max(passing, key=lambda d: d.score)
            print(f"\nBest design: {best.name} (score {best.score:.2f})")
        else:
            print("\nNo design passed all checks.")
    return 0 if passing else 1


if __name__ == "__main__":
    sys.exit(main())
