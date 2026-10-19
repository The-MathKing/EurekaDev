"""Distributional model: treat EMS response time as random (citywide distribution from the
training folds) instead of using each arrest's own value. Same 5-fold CV and scoring as exp_cv."""
import numpy as np
import pandas as pd

from aed import Params, gains, load, milp

OUT = "/Volumes/2TB/eurekadev/results"
P_VALUES = [10, 25, 50, 100, 200]
N_BOOT = 2000
RNG = np.random.default_rng(2026)

o, s, pairs = load()
o["fold"] = (o.ReceivedTime.dt.year - 2017) * 2 + (o.ReceivedTime.dt.month > 6)
density = pairs.groupby("j").size().to_dict()
G_eval = gains(o, s, pairs, Params())
cv = np.load(f"{OUT}/cv_per_arrest.npz")

G_dist = {}
for f in range(5):
    tr = (o.fold != f).values
    sample = o.response_min[tr & ~o.rt_imputed.values].values
    G_dist[f] = gains(o, s, pairs, Params(), rt_sample=sample)

rows, per = [], {}
for p in P_VALUES:
    v = np.zeros(len(o))
    for f in range(5):
        tr, te = o.idx[o.fold != f], o.idx[o.fold == f]
        Gf = G_dist[f]
        sel, _ = milp(Gf[Gf.i.isin(tr)], p, site_bonus=density)
        Gte = G_eval[G_eval.i.isin(te)]
        best = Gte[Gte.j.isin(sel)].groupby("i").g.max()
        v[best.index] += best.values
    per[p] = v
    boot = RNG.choice(len(o), (N_BOOT, len(o)), replace=True)
    for ref in ["classic MCLP", "survival-weighted"]:
        d = (v - cv[f"{ref}|{p}"])[boot].sum(1)
        rows.append({"p": p, "vs": ref, "dist_gain": v.sum(), "ref_gain": cv[f"{ref}|{p}"].sum(),
                     "diff": v.sum() - cv[f"{ref}|{p}"].sum(),
                     "ci_lo": np.percentile(d, 2.5), "ci_hi": np.percentile(d, 97.5)})
    print(rows[-2], rows[-1], sep="\n", flush=True)
pd.DataFrame(rows).to_csv(f"{OUT}/distribution_cv.csv", index=False)
np.savez(f"{OUT}/distribution_per_arrest.npz", **{str(k): v for k, v in per.items()})
