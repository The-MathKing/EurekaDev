"""Devpost thumbnail (3:2, 1500x1000): map of arrests and chosen AED sites with headline numbers."""
import json

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch

ROOT = "/Volumes/2TB/eurekadev"
BG, INK, MUTED = "#0d1321", "#f4f1ea", "#9aa3b5"
RED, AMBER, GREEN = "#ff4d4d", "#ffb347", "#3ddc97"

o = pd.read_csv(f"{ROOT}/data/ohcas_clean.csv")
s = pd.read_csv(f"{ROOT}/data/sites_clean.csv")
tracts = gpd.read_file(f"{ROOT}/data/vb_tracts.geojson")
sel = json.load(open(f"{ROOT}/results/cv2_sites.json"))["expected survival (main)|50"]["4"]

fig = plt.figure(figsize=(15, 10), dpi=100, facecolor=BG)

# Map panel (right)
ax = fig.add_axes([0.50, 0.10, 0.49, 0.86], facecolor=BG)
tracts.plot(ax=ax, color="#16203a", edgecolor="#24304f", lw=0.6)
slow = o.response_min >= 8
ax.scatter(o.Longitude[~slow], o.Latitude[~slow], s=7, color=AMBER, alpha=0.35, lw=0)
ax.scatter(o.Longitude[slow], o.Latitude[slow], s=9, color=RED, alpha=0.55, lw=0)
ss = s.iloc[sel]
ax.scatter(ss.lon, ss.lat, s=900, color=GREEN, alpha=0.10, lw=0)
ax.scatter(ss.lon, ss.lat, s=260, color=GREEN, alpha=0.22, lw=0)
ax.scatter(ss.lon, ss.lat, s=70, color=GREEN, edgecolor="white", lw=1.4, zorder=5)
ax.set_xlim(-76.23, -75.94)
ax.set_ylim(36.68, 36.94)
ax.set_aspect(1 / 0.80)
ax.set_axis_off()

# Text panel (left)
fig.text(0.05, 0.90, "EUREKADEV 2026  ·  RESEARCH  ·  MATH & PHYSICS", color=GREEN, fontsize=15,
         fontweight="bold", family="DejaVu Sans")
fig.text(0.05, 0.63, "Where Should\nthe Defibrillators\nGo?", color=INK, fontsize=52, fontweight="bold",
         linespacing=1.05, va="bottom")
fig.text(0.05, 0.585, "Optimizing public AED placement from\n2,706 real cardiac arrests in Virginia Beach",
         color=MUTED, fontsize=18, va="top", linespacing=1.35)

stats = [("+42–67%", "more expected survival than the standard covering model"),
         ("1 cabinet ≈ 2 AEDs", "a 24/7 outdoor AED is worth about two indoor ones"),
         ("123 m", "walk at which an AED loses half its life-saving value")]
y = 0.445
for big, small in stats:
    fig.patches.append(FancyBboxPatch((0.05, y - 0.105), 0.40, 0.105, boxstyle="round,pad=0.004,rounding_size=0.012",
                                      transform=fig.transFigure, facecolor="#16203a", edgecolor="#24304f", lw=1.2))
    fig.text(0.068, y - 0.037, big, color=GREEN, fontsize=26, fontweight="bold", va="center")
    fig.text(0.068, y - 0.081, small, color=INK, fontsize=13.5, va="center")
    y -= 0.13

# Legend chips on the map
lx, ly = 0.55, 0.075
for col, lab in [(RED, "arrest, EMS > 8 min"), (AMBER, "arrest, EMS ≤ 8 min"), (GREEN, "AED site chosen")]:
    fig.text(lx, ly, "●", color=col, fontsize=16, va="center")
    fig.text(lx + 0.016, ly, lab, color=MUTED, fontsize=12.5, va="center")
    lx += 0.15

fig.savefig(f"{ROOT}/submission/thumbnail.png", facecolor=BG, dpi=100)
print("saved")
