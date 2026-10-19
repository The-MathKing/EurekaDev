"""All paper figures. Run after exp_cv2, exp_sens2, exp_hours_fair2 and exp_fairness."""
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import json

from aed import Params, load, reach_curve, s_demaio, s_valenzuela

RES = "/Volumes/2TB/eurekadev/results"
FIG = "/Volumes/2TB/eurekadev/figures"
plt.rcParams.update({"font.size": 10, "legend.fontsize": 8.5, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 150, "savefig.bbox": "tight"})
LABELS = {'random': 'Random sites', 'classic MCLP 100 m': 'Classic MCLP (100 m, assumes 24/7)', 'survival, no hours': 'Survival, no opening hours', 'expected survival (main)': 'Expected survival + hours (ours)', 'main, 24/7 cabinets': 'Ours, in 24/7 outdoor cabinets'}
C = {"ours": "#c0392b", "classic": "#2c6fbb", "random": "#9a9a9a", "cab": "#2e8b57"}

o, s, pairs = load()


def fig_survival():
    t = np.linspace(0, 15, 200)
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.plot(t, s_valenzuela(t, t), color=C["ours"], label="Valenzuela et al. 1997 (CPR + shock at t)")
    ax.plot(t, s_valenzuela(1, t), color=C["ours"], ls="--", label="Valenzuela, CPR at 1 min, shock at t")
    ax.plot(t, s_demaio(t), color=C["classic"], label="De Maio et al. 2003 (t from 911 call)")
    r = np.median(o.response_min) + 2
    ax.axvline(r, color="k", lw=0.8, ls=":")
    ax.text(r + 0.3, 0.42, "median EMS shock\nin Virginia Beach", fontsize=8)
    ax.set(xlabel="Minutes from collapse to defibrillation", ylabel="Probability of survival",
           ylim=(0, 0.75), xlim=(0, 15))
    ax.legend(fontsize=7.5, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2)
    fig.savefig(f"{FIG}/fig1_survival.png")


def fig_response():
    fig, ax = plt.subplots(figsize=(5.2, 3))
    r = o.loc[~o.rt_imputed, "response_min"]
    ax.hist(r.clip(upper=20), bins=np.arange(0, 20.5, 0.5), color=C["classic"], alpha=0.85)
    for x, lab in [(8, "8-min standard")]:
        ax.axvline(x, color="k", ls=":", lw=0.9)
        ax.text(x + 0.2, ax.get_ylim()[1] * 0.9, f"{lab}\n{(r > x).mean():.0%} slower", fontsize=8)
    ax.set(xlabel="First-unit EMS response time (min, capped at 20)", ylabel="Cardiac arrests")
    fig.savefig(f"{FIG}/fig2_response_times.png")


def fig_cv():
    d = pd.read_csv(f"{RES}/cv2_results.csv")
    fig, ax = plt.subplots(figsize=(5.6, 3.5))
    styles = [("random", C["random"], "-"), ("classic MCLP 100 m", C["classic"], "-"),
              ("survival, no hours", "#8e6c8a", "-"), ("expected survival (main)", C["ours"], "-"),
              ("main, 24/7 cabinets", C["cab"], "--")]
    for m, col, ls in styles:
        x = d[d.method == m].sort_values("p")
        ax.plot(x.p, x.gain, "o", ls=ls, ms=4, color=col, label=LABELS[m])
        ax.fill_between(x.p, x.ci_lo, x.ci_hi, color=col, alpha=0.12)
    ax.set(xlabel="Number of AEDs placed (p)", ylabel="Out-of-sample survival gain\n(potential survivors, 30 months)",
           xscale="log", xticks=[10, 25, 50, 100, 200])
    ax.set_xticklabels([10, 25, 50, 100, 200])
    ax.legend(fontsize=7.5, frameon=False, loc="upper left")
    fig.savefig(f"{FIG}/fig4_cross_validation.png")


def fig_sensitivity():
    d = pd.read_csv(f"{RES}/sensitivity2.csv")
    base = pd.read_csv(f"{RES}/cv2_results.csv")
    base = base[(base.method == "expected survival (main)") & base.p.isin([25, 50, 100])]
    base = base.assign(scenario="baseline", diff=base.vs_classic, ci_lo=base.vs_classic_lo, ci_hi=base.vs_classic_hi)
    d = pd.concat([base[["scenario", "p", "diff", "ci_lo", "ci_hi"]], d])
    tags = list(dict.fromkeys(d.scenario))
    fig, ax = plt.subplots(figsize=(5.8, 4.4))
    for k, (p, mk) in enumerate([(25, "o"), (50, "s"), (100, "^")]):
        x = d[d.p == p].set_index("scenario").reindex(tags)
        y = np.arange(len(tags)) + (k - 1) * 0.22
        ax.errorbar(x["diff"], y, xerr=[x["diff"] - x.ci_lo, x.ci_hi - x["diff"]], fmt=mk,
                    ms=4, lw=1, capsize=2, label=f"p = {p}")
    ax.axvline(0, color="k", lw=0.8)
    ax.set_yticks(range(len(tags)), tags)
    ax.invert_yaxis()
    ax.set_xlabel("Extra out-of-sample survival gain of ours over classic MCLP\n(95% address-clustered bootstrap CI)")
    ax.legend(frameon=False, loc="lower right")
    fig.savefig(f"{FIG}/fig7_sensitivity.png")


def fig_hours():
    h = pd.read_csv(f"{RES}/hours2.csv")
    cv = pd.read_csv(f"{RES}/cv2_results.csv").set_index(["method", "p"]).gain
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.4), gridspec_kw={"width_ratios": [1.15, 1]})
    x, w = np.arange(len(h)), 0.27
    a1.bar(x - w, h.promised, w, color="#cccccc", label="Promised by hours-blind plan")
    a1.bar(x, h.delivered, w, color=C["classic"], label="Delivered by that plan")
    a1.bar(x + w, [cv[("expected survival (main)", p)] for p in h.p], w, color=C["ours"],
           label="Hours-aware plan (ours)")
    a1.set_xticks(x, h.p)
    a1.set(xlabel="Number of AEDs (p)", ylabel="Out-of-sample survival gain\n(potential survivors)")
    a1.legend(fontsize=7.5, frameon=False, loc="upper left")
    pr = pd.read_csv(f"{RES}/hours_profile2.csv")
    pr["block"] = pr.hour // 3
    labels = [f"{3 * b:02d}-{3 * b + 3:02d}" for b in range(8)]
    top = 0
    for k, (name, col) in enumerate([("indoor (opening hours)", C["ours"]), ("24/7 outdoor cabinet", C["cab"])]):
        q = pr[pr.scenario == name].groupby("block")[["gain", "arrests"]].sum()
        vals = q.gain / q.arrests * 100
        top = max(top, vals.max())
        a2.bar(np.arange(8) + (k - 0.5) * 0.4, vals, 0.4, color=col, label=name)
    a2.set_ylim(0, top * 1.35)
    a2.legend(fontsize=7.5, frameon=False, loc="upper left", ncol=2)
    a2.set_xticks(range(8), labels, rotation=45, fontsize=8)
    a2.set(xlabel="Time of 911 call", ylabel="Gain per 100 arrests")
    a2.set_title("p = 50, out-of-sample", fontsize=9)
    fig.savefig(f"{FIG}/fig5_opening_hours.png")


def fig_fairness():
    d = pd.read_csv(f"{RES}/fairness.csv")
    fo = pd.read_csv(f"{RES}/fairness_oos.csv")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.4))
    for p, col in [(25, "#7f8c8d"), (50, C["ours"]), (100, "#34495e")]:
        x = d[d.p == p]
        a1.plot(x.min_ratio, x.price_of_fairness * 100, "o-", ms=3.5, color=col, label=f"p = {p}")
    a1.set(xlabel="Worst-served quartile / citywide average", ylabel="Price of fairness\n(% of total gain, in-sample)")
    a1.legend(frameon=False)
    q = np.arange(1, 5)
    rows = [fo[fo.phi == 0].iloc[0], fo[fo.phi == 0.85].iloc[0]]
    for k, (r, lab, col) in enumerate(zip(rows, ["Unconstrained", "Fairness floor φ = 0.85"], ["#bbbbbb", C["ours"]])):
        a2.bar(q + (k - 0.5) * 0.38, [r[f"q{v}_per100"] for v in q], 0.38, color=col, label=lab)
    a2.set_xticks(q, ["Q1\nleast", "Q2", "Q3", "Q4\nmost"])
    a2.set(xlabel="Social Vulnerability Index quartile", ylabel="Out-of-sample gain\nper 100 arrests")
    a2.set_ylim(0, max(fo[[f"q{v}_per100" for v in q]].max()) * 1.4)
    a2.legend(frameon=False, loc="upper left", ncol=2, fontsize=7.5)
    a2.set_title("p = 50", fontsize=9)
    fig.savefig(f"{FIG}/fig6_fairness.png")


def fig_map():
    from matplotlib.lines import Line2D
    tracts = gpd.read_file("/Volumes/2TB/eurekadev/data/vb_tracts.geojson")
    sites = json.load(open(f"{RES}/cv2_sites.json"))
    picks = [("Classic MCLP (50 AEDs)", sites["classic MCLP 100 m|50"]["4"], C["classic"]),
             ("Expected survival + hours (50 AEDs)", sites["expected survival (main)|50"]["4"], C["ours"])]
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.0), sharex=True, sharey=True)
    fig.subplots_adjust(wspace=0.02, bottom=0.08)
    for ax, (title, sel, col) in zip(axes, picks):
        tracts.plot(ax=ax, color="#f2f2f2", edgecolor="white", lw=0.3)
        tracts.dropna(subset=["RPL_THEMES"]).plot(ax=ax, column="RPL_THEMES", cmap="Greys", alpha=0.45,
                                                  edgecolor="white", lw=0.3)
        sc = ax.scatter(o.Longitude, o.Latitude, c=o.response_min.clip(upper=15), cmap="YlOrRd", s=4,
                        alpha=0.7, vmin=2, vmax=15, lw=0)
        ss = s.iloc[sel]
        ax.scatter(ss.lon, ss.lat, marker="^", s=38, color=col, edgecolor="k", lw=0.6)
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
        ax.set_ylim(36.68, 36.94)
        ax.set_xlim(-76.23, -75.94)
        # 5 km scale bar (1 degree of longitude here is about 89.2 km)
        x0, y0 = -76.21, 36.695
        ax.plot([x0, x0 + 5 / 89.2], [y0, y0], color="k", lw=2)
        ax.text(x0 + 2.5 / 89.2, y0 + 0.004, "5 km", ha="center", fontsize=7.5)
    handles = [Line2D([], [], marker="^", ls="", color=C["classic"], mec="k", label="AED (classic)"),
               Line2D([], [], marker="^", ls="", color=C["ours"], mec="k", label="AED (ours)"),
               plt.Rectangle((0, 0), 1, 1, color="#888888", alpha=0.6, label="High social vulnerability"),
               plt.Rectangle((0, 0), 1, 1, color="#eeeeee", label="Low social vulnerability")]
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.45, 0.06), ncol=4, frameon=False, fontsize=8)
    cb = fig.colorbar(sc, ax=axes, shrink=0.55, pad=0.01)
    cb.set_label("EMS response time (min)")
    fig.savefig(f"{FIG}/fig3_map.png", dpi=200)


def fig_reach():
    v = o.response_min[~o.rt_imputed].values
    d = np.arange(0, 501, 5)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 3.3))
    for speed, ls in [(1.0, ":"), (1.4, "-"), (2.0, "--")]:
        f = reach_curve(d, v, Params(walk_speed=speed))
        a1.plot(d, f * 100, color=C["ours"], ls=ls, label=f"walk {speed} m/s")
    f = reach_curve(d, v, Params())
    half = np.interp(f[0] / 2, f[::-1], d[::-1])
    a1.axvline(half, color="k", lw=0.7, ls=":")
    a1.text(half + 8, f[0] * 100 * 0.62, f"half value\nat {half:.0f} m", fontsize=8)
    a1.step([0, 100, 100, 500], [f[0] * 100 * 0.6] * 2 + [0, 0], where="post", color=C["classic"],
            lw=1, label="100 m rule (shape only)")
    a1.set(xlabel="Walking distance to AED (m)", ylabel="Expected survival gain\n(percentage points)")
    a1.legend(fontsize=7.5, frameon=False)
    cv = pd.read_csv(f"{RES}/cv2_results.csv")
    for m, col in [("expected survival (main)", C["ours"]), ("main, 24/7 cabinets", C["cab"])]:
        x = cv[cv.method == m].sort_values("p")
        a2.plot(x.p, x.gain, "o-", color=col, label="Indoor AEDs (opening hours)" if "main)" in m else "24/7 outdoor cabinets")
        a2.fill_between(x.p, x.ci_lo, x.ci_hi, color=col, alpha=0.12)
    ind = cv[cv.method == "expected survival (main)"].set_index("p").gain
    cab = cv[cv.method == "main, 24/7 cabinets"].set_index("p").gain
    a2.plot([25, 50], [cab[25], ind[50]], color="k", lw=0.8, ls=":")
    a2.text(55, ind[50] - 7, f"25 cabinets ({cab[25]:.1f}) ≈\n50 indoor ({ind[50]:.1f})", fontsize=8)
    a2.set(xlabel="Number of AEDs (p)", ylabel="Out-of-sample survival gain\n(potential survivors)",
           xscale="log", xticks=[10, 25, 50, 100, 200])
    a2.set_xticklabels([10, 25, 50, 100, 200])
    a2.legend(fontsize=7.5, frameon=False, loc="upper left")
    fig.savefig(f"{FIG}/fig8_reach_cabinets.png")


if __name__ == "__main__":
    import sys
    todo = sys.argv[1:] or ["survival", "response", "cv", "sensitivity", "hours", "fairness", "map", "reach"]
    for name in todo:
        globals()[f"fig_{name}"]()
        print("saved", name)
