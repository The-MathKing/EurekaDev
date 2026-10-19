"""Export data for the interactive AED Placement Explorer and write prototype/index.html."""
import json
import os

import numpy as np

from aed import Params, gains, greedy, load
from hours import availability

OUT = "/Volumes/2TB/eurekadev/prototype"
P_MAX = 200
os.makedirs(OUT, exist_ok=True)

o, s, pairs = load()
# Sites are ordered with the expected-survival model (response-time distribution) and scored
# with each arrest's actual response time, as in the paper.
rt = o.response_min[~o.rt_imputed].values
G_real = gains(o, s, pairs, Params())
G_247 = gains(o, s, pairs, Params(hours="always"))
P_real = gains(o, s, pairs, Params(), rt_sample=rt)
P_247 = gains(o, s, pairs, Params(hours="always"), rt_sample=rt)
G_mclp = pairs[pairs.walk_m <= 100].assign(g=1.0)

svi = o.svi_q.fillna(0).astype(int).values  # 0 = no SVI data


def prefix_curve(order, G):
    """Cumulative total gain, per-quartile gain and marginal gain as sites are added in order."""
    by_site = {j: grp[["i", "g"]].values for j, grp in G.groupby("j")}
    best = np.zeros(len(o))
    total, quart, marg = [], [], []
    for j in order:
        before = best.sum()
        for i, g in by_site.get(j, ()):
            best[int(i)] = max(best[int(i)], g)
        total.append(round(best.sum(), 4))
        marg.append(round(best.sum() - before, 4))
        quart.append([round(best[svi == q].sum(), 4) for q in (1, 2, 3, 4)])
    return total, quart, marg


scen = {}
for key, order_G, eval_G in [("indoor", P_real, G_real), ("cabinet", P_247, G_247),
                             ("classic", G_mclp, G_real)]:
    order = [int(j) for j in greedy(order_G, P_MAX)]
    total, quart, marg = prefix_curve(order, eval_G)
    scen[key] = {"order": order, "total": total, "quart": quart, "marg": marg}
    print(key, "sites:", len(order), "gain@50:", total[min(49, len(total) - 1)])

A, src = availability(s)
hours = []
for k in range(len(s)):
    if A[k].all():
        hours.append("24/7" + (" (OSM)" if src[k] == "osm" else " (assumed)"))
    elif src[k] == "osm":
        hours.append(f"OSM: {s.opening_hours.iloc[k]}")
    else:
        hours.append(f"assumed typical hours for {s.kind.iloc[k].replace('_', ' ')}")

data = {
    "arrests": [[round(a, 5), round(b, 5), round(r, 1), int(q), int(h)] for a, b, r, q, h in
                zip(o.Latitude, o.Longitude, o.response_min, svi, o.ReceivedTime.dt.hour)],
    "sites": [[round(a, 5), round(b, 5), k.replace("_", " "), n if isinstance(n, str) else "", hr]
              for a, b, k, n, hr in zip(s.lat, s.lon, s.kind, s.name, hours)],
    "n_by_q": [int((svi == q).sum()) for q in (1, 2, 3, 4)],
    "scenarios": scen,
}
blob = json.dumps(data, separators=(",", ":"))
open(f"{OUT}/data.json", "w").write(blob)

html = open(os.path.join(os.path.dirname(__file__), "prototype_template.html")).read()
html = html.replace("__DATA__", blob.replace("</", "<\\/"))
open(f"{OUT}/index.html", "w").write(html)
print("wrote", f"{OUT}/index.html", os.path.getsize(f"{OUT}/index.html") // 1024, "KB")
