"""How many indoor (opening-hours) AEDs is a 24/7 outdoor cabinet worth?

Uses greedy curves (greedy matched the exact MILP at every budget tested), so F(p) is available
for every p. For each number of cabinets p, finds the smallest number of indoor AEDs q with
F_indoor(q) >= F_cabinet(p); q is infinite when even all 929 indoor sites fall short.
"""
import numpy as np
import pandas as pd

from aed import Params, gains, greedy, load

OUT = "/Volumes/2TB/eurekadev/results"
o, s, pairs = load()


def curve(G, pmax):
    order = greedy(G, pmax)
    best, out = {}, []
    by_site = {j: grp[["i", "g"]].values for j, grp in G.groupby("j")}
    total = 0.0
    for j in order:
        for i, g in by_site[j]:
            if g > best.get(int(i), 0.0):
                total += g - best.get(int(i), 0.0)
                best[int(i)] = g
        out.append(total)
    return np.array(out)


G_in = gains(o, s, pairs, Params(hours="osm"))
G_cab = gains(o, s, pairs, Params(hours="always"))
f_in = curve(G_in, G_in.j.nunique())
f_cab = curve(G_cab, 200)
print(f"indoor: all {len(f_in)} useful sites -> {f_in[-1]:.2f}")
rows = []
for p in range(1, 201):
    q = int(np.searchsorted(f_in, f_cab[p - 1]) + 1) if f_cab[p - 1] <= f_in[-1] else np.inf
    rows.append({"p_cabinets": p, "F_cabinet": f_cab[p - 1], "indoor_needed": q,
                 "ratio": q / p if np.isfinite(q) else np.inf})
d = pd.DataFrame(rows)
d.to_csv(f"{OUT}/cabinets.csv", index=False)
pd.DataFrame({"p": np.arange(1, len(f_in) + 1), "F_indoor": f_in}).to_csv(f"{OUT}/indoor_curve.csv", index=False)
print(d[d.p_cabinets.isin([1, 2, 5, 10, 15, 20, 25, 30, 40, 50])].round(2).to_string())
first_inf = d[~np.isfinite(d.indoor_needed)].p_cabinets.min()
print("smallest number of cabinets that beats AEDs at every indoor site:", first_inf)
