"""Place-based (kernel-smoothed, 1 km) response time, in the corrected OOS framework.
Also checks the own-RT vs median-RT difference with the address-clustered bootstrap."""
import numpy as np
import pandas as pd

from aed import Params, gains
from cv import cluster_boot, run_cv, setup

OUT = "/Volumes/2TB/eurekadev/results"
P = [25, 50, 100]
o, s, pairs = setup()
valid = ~o.rt_imputed.values
lat, lon = np.radians(o.Latitude.values), np.radians(o.Longitude.values)
a = (np.sin((lat[None] - lat[:, None]) / 2) ** 2
     + np.cos(lat[:, None]) * np.cos(lat[None]) * np.sin((lon[None] - lon[:, None]) / 2) ** 2)
K = np.exp(-((2 * 6371000 * np.arcsin(np.sqrt(a))) / 1000.0) ** 2 / 2)
r = o.response_min.clip(upper=30).values


def smoothed(o_, tr):
    w = K[:, tr & valid]
    return gains(o.assign(response_min=(w @ r[tr & valid]) / w.sum(1)), s, pairs, Params())


res = run_cv(o, s, pairs, {"smoothed RT (1 km)": smoothed}, P, gains(o, s, pairs, Params()))
cv = np.load(f"{OUT}/cv2_per_arrest.npz")
arrays = {k: v["gain"] for k, v in res.items()}
for p in P:
    for name in ["survival+hours, own RT", "survival+hours, median RT", "expected survival (main)"]:
        arrays[(name, p)] = cv[f"{name}|{p}"]
boot = cluster_boot(o, arrays)
rows = []
for p in P:
    for a_, b_ in [("smoothed RT (1 km)", "expected survival (main)"),
                   ("survival+hours, own RT", "survival+hours, median RT")]:
        d = boot[(a_, p)] - boot[(b_, p)]
        rows.append({"p": p, "a": a_, "b": b_, "a_gain": arrays[(a_, p)].sum(), "b_gain": arrays[(b_, p)].sum(),
                     "ci_lo": np.percentile(d, 2.5), "ci_hi": np.percentile(d, 97.5)})
d = pd.DataFrame(rows)
d.to_csv(f"{OUT}/smoothed_rt2.csv", index=False)
print(d.round(2).to_string())
