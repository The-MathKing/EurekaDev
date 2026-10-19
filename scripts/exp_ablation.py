"""Ablation: which ingredient drives the improvement over classic MCLP?

All variants are scored on the same out-of-sample, hours-aware survival gain (5 half-year folds).
  classic          count within 100 m, sites assumed 24/7
  + hours          count within 100 m, only sites open at the time of each arrest
  + survival       survival-weighted gain (response-time weighted), sites assumed 24/7
  full model       survival-weighted gain with opening hours
  no RT weighting  full model but every arrest gets the citywide median response time
"""
import numpy as np
import pandas as pd

from aed import Params, gains, load, milp

OUT = "/Volumes/2TB/eurekadev/results"
P_VALUES = [25, 50, 100]
N_BOOT = 2000
RNG = np.random.default_rng(2026)

o, s, pairs = load()
o["fold"] = (o.ReceivedTime.dt.year - 2017) * 2 + (o.ReceivedTime.dt.month > 6)
density = pairs.groupby("j").size().to_dict()

G_eval = gains(o, s, pairs, Params())
o_flat = o.assign(response_min=o.response_min.median())
variants = {
    "classic": pairs[pairs.walk_m <= 100].assign(g=1.0),
    "+ hours": gains(o, s, pairs, Params(max_walk_m=100)).assign(g=1.0),
    "+ survival (no hours)": gains(o, s, pairs, Params(hours="always")),
    "no RT weighting": gains(o_flat, s, pairs, Params()),
    "full model": G_eval,
}

per = {}
for p in P_VALUES:
    for name, Gv in variants.items():
        v = np.zeros(len(o))
        for f in range(5):
            tr, te = o.idx[o.fold != f], o.idx[o.fold == f]
            sel, _ = milp(Gv[Gv.i.isin(tr)], p, site_bonus=density)
            Gte = G_eval[G_eval.i.isin(te)]
            best = Gte[Gte.j.isin(sel)].groupby("i").g.max()
            v[best.index] += best.values
        per[(name, p)] = v
    print(p, {k[0]: round(v.sum(), 2) for k, v in per.items() if k[1] == p}, flush=True)

boot = RNG.choice(len(o), (N_BOOT, len(o)), replace=True)
rows = []
for (name, p), v in per.items():
    d = (v - per[("classic", p)])[boot].sum(1)
    rows.append({"p": p, "variant": name, "oos_gain": v.sum(), "vs_classic": v.sum() - per[("classic", p)].sum(),
                 "ci_lo": np.percentile(d, 2.5), "ci_hi": np.percentile(d, 97.5)})
    if name == "full model":
        d2 = (v - per[("no RT weighting", p)])[boot].sum(1)
        rows.append({"p": p, "variant": "full minus no-RT-weighting", "oos_gain": d2.mean(),
                     "vs_classic": np.nan, "ci_lo": np.percentile(d2, 2.5), "ci_hi": np.percentile(d2, 97.5)})
res = pd.DataFrame(rows)
res.to_csv(f"{OUT}/ablation.csv", index=False)
print(res.round(2).to_string())
