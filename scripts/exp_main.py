"""Main experiment: train on 2017-18 OHCAs, test on 2019 OHCAs.

Compares site-selection methods by out-of-sample expected survival gain and
by 100 m open-site coverage. Also records greedy-vs-MILP optimality gaps.
"""
import json
import time

import numpy as np
import pandas as pd

from aed import Params, gains, greedy, load, milp, objective

OUT = "/Volumes/2TB/eurekadev/results"
P_VALUES = [10, 25, 50, 100, 200]
RNG = np.random.default_rng(2026)

o, s, pairs = load()
train = set(o.idx[o.ReceivedTime < "2019-01-01"])
test = set(o.idx[o.ReceivedTime >= "2019-01-01"])
print(f"train {len(train)} arrests, test {len(test)} arrests")

# Evaluation model: survival gain with real opening hours (the "truth" we score against).
G_eval = gains(o, s, pairs, Params())
# Coverage indicator: open site within 100 m walking at time of arrest.
G_cov = gains(o, s, pairs, Params(max_walk_m=100))
G_cov = G_cov.assign(g=1.0)

# Classic MCLP (Church & ReVelle 1974): count arrests within 100 m, sites assumed always open.
G_mclp = pairs[pairs.walk_m <= 100].assign(g=1.0)
G_mclp = G_mclp[G_mclp.i.isin(train)]
G_ours = G_eval[G_eval.i.isin(train)]

rows, gaps = [], []
for p in P_VALUES:
    t0 = time.time()
    picks = {}
    picks["classic MCLP (100 m, 24/7)"], st1 = milp(G_mclp, p)
    picks["survival-weighted (ours)"], st2 = milp(G_ours, p)
    g_sel = greedy(G_ours, p)
    picks["survival-weighted greedy"] = g_sel
    f_opt, f_gr = objective(G_ours, picks["survival-weighted (ours)"]), objective(G_ours, g_sel)
    gaps.append({"p": p, "milp": f_opt, "greedy": f_gr, "ratio": f_gr / f_opt, "status": st2})

    rand_eval = [objective(G_eval, RNG.choice(len(s), p, replace=False), test) for _ in range(200)]
    rand_cov = [objective(G_cov, RNG.choice(len(s), p, replace=False), test) for _ in range(200)]
    rows.append({"p": p, "method": "random", "test_gain": np.mean(rand_eval),
                 "test_gain_sd": np.std(rand_eval), "test_cov100": np.mean(rand_cov) / len(test)})
    for name, sel in picks.items():
        rows.append({"p": p, "method": name, "test_gain": objective(G_eval, sel, test),
                     "test_gain_sd": 0.0, "test_cov100": objective(G_cov, sel, test) / len(test),
                     "train_gain": objective(G_eval, sel, train)})
    print(f"p={p} done in {time.time() - t0:.0f}s ({st1}, {st2})")

ceiling = {"test_gain_all_sites": objective(G_eval, list(range(len(s))), test),
           "test_cov100_all_sites": objective(G_cov, list(range(len(s))), test) / len(test)}
res = pd.DataFrame(rows)
res.to_csv(f"{OUT}/main_results.csv", index=False)
pd.DataFrame(gaps).to_csv(f"{OUT}/greedy_gap.csv", index=False)
json.dump(ceiling, open(f"{OUT}/ceiling.json", "w"), indent=1)
print(res.round(4).to_string())
print(pd.DataFrame(gaps).round(4).to_string())
print(ceiling)
