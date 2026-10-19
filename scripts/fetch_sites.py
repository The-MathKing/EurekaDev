"""Fetch candidate AED host sites in Virginia Beach from OpenStreetMap (Overpass API)."""
import json
import requests
import pandas as pd

QUERY = """
[out:json][timeout:180];
area["name"="Virginia Beach"]["boundary"="administrative"]->.vb;
(
  nwr["amenity"~"^(pharmacy|library|fire_station|police|place_of_worship|school|bank|community_centre|townhall|post_office|fuel)$"](area.vb);
  nwr["shop"~"^(supermarket|convenience)$"](area.vb);
  nwr["leisure"~"^(sports_centre|fitness_centre)$"](area.vb);
  nwr["emergency"="defibrillator"](area.vb);
);
out center tags;
"""

resp = requests.post("https://overpass-api.de/api/interpreter", data={"data": QUERY}, timeout=240,
                     headers={"User-Agent": "eurekadev-aed-research/1.0"})
resp.raise_for_status()
elements = resp.json()["elements"]
json.dump(elements, open("data/raw/osm_sites.json", "w"))

rows = []
for e in elements:
    lat = e.get("lat", e.get("center", {}).get("lat"))
    lon = e.get("lon", e.get("center", {}).get("lon"))
    t = e.get("tags", {})
    kind = t.get("amenity") or t.get("shop") or t.get("leisure") or t.get("emergency")
    if t.get("emergency") == "defibrillator":
        kind = "defibrillator"
    rows.append({"osm_id": f"{e['type']}/{e['id']}", "lat": lat, "lon": lon, "kind": kind,
                 "name": t.get("name"), "opening_hours": t.get("opening_hours")})

df = pd.DataFrame(rows).dropna(subset=["lat", "lon"])
df.to_csv("data/candidate_sites.csv", index=False)
print(len(df), "sites")
print(df.kind.value_counts().to_string())
print("with opening_hours:", df.opening_hours.notna().sum())
