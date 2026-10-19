"""Walking-network distances (m) from each OHCA to candidate sites within 1 km, via OSMnx."""
import networkx as nx
import numpy as np
import osmnx as ox
import pandas as pd

CUTOFF_M = 1000

o = pd.read_csv("data/ohcas_clean.csv")
s = pd.read_csv("data/sites_clean.csv")

G = ox.graph_from_place("Virginia Beach, Virginia, USA", network_type="walk")
G = ox.convert.to_undirected(G)
print("walk graph:", G.number_of_nodes(), "nodes", G.number_of_edges(), "edges")

o_node = ox.distance.nearest_nodes(G, o.Longitude.values, o.Latitude.values)
s_node = ox.distance.nearest_nodes(G, s.lon.values, s.lat.values)

site_by_node = {}
for j, n in enumerate(s_node):
    site_by_node.setdefault(n, []).append(j)

rows = []
for i, src in enumerate(o_node):
    lengths = nx.single_source_dijkstra_path_length(G, src, cutoff=CUTOFF_M, weight="length")
    for n, dist in lengths.items():
        for j in site_by_node.get(n, ()):
            rows.append((int(o.ID_OHCA[i]), int(j), float(dist)))

out = pd.DataFrame(rows, columns=["ID_OHCA", "site_idx", "walk_m"])
out.to_csv("data/walk_pairs.csv", index=False)
print(len(out), "OHCA-site pairs within", CUTOFF_M, "m")
