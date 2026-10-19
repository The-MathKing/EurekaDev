"""Clean OHCAs, attach census tract + SVI, and filter candidate sites to Virginia Beach."""
import geopandas as gpd
import numpy as np
import pandas as pd

RAW = "data/raw"

tracts = gpd.read_file(f"zip://{RAW}/tl_2022_51_tract.zip")
tracts = tracts[tracts.COUNTYFP == "810"][["GEOID", "geometry"]].to_crs(4326)

svi = pd.read_csv(f"{RAW}/Virginia.csv", dtype={"FIPS": str})
svi = svi[svi.FIPS.str.startswith("51810")][["FIPS", "RPL_THEMES", "E_TOTPOP"]]
svi.loc[svi.RPL_THEMES < 0, "RPL_THEMES"] = pd.NA  # -999 = missing
tracts = tracts.merge(svi, left_on="GEOID", right_on="FIPS", how="left")
# Quartiles of vulnerability within Virginia Beach (1 = least, 4 = most vulnerable)
tracts["svi_q"] = pd.qcut(tracts.RPL_THEMES, 4, labels=[1, 2, 3, 4])
tracts.to_file("data/vb_tracts.geojson", driver="GeoJSON")

o = pd.read_excel(f"{RAW}/../VBOHCAR.xlsx", sheet_name="OHCAs")
n0 = len(o)
# Response time of exactly 0 (373 rows) or >60 min (1 row) is treated as missing, not instant.
# Impute from road distance to the nearest first-responder station, fitted on valid rows.
dist = pd.read_excel(f"{RAW}/../VBOHCAR.xlsx", sheet_name="Distances")
nearest = dist.groupby("ID_OHCA")["Road Distance (meters)"].min().rename("nearest_station_m")
o = o.merge(nearest, left_on="ID_OHCA", right_index=True, how="left")
valid = (o.MinimumResponseTime > 0) & (o.MinimumResponseTime <= 60)
fit = o[valid]
b1, b0 = np.polyfit(fit.nearest_station_m / 1000, fit.MinimumResponseTime, 1)
r = np.corrcoef(fit.nearest_station_m, fit.MinimumResponseTime)[0, 1]
print(f"response time ~ {b0:.2f} + {b1:.2f} * km_to_nearest_station  (r = {r:.2f}, n = {len(fit)})")
o["rt_imputed"] = ~valid
o["response_min"] = o.MinimumResponseTime.where(valid, b0 + b1 * o.nearest_station_m / 1000)
print(f"OHCAs: {n0} kept, {(~valid).sum()} response times imputed")
o["Incident_Location"] = o.Incident_Location.str.replace("_x000D_", "", regex=False).str.strip()
og = gpd.GeoDataFrame(o, geometry=gpd.points_from_xy(o.Longitude, o.Latitude), crs=4326)
og = gpd.sjoin(og, tracts[["GEOID", "RPL_THEMES", "svi_q", "geometry"]], how="left", predicate="within")
print("OHCAs without tract:", og.GEOID.isna().sum())
og.drop(columns=["geometry", "index_right"]).to_csv("data/ohcas_clean.csv", index=False)

s = pd.read_csv("data/candidate_sites.csv")
sg = gpd.GeoDataFrame(s, geometry=gpd.points_from_xy(s.lon, s.lat), crs=4326)
sg = gpd.sjoin(sg, tracts[["GEOID", "geometry"]], how="inner", predicate="within")
sg = sg[sg.kind != "defibrillator"]
print("candidate sites inside city tracts:", len(sg), "of", len(s))
sg.drop(columns=["geometry", "index_right"]).to_csv("data/sites_clean.csv", index=False)

print(og.groupby("svi_q", observed=True).agg(n=("ID_OHCA", "size"),
      median_rt=("response_min", "median")).to_string())
