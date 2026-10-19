"""Price of fairness: per-arrest gain in every SVI quartile >= phi * the unconstrained plan's citywide per-arrest gain."""
import numpy as np
import pandas as pd

from aed import Params, gains, load, milp, objective

OUT = "/Volumes/2TB/eurekadev/results"
o, s, pairs = load()
G = gains(o, s, pairs, Params(), rt_sample=o.response_min[~o.rt_imputed].values)
groups = o.set_index("idx").svi_q  # 1 = least vulnerable ... 4 = most vulnerable
n_q = groups.value_counts().sort_index()
density = pairs.groupby("j").size().to_dict()
cap = G.groupby("i").g.max()
print("max achievable per-arrest gain by quartile (all sites):",
      (cap.groupby(groups.reindex(cap.index)).sum() / n_q).round(4).to_dict())

rows = []
for p in [25, 50, 100]:
    base_sel, _ = milp(G, p, site_bonus=density, time_limit=600)
    base = G[G.j.isin(base_sel)].groupby("i").g.max().sum()
    target = base / n_q.sum()  # citywide gain per arrest of the unconstrained plan
    for phi in np.round(np.arange(0, 1.01, 0.05), 2):
        sel, status = milp(G, p, groups=groups, floor=phi * target, site_bonus=density, time_limit=600)
        if status != "optimal":
            print(p, phi, status)
            break
        best = G[G.j.isin(sel)].groupby("i").g.max()
        by_q = best.groupby(groups.reindex(best.index)).sum().reindex(n_q.index, fill_value=0) / n_q
        total = best.sum()
        rows.append({"p": p, "phi": phi, "total": total, "price_of_fairness": 1 - total / base,
                     "min_ratio": by_q.min() / target,
                     **{f"q{q}_per_arrest": v for q, v in by_q.items()}})
        print(rows[-1], flush=True)
pd.DataFrame(rows).to_csv(f"{OUT}/fairness.csv", index=False)
