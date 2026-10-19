"""Main out-of-sample comparison (supersedes exp_cv / exp_ablation / exp_distribution).

Methods (all choose exactly p sites, trained only on training folds):
  classic MCLP 100 m        Church & ReVelle: count arrests within 100 m, sites assumed 24/7
  MCLP 100 m + hours        Sun et al. 2016 style: count arrests within 100 m of an OPEN site
  MCLP 300 m                classic with a larger radius
  survival, no hours        Pourghaderi et al. 2021 style: expected survival, sites assumed 24/7
  survival+hours, own RT    our first model: each arrest's own response time
  survival+hours, median RT every arrest gets the training-median response time
  expected survival (main)  survival + hours, response time ~ training distribution
  main, 24/7 cabinets       main model with sites in outdoor cabinets (scored as always open)
Scoring: realised survival gain on held-out arrests using their actual response times and real
opening hours (cabinets: always open); also 100 m open-AED coverage.
"""
import json

import numpy as np
import pandas as pd

from aed import Params, gains
from cv import N_FOLDS, cluster_boot, run_cv, score, setup

OUT = "/Volumes/2TB/eurekadev/results"
P_VALUES = [10, 25, 50, 100, 200]

o, s, pairs = setup()
valid = ~o.rt_imputed.values


def rt_sample(train):
    return o.response_min.values[train & valid]


def count_table(radius, hours):
    if hours:
        return gains(o, s, pairs, Params(max_walk_m=radius)).assign(g=1.0)
    return pairs[pairs.walk_m <= radius].assign(g=1.0)


methods = {
    "classic MCLP 100 m": lambda o_, tr: count_table(100, False),
    "MCLP 100 m + hours": lambda o_, tr: count_table(100, True),
    "MCLP 300 m": lambda o_, tr: count_table(300, False),
    "survival, no hours": lambda o_, tr: gains(o, s, pairs, Params(hours="always"), rt_sample=rt_sample(tr)),
    "survival+hours, own RT": lambda o_, tr: gains(o, s, pairs, Params()),
    "survival+hours, median RT": lambda o_, tr: gains(
        o.assign(response_min=np.median(rt_sample(tr))), s, pairs, Params()),
    "expected survival (main)": lambda o_, tr: gains(o, s, pairs, Params(), rt_sample=rt_sample(tr)),
    "main, 24/7 cabinets": lambda o_, tr: gains(o, s, pairs, Params(hours="always"), rt_sample=rt_sample(tr)),
}

G_eval = gains(o, s, pairs, Params())
G_eval_cab = gains(o, s, pairs, Params(hours="always"))
G_cov = gains(o, s, pairs, Params(max_walk_m=100)).assign(g=1.0)
res = run_cv(o, s, pairs, methods, P_VALUES, G_eval, G_cov, eval_overrides={"main, 24/7 cabinets": G_eval_cab})

# Random placement: mean over 30 draws per fold.
rng = np.random.default_rng(2026)
for p in P_VALUES:
    g = np.zeros(len(o))
    for f in range(N_FOLDS):
        te = o.idx[o.fold == f].values
        for _ in range(30):
            g += score(G_eval, rng.choice(len(s), p, replace=False), te, len(o)) / 30
    res[("random", p)] = {"gain": g, "cov": np.zeros(len(o)), "sites": {}}

np.savez(f"{OUT}/cv2_per_arrest.npz", **{f"{k[0]}|{k[1]}": v["gain"] for k, v in res.items()})
json.dump({f"{k[0]}|{k[1]}": {str(f): [int(x) for x in v["sites"][f]] for f in v["sites"]}
           for k, v in res.items() if v["sites"]}, open(f"{OUT}/cv2_sites.json", "w"))

boot = cluster_boot(o, {k: v["gain"] for k, v in res.items()})
rows = []
for (name, p), v in res.items():
    b = boot[(name, p)]
    ref = boot[("classic MCLP 100 m", p)]
    main = boot[("expected survival (main)", p)]
    folds = [v["gain"][o.fold.values == f].sum() for f in range(N_FOLDS)]
    rows.append({"p": p, "method": name, "gain": v["gain"].sum(),
                 "ci_lo": np.percentile(b, 2.5), "ci_hi": np.percentile(b, 97.5),
                 "vs_classic": v["gain"].sum() - res[("classic MCLP 100 m", p)]["gain"].sum(),
                 "vs_classic_lo": np.percentile(b - ref, 2.5), "vs_classic_hi": np.percentile(b - ref, 97.5),
                 "main_minus_this_lo": np.percentile(main - b, 2.5), "main_minus_this_hi": np.percentile(main - b, 97.5),
                 "cov100": v["cov"].sum() / len(o),
                 **{f"fold{f}": x for f, x in enumerate(folds)}})
d = pd.DataFrame(rows)
d.to_csv(f"{OUT}/cv2_results.csv", index=False)
pd.set_option("display.width", 250)
print(d.pivot_table(index="method", columns="p", values="gain", sort=False).round(2).to_string())
print(d[["p", "method", "vs_classic", "vs_classic_lo", "vs_classic_hi", "main_minus_this_lo", "main_minus_this_hi", "cov100"]].round(3).to_string())
