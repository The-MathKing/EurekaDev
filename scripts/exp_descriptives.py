"""Small checks behind numbers quoted in the paper:
  - share of response-time variance explained by location (leave-one-out kernel R^2)
  - candidate sites per km^2 and median response time by SVI quartile
  - greedy vs exact MILP on the full data (indoor and cabinet models)
  - 100 m coverage of held-out arrests, both 24/7 (classic's own metric) and open-at-the-time
  - reach-curve summary numbers
"""
import json

import geopandas as gpd
import numpy as np
import pandas as pd

from aed import Params, gains, greedy, load, milp, objective, reach_curve

OUT = "/Volumes/2TB/eurekadev/results"
DATA = "/Volumes/2TB/eurekadev/data"
o, s, pairs = load()
valid = ~o.rt_imputed.values
out = {}

# 1) Location vs response time.
v = o[valid].reset_index(drop=True)
lat, lon = np.radians(v.Latitude.values), np.radians(v.Longitude.values)
a = (np.sin((lat[None] - lat[:, None]) / 2) ** 2
     + np.cos(lat[:, None]) * np.cos(lat[None]) * np.sin((lon[None] - lon[:, None]) / 2) ** 2)
D = 2 * 6371000 * np.arcsin(np.sqrt(a))
r = v.response_min.clip(upper=30).values
out["loo_kernel_r2"] = {}
for bw in [500, 1000, 2000, 3000]:
    W = np.exp(-(D / bw) ** 2 / 2)
    np.fill_diagonal(W, 0)
    pred = W @ r / W.sum(1)
    out["loo_kernel_r2"][bw] = round(float(1 - ((r - pred) ** 2).mean() / r.var()), 4)

# 2) Geography by SVI quartile.
t = gpd.read_file(f"{DATA}/vb_tracts.geojson").to_crs(32618)
t["km2"] = t.area / 1e6
counts = s.groupby(s.GEOID.astype(str)).size()
t["sites"] = t.GEOID.astype(str).map(counts).fillna(0)
g = t.groupby("svi_q").agg(km2=("km2", "sum"), sites=("sites", "sum"))
g["sites_per_km2"] = g.sites / g.km2
g["median_rt_valid"] = o[valid].groupby("svi_q").response_min.median()
out["quartiles"] = g.round(3).reset_index().to_dict(orient="records")

# 3) Greedy vs exact.
rt = o.response_min[valid].values
out["greedy_vs_exact"] = []
for h in ["osm", "always"]:
    G = gains(o, s, pairs, Params(hours=h), rt_sample=rt)
    for p in [10, 25, 50, 100, 200]:
        m, _ = milp(G, p)
        out["greedy_vs_exact"].append({"hours": h, "p": p,
                                       "ratio": round(objective(G, greedy(G, p)) / objective(G, m), 5)})

# 4) 100 m coverage of held-out arrests, from the cross-validation site choices.
o["fold"] = (o.ReceivedTime.dt.year - 2017) * 2 + (o.ReceivedTime.dt.month > 6)
sites = json.load(open(f"{OUT}/cv2_sites.json"))
cov_open = gains(o, s, pairs, Params(max_walk_m=100))
cov_247 = pairs[pairs.walk_m <= 100]
out["coverage100_heldout"] = []
for p in [10, 25, 50, 100, 200]:
    for m in ["classic MCLP 100 m", "expected survival (main)"]:
        n247 = nopen = 0
        for f in range(5):
            te = set(o.idx[o.fold == f])
            sel = set(sites[f"{m}|{p}"][str(f)])
            n247 += cov_247[cov_247.j.isin(sel) & cov_247.i.isin(te)].i.nunique()
            nopen += cov_open[cov_open.j.isin(sel) & cov_open.i.isin(te)].i.nunique()
        out["coverage100_heldout"].append({"p": p, "method": m, "covered_24_7": n247, "covered_open": nopen})

# 5) Reach curve.
d = np.arange(0, 1001, 1.0)
for speed in [1.0, 1.4, 2.0]:
    f = reach_curve(d, rt, Params(walk_speed=speed))
    out[f"reach_{speed}"] = {"rho0": round(float(f[0]), 4),
                             "half_value_m": float(d[np.argmax(f <= f[0] / 2)]),
                             "share_at_300m": round(float(f[300] / f[0]), 4),
                             "share_at_500m": round(float(f[500] / f[0]), 4)}

# 6) Arrests unreachable on foot, by quartile.
reach = set(pairs.i)
out["off_network_by_quartile"] = o[~o.idx.isin(reach)].svi_q.value_counts(dropna=False).to_dict()

json.dump(out, open(f"{OUT}/descriptives.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
