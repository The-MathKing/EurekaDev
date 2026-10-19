"""Does a place-based (kernel-smoothed) response time help where per-incident response time did not?

Per fold, each arrest's response time is replaced by a Gaussian-kernel average (bandwidth 1 km)
of valid response times of TRAINING-fold arrests only, then sites are chosen and scored as usual.
"""
import numpy as np
import pandas as pd

from aed import Params, gains, load, milp

OUT = "/Volumes/2TB/eurekadev/results"
BW = 1000.0
o, s, pairs = load()
o["fold"] = (o.ReceivedTime.dt.year - 2017) * 2 + (o.ReceivedTime.dt.month > 6)
density = pairs.groupby("j").size().to_dict()
G_eval = gains(o, s, pairs, Params())

lat, lon = np.radians(o.Latitude.values), np.radians(o.Longitude.values)
a = (np.sin((lat[None] - lat[:, None]) / 2) ** 2
     + np.cos(lat[:, None]) * np.cos(lat[None]) * np.sin((lon[None] - lon[:, None]) / 2) ** 2)
K = np.exp(-((2 * 6371000 * np.arcsin(np.sqrt(a))) / BW) ** 2 / 2)
r = o.response_min.clip(upper=30).values
valid = ~o.rt_imputed.values

rows = []
for p in [25, 50, 100]:
    tot = 0.0
    for f in range(5):
        tr = (o.fold != f).values
        w = K[:, tr & valid]
        o_s = o.assign(response_min=(w @ r[tr & valid]) / w.sum(1))
        G_tr = gains(o_s, s, pairs, Params())
        sel, _ = milp(G_tr[G_tr.i.isin(o.idx[tr])], p, site_bonus=density)
        Gte = G_eval[G_eval.i.isin(o.idx[~tr])]
        tot += Gte[Gte.j.isin(sel)].groupby("i").g.max().sum()
    rows.append({"p": p, "variant": "smoothed RT (1 km)", "oos_gain": tot})
    print(rows[-1], flush=True)
pd.DataFrame(rows).to_csv(f"{OUT}/smoothed_rt.csv", index=False)
