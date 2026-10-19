"""Robustness of main-vs-classic under alternative assumptions (corrected OOS framework)."""
import numpy as np
import pandas as pd

from aed import Params, gains
from cv import cluster_boot, run_cv, setup

OUT = "/Volumes/2TB/eurekadev/results"
P = [25, 50, 100]
o, s, pairs_all = setup()
valid = ~o.rt_imputed.values

SCENARIOS = [
    ("walk 1.0 m/s", Params(walk_speed=1.0), None),
    ("walk 2.0 m/s (jog)", Params(walk_speed=2.0), None),
    ("max walk 300 m", Params(max_walk_m=300), None),
    ("max walk 800 m", Params(max_walk_m=800), None),
    ("De Maio survival curve", Params(survival="demaio"), None),
    ("call delay 2 min", Params(call_delay=2.0), None),
    ("AED setup 1.5 min", Params(setup_min=1.5), None),
    ("EMS arrival-to-shock 2 min", Params(ems_defib_min=2.0), None),
    ("imputed response times dropped", Params(), "imputed"),
    ("top-20 repeat addresses dropped", Params(), "top20"),
]
rows = []
for tag, prm, drop in SCENARIOS:
    keep = np.ones(len(o), bool)
    if drop == "imputed":
        keep = valid.copy()
    elif drop == "top20":
        keep = ~o.Incident_Location.isin(o.Incident_Location.value_counts().head(20).index).values
    pairs = pairs_all[pairs_all.i.isin(np.where(keep)[0])]

    def rt(tr):
        return o.response_min.values[tr & valid & keep]

    methods = {
        "classic": lambda o_, tr: pairs[pairs.walk_m <= 100].assign(g=1.0),
        "main": lambda o_, tr, prm=prm: gains(o, s, pairs, prm, rt_sample=rt(tr)),
    }
    G_eval = gains(o, s, pairs, prm)
    res = run_cv(o, s, pairs, methods, P, G_eval)
    boot = cluster_boot(o, {k: v["gain"] for k, v in res.items()})
    for p in P:
        diff = boot[("main", p)] - boot[("classic", p)]
        rows.append({"scenario": tag, "p": p, "main": res[("main", p)]["gain"].sum(),
                     "classic": res[("classic", p)]["gain"].sum(),
                     "diff": res[("main", p)]["gain"].sum() - res[("classic", p)]["gain"].sum(),
                     "ci_lo": np.percentile(diff, 2.5), "ci_hi": np.percentile(diff, 97.5)})
    print(pd.DataFrame(rows[-3:]).round(2).to_string(header=False), flush=True)
pd.DataFrame(rows).to_csv(f"{OUT}/sensitivity2.csv", index=False)
