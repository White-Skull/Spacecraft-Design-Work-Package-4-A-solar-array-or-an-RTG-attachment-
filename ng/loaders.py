"""Load sets of design values from a python file or a CSV file."""
from __future__ import annotations

import csv
import importlib.util
from dataclasses import fields
from pathlib import Path

from design import LugDesign

HERE = Path(__file__).parent


def load_python(path=None) -> list:
    """Import a .py file that defines CANDIDATES (a list of LugDesign)."""
    path = Path(path) if path else HERE / "candidates.py"
    spec = importlib.util.spec_from_file_location("candidates_user", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return list(mod.CANDIDATES)


def parse_bolts(text: str) -> list:
    """'x:y;x:y' -> [(x, y), ...]"""
    return [tuple(float(v) for v in pair.split(":")) for pair in text.split(";") if pair.strip()]


def load_csv(path) -> list:
    """One row per design. Column names are LugDesign input field names;
    blank/missing columns keep the default. Bolts column: 'x:y;x:y;...'."""
    inputs = {f.name: f for f in fields(LugDesign) if f.metadata["kind"] == "input"}
    convert = {"float": float, "int": int, "str": str}
    designs = []
    with open(path, newline="") as fh:
        reader = csv.DictReader(fh)
        unknown = set(reader.fieldnames or []) - set(inputs)
        if unknown:
            raise ValueError(f"CSV columns that are not input fields: {sorted(unknown)}")
        for row in reader:
            d = LugDesign()
            for key, text in row.items():
                if text is None or text.strip() == "":
                    continue
                if key == "bolts":
                    setattr(d, key, parse_bolts(text))
                else:
                    setattr(d, key, convert[inputs[key].type](text.strip()))
            designs.append(d)
    return designs
