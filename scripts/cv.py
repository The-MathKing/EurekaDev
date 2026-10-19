"""Shared out-of-sample evaluation: 5 half-year folds, training-only tie-breaks, equal budgets.

A "method" is a function (o, train_mask) -> gain table G restricted to training arrests.
Every method's chosen sites are scored on held-out arrests with the same evaluation table.
"""
import numpy as np
import pandas as pd

from aed import Params, gains, load, milp

N_FOLDS = 5


def setup():
    o, s, pairs = load()
    o["fold"] = ((o.ReceivedTime.dt.year - 2017) * 2 + (o.ReceivedTime.dt.month > 6)).values
    o["cluster"] = o.groupby(["Latitude", "Longitude"]).ngroup()
    return o, s, pairs


def train_density(pairs, train_idx):
    """Tie-breaker: number of TRAINING arrests within walking range of each site."""
    return pairs[pairs.i.isin(train_idx)].groupby("j").size().to_dict()


def choose(G_train, p, n_sites, density, **kw):
    """Exact MILP, then fill any unused budget with the busiest remaining sites (equal budgets)."""
    sel, status = milp(G_train, p, site_bonus=density, **kw) if len(G_train) else ([], "empty")
    if len(sel) < p:
        rest = sorted((j for j in range(n_sites) if j not in set(sel)),
                      key=lambda j: (-density.get(j, 0), j))
        sel = list(sel) + rest[: p - len(sel)]
    return sel, status


def score(G_eval, sel, test_idx, n):
    """Per-arrest realised gain (array of length n) for held-out arrests."""
    v = np.zeros(n)
    g = G_eval[G_eval.j.isin(sel) & G_eval.i.isin(test_idx)]
    best = g.groupby("i").g.max()
    v[best.index] = best.values
    return v


def run_cv(o, s, pairs, methods, p_values, G_eval, G_cov=None, eval_overrides=None):
    """Return dict (method, p) -> {"gain": per-arrest array, "cov": per-arrest 0/1, "sites": per-fold lists}."""
    n = len(o)
    eval_overrides = eval_overrides or {}
    out = {}
    for f in range(N_FOLDS):
        tr = o.idx[o.fold != f].values
        te = o.idx[o.fold == f].values
        dens = train_density(pairs, tr)
        tables = {name: fn(o, o.fold.values != f) for name, fn in methods.items()}
        for name, Gt in tables.items():
            Gt = Gt[Gt.i.isin(tr)]
            Ge = eval_overrides.get(name, G_eval)
            for p in p_values:
                sel, _ = choose(Gt, p, len(s), dens)
                rec = out.setdefault((name, p), {"gain": np.zeros(n), "cov": np.zeros(n), "sites": {}})
                rec["gain"] += score(Ge, sel, te, n)
                if G_cov is not None:
                    rec["cov"] += score(G_cov, sel, te, n)
                rec["sites"][f] = sel
    return out


def cluster_boot(o, arrays, n_boot=2000, seed=2026):
    """Sums of each array over a bootstrap that resamples address clusters (shared coordinates)."""
    rng = np.random.default_rng(seed)
    cl = o.cluster.values
    k = cl.max() + 1
    sums = {key: np.bincount(cl, weights=a, minlength=k) for key, a in arrays.items()}
    draws = rng.integers(0, k, size=(n_boot, k))
    counts = np.stack([np.bincount(d, minlength=k) for d in draws])
    return {key: counts @ v for key, v in sums.items()}
