"""5-fold temporal cross-validation (half-year folds) of AED siting methods.

Each fold: choose sites using the other four half-years, score on the held-out
half-year. Out-of-sample gains are pooled over all 2,706 arrests; 95% CIs come
from a bootstrap over arrests (paired, so methods are compared on the same draws).
"""
import sys

import numpy as np
import pandas as pd

from aed import Params, gains, load, milp

OUT = "/Volumes/2TB/eurekadev/results"
P_VALUES = [10, 25, 50, 100, 200]
N_RANDOM, N_BOOT = 50, 2000
RNG = np.random.default_rng(2026)


def run(prm=Params(), exclude_top=0, drop_imputed=False, tag="base", p_values=P_VALUES):
    o, s, pairs = load()
    keep = np.ones(len(o), bool)
    if exclude_top:
        top = o.Incident_Location.value_counts().head(exclude_top).index
        keep &= ~o.Incident_Location.isin(top).values
    if drop_imputed:
        keep &= ~o.rt_imputed.values
    o["fold"] = (o.ReceivedTime.dt.year - 2017) * 2 + (o.ReceivedTime.dt.month > 6)
    idx_keep = set(o.idx[keep])

    G_eval = gains(o, s, pairs, prm)
    G_eval = G_eval[G_eval.i.isin(idx_keep)]
    G_mclp = pairs[(pairs.walk_m <= 100) & pairs.i.isin(idx_keep)].assign(g=1.0)
    density = pairs[pairs.i.isin(idx_keep)].groupby("j").size().to_dict()

    n = len(o)
    # per-arrest out-of-sample gain for each (method, p)
    per = {}
    for p in p_values:
        for name in ["random", "classic MCLP", "survival-weighted"]:
            per[(name, p)] = np.zeros(n)
        for f in range(5):
            tr = set(o.idx[(o.fold != f) & keep])
            te = o.idx[(o.fold == f) & keep].values
            Gte = G_eval[G_eval.i.isin(te)]
            sel_ours, _ = milp(G_eval[G_eval.i.isin(tr)], p, site_bonus=density)
            sel_mclp, _ = milp(G_mclp[G_mclp.i.isin(tr)], p, site_bonus=density)
            for name, sel in [("survival-weighted", sel_ours), ("classic MCLP", sel_mclp)]:
                best = Gte[Gte.j.isin(sel)].groupby("i").g.max()
                per[(name, p)][best.index] += best.values
            acc = np.zeros(n)
            for _ in range(N_RANDOM):
                sel = RNG.choice(len(s), p, replace=False)
                best = Gte[Gte.j.isin(sel)].groupby("i").g.max()
                acc[best.index] += best.values
            per[("random", p)] += acc / N_RANDOM
        print(tag, "p =", p, {k[0]: round(v.sum(), 2) for k, v in per.items() if k[1] == p}, flush=True)

    members = np.where(keep)[0]
    boot = RNG.choice(members, (N_BOOT, len(members)), replace=True)
    rows = []
    for (name, p), v in per.items():
        tot = v[boot].sum(1)
        rows.append({"tag": tag, "p": p, "method": name, "oos_gain": v[members].sum(),
                     "ci_lo": np.percentile(tot, 2.5), "ci_hi": np.percentile(tot, 97.5)})
    for p in p_values:
        diff = (per[("survival-weighted", p)] - per[("classic MCLP", p)])[boot].sum(1)
        rows.append({"tag": tag, "p": p, "method": "ours minus classic", "oos_gain": diff.mean(),
                     "ci_lo": np.percentile(diff, 2.5), "ci_hi": np.percentile(diff, 97.5)})
    return pd.DataFrame(rows), per, o


if __name__ == "__main__":
    res, per, o = run()
    res.to_csv(f"{OUT}/cv_results.csv", index=False)
    np.savez(f"{OUT}/cv_per_arrest.npz", **{f"{k[0]}|{k[1]}": v for k, v in per.items()})
    print(res.round(3).to_string())
