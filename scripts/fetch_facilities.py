"""Hospitals and residential care facilities in Virginia Beach (OSM) for flagging OHCAs."""
import requests
import pandas as pd

QUERY = """
[out:json][timeout:120];
area["name"="Virginia Beach"]["boundary"="administrative"]->.vb;
(
  nwr["amenity"="hospital"](area.vb);
  nwr["healthcare"="hospital"](area.vb);
  nwr["amenity"~"^(nursing_home|social_facility)$"](area.vb);
  nwr["social_facility"~"^(nursing_home|assisted_living|group_home)$"](area.vb);
  nwr["healthcare"="nursing_home"](area.vb);
);
out center tags;
"""
r = requests.post("https://overpass-api.de/api/interpreter", data={"data": QUERY}, timeout=180,
                  headers={"User-Agent": "eurekadev-aed-research/1.0"})
r.raise_for_status()
rows = []
for e in r.json()["elements"]:
    t = e.get("tags", {})
    hosp = t.get("amenity") == "hospital" or t.get("healthcare") == "hospital"
    rows.append({"lat": e.get("lat", e.get("center", {}).get("lat")),
                 "lon": e.get("lon", e.get("center", {}).get("lon")),
                 "type": "hospital" if hosp else "care_facility", "name": t.get("name")})
df = pd.DataFrame(rows).dropna(subset=["lat"])
df.to_csv("data/facilities.csv", index=False)
print(df.type.value_counts().to_string())
print(df.to_string())
