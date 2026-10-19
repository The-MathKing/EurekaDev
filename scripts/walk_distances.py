"""Walking distances (m) from each OHCA to candidate sites within 1 km, via the OSMnx walk network.

distance = snap(arrest -> nearest node) + network path + snap(nearest node -> site),
and never less than the straight-line distance. Points more than MAX_SNAP_M from the
network are treated as unreachable on foot (no pairs).
"""
import networkx as nx
import numpy as np
import osmnx as ox
import pandas as pd

CUTOFF_M = 1000
MAX_SNAP_M = 150


def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371000 * np.arcsin(np.sqrt(a))


o = pd.read_csv("data/ohcas_clean.csv")
s = pd.read_csv("data/sites_clean.csv")

G = ox.graph_from_place("Virginia Beach, Virginia, USA", network_type="walk")
G = ox.convert.to_undirected(G)
print("walk graph:", G.number_of_nodes(), "nodes", G.number_of_edges(), "edges")

o_node, o_snap = ox.distance.nearest_nodes(G, o.Longitude.values, o.Latitude.values, return_dist=True)
s_node, s_snap = ox.distance.nearest_nodes(G, s.lon.values, s.lat.values, return_dist=True)
print(f"arrests snapped > {MAX_SNAP_M} m: {(np.asarray(o_snap) > MAX_SNAP_M).sum()}, "
      f"sites snapped > {MAX_SNAP_M} m: {(np.asarray(s_snap) > MAX_SNAP_M).sum()}")

site_by_node = {}
for j, (n, sd) in enumerate(zip(s_node, s_snap)):
    if sd <= MAX_SNAP_M:
        site_by_node.setdefault(n, []).append(j)

rows = []
for i, (src, od) in enumerate(zip(o_node, o_snap)):
    if od > MAX_SNAP_M:
        continue
    lengths = nx.single_source_dijkstra_path_length(G, src, cutoff=CUTOFF_M, weight="length")
    for n, path in lengths.items():
        for j in site_by_node.get(n, ()):
            d = od + path + s_snap[j]
            straight = haversine(o.Latitude[i], o.Longitude[i], s.lat[j], s.lon[j])
            d = max(d, straight)
            if d <= CUTOFF_M:
                rows.append((int(o.ID_OHCA[i]), int(j), float(d)))

out = pd.DataFrame(rows, columns=["ID_OHCA", "site_idx", "walk_m"])
out.to_csv("data/walk_pairs.csv", index=False)
print(len(out), "OHCA-site pairs within", CUTOFF_M, "m")
