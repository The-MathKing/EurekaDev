"""Weekly availability (7 days x 24 hours) for candidate AED host sites.

Uses the OpenStreetMap `opening_hours` tag when it can be parsed, otherwise a
category default. Defaults are modelling assumptions and are listed in the paper.
"""
import re

import numpy as np

DAYS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

# Category defaults: list of (days, start_hour, end_hour) with end exclusive.
DEFAULTS = {
    "fire_station": [("Mo-Su", 0, 24)],
    "police": [("Mo-Su", 0, 24)],
    "fuel": [("Mo-Su", 5, 23)],
    "convenience": [("Mo-Su", 6, 23)],
    "supermarket": [("Mo-Su", 7, 22)],
    "pharmacy": [("Mo-Fr", 8, 21), ("Sa-Su", 9, 18)],
    "bank": [("Mo-Fr", 9, 17), ("Sa", 9, 12)],
    "school": [("Mo-Fr", 7, 16)],
    "place_of_worship": [("Su", 8, 13), ("We", 18, 20)],
    "library": [("Mo-Sa", 10, 19)],
    "community_centre": [("Mo-Fr", 8, 17)],
    "townhall": [("Mo-Fr", 8, 17)],
    "post_office": [("Mo-Fr", 9, 17)],
    "fitness_centre": [("Mo-Su", 5, 22)],
    "sports_centre": [("Mo-Su", 5, 22)],
}
FALLBACK = [("Mo-Su", 8, 21)]


def _day_set(spec):
    out = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            ia, ib = DAYS.index(a), DAYS.index(b)
            rng = range(ia, ib + 1) if ia <= ib else list(range(ia, 7)) + list(range(0, ib + 1))
            out.update(rng)
        else:
            out.add(DAYS.index(part))
    return out


def _fill(grid, days, start, end):
    for d in days:
        if end > start:
            grid[d, start:end] = True
        else:  # past midnight, e.g. 18:00-02:00
            grid[d, start:] = True
            grid[(d + 1) % 7, :end] = True


def _from_rules(rules):
    grid = np.zeros((7, 24), dtype=bool)
    for days, start, end in rules:
        _fill(grid, _day_set(days), start, end)
    return grid


TIME = r"(\d{1,2}):(\d{2})"
RULE = re.compile(rf"^((?:{'|'.join(DAYS)})(?:\s*[-,]\s*(?:{'|'.join(DAYS)}))*)?\s*((?:{TIME}\s*-\s*{TIME}\s*,?\s*)+|off|closed)$")


def parse_opening_hours(text):
    """Parse common OSM opening_hours strings; return a 7x24 bool grid or None."""
    if not isinstance(text, str):
        return None
    text = text.strip()
    if text in ("24/7", "Mo-Su 00:00-24:00"):
        return np.ones((7, 24), dtype=bool)
    grid = np.zeros((7, 24), dtype=bool)
    for rule in text.split(";"):
        rule = rule.strip()
        if not rule:
            continue
        m = RULE.match(rule)
        if not m:
            return None
        days = _day_set(m.group(1).replace(" ", "")) if m.group(1) else set(range(7))
        if m.group(2) in ("off", "closed"):
            grid[list(days), :] = False
            continue
        for h1, m1, h2, m2 in re.findall(rf"{TIME}\s*-\s*{TIME}", m.group(2)):
            start = int(h1)
            end = int(h2) + (1 if int(m2) > 0 else 0)
            _fill(grid, days, start, min(end, 24))
    return grid


def availability(sites):
    """Return (array n_sites x 7 x 24, array of source labels 'osm' / 'default')."""
    grids, source = [], []
    for kind, oh in zip(sites.kind, sites.opening_hours):
        g = parse_opening_hours(oh)
        if g is None:
            g = _from_rules(DEFAULTS.get(kind, FALLBACK))
            source.append("default")
        else:
            source.append("osm")
        grids.append(g)
    return np.stack(grids), np.array(source)
