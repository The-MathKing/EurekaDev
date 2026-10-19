"""All paper figures. Run after exp_cv, exp_fairness, exp_hours, exp_sensitivity."""
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from aed import Params, gains, load, milp, s_demaio, s_valenzuela

RES = "/Volumes/2TB/eurekadev/results"
FIG = "/Volumes/2TB/eurekadev/figures"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 150, "savefig.bbox": "tight"})
C = {"ours": "#c0392b", "classic": "#2c6fbb", "random": "#9a9a9a", "cab": "#2e8b57"}

o, s, pairs = load()


def fig_survival():
    t = np.linspace(0, 15, 200)
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.plot(t, s_valenzuela(t, t), color=C["ours"], label="Valenzuela et al. 1997 (CPR + shock at t)")
    ax.plot(t, s_valenzuela(1, t), color=C["ours"], ls="--", label="Valenzuela, CPR at 1 min, shock at t")
    ax.plot(t, s_demaio(t), color=C["classic"], label="De Maio et al. 2003")
    r = np.median(o.response_min) + 2
    ax.axvline(r, color="k", lw=0.8, ls=":")
    ax.annotate("median EMS shock\nin Virginia Beach", (r, 0.55), xytext=(r + 0.6, 0.55), fontsize=8)
    ax.set(xlabel="Minutes from collapse to defibrillation", ylabel="Probability of survival",
           ylim=(0, 0.75), xlim=(0, 15))
    ax.legend(fontsize=7.5, frameon=False)
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
    d = pd.read_csv(f"{RES}/cv_results.csv")
    fig, ax = plt.subplots(figsize=(5.2, 3.3))
    for m, key in [("survival-weighted", "ours"), ("classic MCLP", "classic"), ("random", "random")]:
        x = d[d.method == m].sort_values("p")
        lab = {"survival-weighted": "Survival-weighted, hours-aware (ours)",
               "classic MCLP": "Classic MCLP (100 m, assumes 24/7)", "random": "Random sites"}[m]
        ax.plot(x.p, x.oos_gain, "o-", color=C[key], label=lab)
        ax.fill_between(x.p, x.ci_lo, x.ci_hi, color=C[key], alpha=0.15)
    ax.set(xlabel="Number of AEDs placed (p)", ylabel="Out-of-sample survival gain\n(potential survivors, 2.5 yrs)",
           xscale="log", xticks=[10, 25, 50, 100, 200])
    ax.set_xticklabels([10, 25, 50, 100, 200])
    ax.legend(fontsize=8, frameon=False)
    fig.savefig(f"{FIG}/fig4_cross_validation.png")


def fig_sensitivity():
    d = pd.read_csv(f"{RES}/sensitivity.csv")
    base = pd.read_csv(f"{RES}/cv_results.csv").assign(tag="baseline")
    d = pd.concat([base[base.p.isin([25, 50, 100])], d])
    d = d[d.method == "ours minus classic"]
    tags = list(dict.fromkeys(d.tag))
    fig, ax = plt.subplots(figsize=(5.6, 4))
    for k, (p, mk) in enumerate([(25, "o"), (50, "s"), (100, "^")]):
        x = d[d.p == p].set_index("tag").reindex(tags)
        y = np.arange(len(tags)) + (k - 1) * 0.22
        ax.errorbar(x.oos_gain, y, xerr=[x.oos_gain - x.ci_lo, x.ci_hi - x.oos_gain], fmt=mk,
                    ms=4, lw=1, capsize=2, label=f"p = {p}")
    ax.axvline(0, color="k", lw=0.8)
    ax.set_yticks(range(len(tags)), tags)
    ax.invert_yaxis()
    ax.set_xlabel("Extra survival gain of ours over classic MCLP\n(95% bootstrap CI)")
    ax.legend(fontsize=8, frameon=False, loc="lower right")
    fig.savefig(f"{FIG}/fig7_sensitivity.png")


def fig_hours():
    d = pd.read_csv(f"{RES}/hours.csv")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 3.2), gridspec_kw={"width_ratios": [1.1, 1]})
    x, w = np.arange(len(d)), 0.2
    a1.bar(x - 1.5 * w, d.naive_planned, w, color="#cccccc", label="Promised (plan assumes 24/7)")
    a1.bar(x - 0.5 * w, d.naive_realized, w, color=C["classic"], label="Delivered by that plan")
    a1.bar(x + 0.5 * w, d.hours_aware_realized, w, color=C["ours"], label="Hours-aware plan (ours)")
    a1.bar(x + 1.5 * w, d.cabinet_realized, w, color=C["cab"], label="24/7 outdoor cabinets")
    a1.set_xticks(x, d.p)
    a1.set(xlabel="Number of AEDs (p)", ylabel="Survival gain (potential survivors)")
    a1.legend(fontsize=7, frameon=False)
    pr = pd.read_csv(f"{RES}/hours_profile.csv")
    pr["block"] = pr.hour // 3
    labels = [f"{3 * b:02d}-{3 * b + 3:02d}" for b in range(8)]
    for k, (name, col) in enumerate([("indoor (opening hours)", C["ours"]), ("24/7 outdoor cabinet", C["cab"])]):
        q = pr[pr.scenario == name].groupby("block")[["gain", "arrests"]].sum()
        a2.bar(np.arange(8) + (k - 0.5) * 0.4, q.gain / q.arrests * 100, 0.4, color=col, label=name)
    a2.legend(fontsize=7.5, frameon=False, loc="upper left")
    a2.set_xticks(range(8), labels, rotation=45, fontsize=8)
    a2.set(xlabel="Time of 911 call", ylabel="Gain per 100 arrests")
    a2.set_title("p = 50", fontsize=9)
    fig.savefig(f"{FIG}/fig5_opening_hours.png")


def fig_fairness():
    d = pd.read_csv(f"{RES}/fairness.csv")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.4, 3.2))
    for p, col in [(25, "#7f8c8d"), (50, C["ours"]), (100, "#34495e")]:
        x = d[d.p == p]
        a1.plot(x.min_ratio, x.price_of_fairness * 100, "o-", ms=3, color=col, label=f"p = {p}")
    a1.set(xlabel="Worst-served quartile, relative to citywide average", ylabel="Price of fairness (% of total gain)")
    a1.legend(fontsize=8, frameon=False)
    x = d[d.p == 50]
    fair = x[x.phi == x.phi.max()].iloc[0]
    rows = [x[x.phi == 0].iloc[0], fair]
    q = np.arange(1, 5)
    labs = ["Unconstrained", f"Strictest feasible fairness (φ = {fair.phi:.2f})"]
    for k, (r, lab, col) in enumerate(zip(rows, labs, ["#bbbbbb", C["ours"]])):
        a2.bar(q + (k - 0.5) * 0.38, [r[f"q{v}.0_per_arrest"] * 100 for v in q], 0.38, color=col, label=lab)
    a2.set_xticks(q, ["Q1\nleast", "Q2", "Q3", "Q4\nmost"])
    a2.set(xlabel="Social Vulnerability Index quartile", ylabel="Gain per 100 arrests", ylim=(0, 2.3))
    a2.legend(fontsize=8, frameon=False, loc="upper left")
    a2.set_title("p = 50", fontsize=9)
    fig.savefig(f"{FIG}/fig6_fairness.png")


def fig_map():
    tracts = gpd.read_file("/Volumes/2TB/eurekadev/data/vb_tracts.geojson")
    G = gains(o, s, pairs, Params())
    G_mclp = pairs[pairs.walk_m <= 100].assign(g=1.0)
    density = pairs.groupby("j").size().to_dict()
    ours, _ = milp(G, 50, site_bonus=density)
    classic, _ = milp(G_mclp, 50, site_bonus=density)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.6), sharex=True, sharey=True)
    for ax, sel, title, col in [(axes[0], classic, "Classic MCLP (50 AEDs)", C["classic"]),
                                (axes[1], ours, "Survival-weighted, hours-aware (50 AEDs)", C["ours"])]:
        tracts.plot(ax=ax, color="#f2f2f2", edgecolor="white", lw=0.3)
        tracts.dropna(subset=["RPL_THEMES"]).plot(ax=ax, column="RPL_THEMES", cmap="Greys", alpha=0.45,
                                                  edgecolor="white", lw=0.3)
        sc = ax.scatter(o.Longitude, o.Latitude, c=o.response_min.clip(upper=15), cmap="YlOrRd", s=4,
                        alpha=0.7, vmin=2, vmax=15, lw=0)
        ss = s.iloc[sel]
        ax.scatter(ss.lon, ss.lat, marker="^", s=38, color=col, edgecolor="k", lw=0.6, label="AED site")
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
        ax.set_ylim(36.68, 36.94)
        ax.set_xlim(-76.23, -75.94)
        ax.legend(loc="lower left", fontsize=8, frameon=False)
    cb = fig.colorbar(sc, ax=axes, shrink=0.55, pad=0.01)
    cb.set_label("EMS response time (min)")
    fig.text(0.13, 0.04, "Grey shading: CDC Social Vulnerability Index (darker = more vulnerable). "
             "Dots: cardiac arrests 2017-2019.", fontsize=8)
    fig.savefig(f"{FIG}/fig3_map.png", dpi=200)


if __name__ == "__main__":
    import sys
    todo = sys.argv[1:] or ["survival", "response", "cv", "sensitivity", "hours", "fairness", "map"]
    for name in todo:
        globals()[f"fig_{name}"]()
        print("saved", name)
