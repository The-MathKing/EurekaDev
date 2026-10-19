"""Out-of-sample opening-hours and fairness analyses (corrected framework)."""
import json

import numpy as np
import pandas as pd

from aed import Params, gains, milp
from cv import N_FOLDS, choose, score, setup, train_density

OUT = "/Volumes/2TB/eurekadev/results"
o, s, pairs = setup()
valid = ~o.rt_imputed.values
n = len(o)
G_hours = gains(o, s, pairs, Params())
G_247 = gains(o, s, pairs, Params(hours="always"))
sites = json.load(open(f"{OUT}/cv2_sites.json"))

# 1) Overstatement out-of-sample: the hours-blind plan's held-out benefit if every AED were
#    always reachable (what the planner expects) versus with real opening hours (what happens).
rows = []
for p in [10, 25, 50, 100, 200]:
    promised, delivered = np.zeros(n), np.zeros(n)
    for f in range(N_FOLDS):
        sel = sites[f"survival, no hours|{p}"][str(f)]
        te = o.idx[o.fold == f].values
        promised += score(G_247, sel, te, n)
        delivered += score(G_hours, sel, te, n)
    rows.append({"p": p, "promised": promised.sum(), "delivered": delivered.sum(),
                 "overstatement": promised.sum() / delivered.sum() - 1})
pd.DataFrame(rows).to_csv(f"{OUT}/hours2.csv", index=False)
print(pd.DataFrame(rows).round(3).to_string())

# 2) Time-of-day profile (OOS, p = 50): main model indoor vs cabinets.
prof = []
hour = o.ReceivedTime.dt.hour.values
for name, G in [("indoor (opening hours)", G_hours), ("24/7 outdoor cabinet", G_247)]:
    key = "expected survival (main)|50" if name.startswith("indoor") else "main, 24/7 cabinets|50"
    v = np.zeros(n)
    for f in range(N_FOLDS):
        v += score(G, sites[key][str(f)], o.idx[o.fold == f].values, n)
    for h in range(24):
        m = hour == h
        prof.append({"scenario": name, "hour": h, "arrests": m.sum(), "gain": v[m].sum()})
pd.DataFrame(prof).to_csv(f"{OUT}/hours_profile2.csv", index=False)

# 3) Fairness out-of-sample at p = 50: floor set from TRAINING arrests, scored on held-out arrests.
groups = o.set_index("idx").svi_q
q_all = groups.dropna()
rows = []
P = 50
for phi in [0.0, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9]:
    v = np.zeros(n)
    infeasible = 0
    for f in range(N_FOLDS):
        tr = (o.fold != f).values
        G_tr = gains(o, s, pairs, Params(), rt_sample=o.response_min.values[tr & valid])
        G_tr = G_tr[G_tr.i.isin(o.idx[tr])]
        dens = train_density(pairs, o.idx[tr])
        g_tr = groups[tr]
        base, _ = choose(G_tr, P, len(s), dens)
        T = G_tr[G_tr.j.isin(base)].groupby("i").g.max().sum() / g_tr.notna().sum()
        sel, st = (base, "optimal") if phi == 0 else milp(G_tr, P, groups=g_tr, floor=phi * T,
                                                          site_bonus=dens, time_limit=600)
        if st != "optimal":
            infeasible += 1
            sel = base
        v += score(G_hours, sel, o.idx[~tr].values, n)
    by_q = pd.Series(v).groupby(groups.values).sum() / q_all.value_counts().sort_index()
    rows.append({"phi": phi, "infeasible_folds": infeasible, "total": v.sum(),
                 **{f"q{int(k)}_per100": by_q[k] * 100 for k in by_q.index}})
    print(rows[-1], flush=True)
pd.DataFrame(rows).to_csv(f"{OUT}/fairness_oos.csv", index=False)
