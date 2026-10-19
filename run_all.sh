#!/usr/bin/env bash
# Reproduce every result and figure in the paper from public data (about 1-2 hours).
set -euo pipefail
cd "$(dirname "$0")"
PY="$(pwd)/.venv/bin/python"
bash scripts/download_data.sh
$PY scripts/fetch_sites.py                       # OpenStreetMap candidate sites
$PY scripts/fetch_facilities.py                  # hospitals / care facilities (for checks)
$PY scripts/prepare.py                           # clean arrests, impute missing response times, attach SVI
$PY scripts/walk_distances.py > data/walk_log.txt   # walking-network distances (OSMnx)
cd scripts
$PY exp_cv2.py              # main out-of-sample comparison, all baselines (Tables 2-4, Figs 4, 8)
$PY exp_sens2.py            # robustness scenarios (Fig 7)
$PY exp_hours_fair2.py      # out-of-sample opening hours and fairness (Table 3, Figs 5, 6)
$PY exp_fairness.py         # in-sample price of fairness and the feasibility bound (Fig 6)
$PY exp_smoothed_rt2.py     # place-based response time and own-vs-median check (Section 5.3)
$PY exp_descriptives.py     # R^2, quartile geography, greedy vs exact, 100 m coverage, reach curve
$PY figures.py
$PY export_prototype.py     # interactive map
cd ../paper && pdflatex -interaction=nonstopmode paper.tex >/dev/null && pdflatex -interaction=nonstopmode paper.tex >/dev/null
echo "done: paper/paper.pdf, prototype/index.html"
