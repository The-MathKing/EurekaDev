"""Opening hours: cost of assuming 24/7 access, and value of outdoor 24/7 cabinets."""
import numpy as np
import pandas as pd

from aed import Params, gains, load, milp, objective

OUT = "/Volumes/2TB/eurekadev/results"
o, s, pairs = load()
G_real = gains(o, s, pairs, Params(hours="osm"))
G_247 = gains(o, s, pairs, Params(hours="always"))
density = pairs.groupby("j").size().to_dict()

rows = []
for p in [10, 25, 50, 100, 200]:
    sel_naive, _ = milp(G_247, p, site_bonus=density)   # planner assumes 24/7
    sel_aware, _ = milp(G_real, p, site_bonus=density)  # planner uses opening hours
    planned = objective(G_247, sel_naive)
    realized = objective(G_real, sel_naive)
    rows.append({"p": p,
                 "naive_planned": planned, "naive_realized": realized,
                 "overstatement": planned / realized - 1,
                 "hours_aware_realized": objective(G_real, sel_aware),
                 "cabinet_realized": planned})  # same sites, 24/7 outdoor cabinets
    print(rows[-1], flush=True)
pd.DataFrame(rows).to_csv(f"{OUT}/hours.csv", index=False)

# Hour-of-day profile at p = 50: share of arrests with an AED reachable, indoor vs cabinet.
sel, _ = milp(G_real, 50, site_bonus=density)
hour = o.ReceivedTime.dt.hour.values
prof = []
for name, G in [("indoor (opening hours)", G_real), ("24/7 outdoor cabinet", G_247)]:
    best = G[G.j.isin(sel)].groupby("i").g.max().reindex(range(len(o)), fill_value=0).values
    for h in range(24):
        m = hour == h
        prof.append({"scenario": name, "hour": h, "arrests": m.sum(), "gain": best[m].sum()})
pd.DataFrame(prof).to_csv(f"{OUT}/hours_profile.csv", index=False)
