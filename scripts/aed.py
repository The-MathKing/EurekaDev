"""Survival-weighted AED location model for Virginia Beach OHCAs.

Objective: choose p host sites X to maximise
    F(X) = sum_i  max_{j in X, j open at t_i}  g_ij
where g_ij is the gain in survival probability for arrest i if a bystander
fetches the AED at site j instead of waiting for EMS (response time r_i).
F is monotone submodular, so greedy is within (1 - 1/e) of optimal; we also
solve the exact MILP with HiGHS (via scipy).
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.optimize import Bounds, LinearConstraint, milp as _scipy_milp

from hours import availability

DATA = "/Volumes/2TB/eurekadev/data"


@dataclass
class Params:
    walk_speed: float = 1.4      # m/s, bystander retrieval speed
    setup_min: float = 0.5       # min to open cabinet, power on, attach pads
    call_delay: float = 1.0      # min from collapse to 911 call
    ems_defib_min: float = 1.0   # min from EMS arrival to first shock
    max_walk_m: float = 500.0    # one-way walking distance beyond which no one retrieves
    survival: str = "valenzuela"  # or "demaio"
    hours: str = "osm"           # "osm" (opening hours) or "always" (24/7 outdoor cabinet)


def s_valenzuela(i_cpr, i_defib):
    """Valenzuela et al. 1997 (Circulation), witnessed VF arrests; times from collapse (min)."""
    return 1.0 / (1.0 + np.exp(-0.260 + 0.106 * i_cpr + 0.139 * i_defib))


def s_demaio(i_resp):
    """De Maio et al. 2003 (Ann Emerg Med), all treated arrests; time to defibrillation (min)."""
    return 1.0 / (1.0 + np.exp(-0.679 + 0.262 * i_resp))


def load():
    o = pd.read_csv(f"{DATA}/ohcas_clean.csv", parse_dates=["ReceivedTime"])
    s = pd.read_csv(f"{DATA}/sites_clean.csv")
    pairs = pd.read_csv(f"{DATA}/walk_pairs.csv")
    o["idx"] = np.arange(len(o))
    pairs = pairs.merge(o[["ID_OHCA", "idx"]], on="ID_OHCA").rename(columns={"idx": "i", "site_idx": "j"})
    pairs = pairs.groupby(["i", "j"], as_index=False).walk_m.min()
    return o, s, pairs


def survival_gain(walk_m, r, prm: Params):
    """Gain in survival probability from an AED at walking distance walk_m when EMS takes r minutes."""
    c = prm.call_delay
    t_aed = c + 2 * walk_m / prm.walk_speed / 60 + prm.setup_min   # AED on chest
    t_ems = c + r + prm.ems_defib_min                               # EMS shock
    if prm.survival == "valenzuela":
        base = s_valenzuela(c + r, t_ems)
        # Assumes the bystander starts CPR on AED arrival (AED voice prompts) if EMS not yet there.
        with_aed = s_valenzuela(np.minimum(t_aed, c + r), np.minimum(t_aed, t_ems))
    else:
        # De Maio's predictor is the response interval measured from the 911 call.
        base = s_demaio(r)
        with_aed = s_demaio(np.minimum(t_aed - c, r))
    return with_aed - base


def reach_curve(walk_m, rt_sample, prm: Params):
    """Expected gain E_R[survival_gain(d, R)] over an empirical sample of response times."""
    walk_m = np.asarray(walk_m, dtype=float)
    r = np.asarray(rt_sample, dtype=float)
    return survival_gain(walk_m[:, None], r[None, :], prm).mean(axis=1)


def gains(o, s, pairs, prm: Params, rt_sample=None):
    """Return DataFrame (i, j, g) of positive survival gains, respecting opening hours.

    With rt_sample, each arrest's own response time is replaced by the expectation over that
    sample, so g_ij depends only on walking distance (and opening hours).
    """
    p = pairs[pairs.walk_m <= prm.max_walk_m].copy()
    if rt_sample is None:
        p["g"] = survival_gain(p.walk_m.values, o.response_min.values[p.i.values], prm)
    else:
        grid = np.arange(0, prm.max_walk_m + 5, 5.0)
        p["g"] = np.interp(p.walk_m.values, grid, reach_curve(grid, rt_sample, prm))
    if prm.hours == "osm":
        A, _ = availability(s)
        t = o.ReceivedTime.iloc[p.i.values]
        p = p[A[p.j.values, t.dt.weekday.values, t.dt.hour.values]]
    return p[p.g > 1e-9].reset_index(drop=True)


def objective(G, chosen, incidents=None):
    """F(X) restricted to an optional subset of incident indices."""
    g = G[G.j.isin(chosen)]
    if incidents is not None:
        g = g[g.i.isin(incidents)]
    return g.groupby("i").g.max().sum()


def greedy(G, p, candidates=None):
    """Lazy greedy for monotone submodular F; returns ordered list of sites."""
    best = {}  # incident -> current best gain
    by_site = {j: grp[["i", "g"]].values for j, grp in G.groupby("j")}
    if candidates is not None:
        by_site = {j: v for j, v in by_site.items() if j in candidates}
    import heapq
    heap = [(-v[:, 1].sum(), j) for j, v in by_site.items()]
    heapq.heapify(heap)
    chosen = []
    while heap and len(chosen) < p:
        neg, j = heapq.heappop(heap)
        v = by_site[j]
        inc = sum(max(0.0, g - best.get(int(i), 0.0)) for i, g in v)
        if not heap or inc >= -heap[0][0] - 1e-12:
            chosen.append(j)
            for i, g in v:
                if g > best.get(int(i), 0.0):
                    best[int(i)] = g
        else:
            heapq.heappush(heap, (-inc, j))
    return chosen


def milp(G, p, groups=None, floor=0.0, site_bonus=None, time_limit=120):
    """Exact MILP via HiGHS. y_j: open site j; x_k: arrest i(k) served by site j(k).

    site_bonus: optional {site: value}, a tie-breaker scaled so it never outweighs real gain.
    Optional fairness: for each group q (e.g. SVI quartile, given as a Series indexed by
    arrest index), mean gain per arrest in q >= floor.
    """
    sites = np.sort(G.j.unique())
    col = {j: c for c, j in enumerate(sites)}
    ns, nk = len(sites), len(G)
    ii, jj, g = G.i.values, np.array([col[j] for j in G.j.values]), G.g.values
    c = np.concatenate([np.zeros(ns), -g])                  # minimise -F
    if site_bonus is not None:  # tiny tie-breaker, e.g. nearby historical arrest density
        bonus = np.array([site_bonus.get(j, 0.0) for j in sites], dtype=float)
        c[:ns] = -1e-6 * bonus / max(bonus.max(), 1e-12)  # total <= p * 1e-6
    rows = []
    # sum y <= p (F is monotone, so <= p is equivalent to == p when enough sites help)
    rows.append((sp.csr_matrix((np.ones(ns), (np.zeros(ns), np.arange(ns))), shape=(1, ns + nk)), -np.inf, p))
    # x_k - y_j(k) <= 0
    A = sp.csr_matrix((np.concatenate([np.ones(nk), -np.ones(nk)]),
                       (np.concatenate([np.arange(nk)] * 2), np.concatenate([ns + np.arange(nk), jj]))),
                      shape=(nk, ns + nk))
    rows.append((A, -np.inf, 0))
    # each arrest served at most once
    inc, inv = np.unique(ii, return_inverse=True)
    A = sp.csr_matrix((np.ones(nk), (inv, ns + np.arange(nk))), shape=(len(inc), ns + nk))
    rows.append((A, -np.inf, 1))
    if groups is not None and floor > 0:
        # A fixed floor (not one relative to this plan's own total), so the solver can never
        # make a plan look fairer by declining to use benefit in well-served groups.
        q_of = groups.reindex(ii).values
        for q in groups.dropna().unique():
            n_q = (groups == q).sum()
            coef = np.where(q_of == q, g / n_q, 0.0)
            rows.append((sp.csr_matrix(np.concatenate([np.zeros(ns), coef])[None, :]), floor, np.inf))
    cons = [LinearConstraint(A, lb, ub) for A, lb, ub in rows]
    integrality = np.concatenate([np.ones(ns), np.zeros(nk)])
    bounds = Bounds(np.zeros(ns + nk), np.ones(ns + nk))
    res = _scipy_milp(c, constraints=cons, integrality=integrality, bounds=bounds,
               options={"time_limit": time_limit, "mip_rel_gap": 1e-6})
    if res.x is None:
        return [], res.message
    chosen = [int(sites[k]) for k in np.where(res.x[:ns] > 0.5)[0]]
    return chosen, "optimal" if res.status == 0 else res.message
