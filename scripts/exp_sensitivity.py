"""Robustness: re-run the cross-validation under alternative assumptions (p = 25, 50, 100)."""
import pandas as pd

from aed import Params
from exp_cv import run

OUT = "/Volumes/2TB/eurekadev/results"
P = [25, 50, 100]
SCENARIOS = [
    ("walk 1.0 m/s", dict(prm=Params(walk_speed=1.0))),
    ("walk 2.0 m/s (jog)", dict(prm=Params(walk_speed=2.0))),
    ("max walk 300 m", dict(prm=Params(max_walk_m=300))),
    ("max walk 800 m", dict(prm=Params(max_walk_m=800))),
    ("De Maio survival curve", dict(prm=Params(survival="demaio"))),
    ("call delay 2 min", dict(prm=Params(call_delay=2.0))),
    ("imputed response times dropped", dict(drop_imputed=True)),
    ("top-20 repeat addresses dropped", dict(exclude_top=20)),
]
frames = []
for tag, kw in SCENARIOS:
    res, _, _ = run(tag=tag, p_values=P, **kw)
    frames.append(res)
    pd.concat(frames).to_csv(f"{OUT}/sensitivity.csv", index=False)
print(pd.concat(frames).query("method == 'ours minus classic'").round(2).to_string())
