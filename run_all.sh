#!/usr/bin/env bash
# Reproduce every result and figure from public data (about 30-60 minutes).
set -euo pipefail
cd "$(dirname "$0")"
PY=.venv/bin/python
bash scripts/download_data.sh
$PY scripts/fetch_sites.py          # OpenStreetMap candidate sites
$PY scripts/fetch_facilities.py     # hospitals / care facilities (for checks)
$PY scripts/prepare.py              # clean arrests, impute missing response times, attach SVI
$PY scripts/walk_distances.py       # walking-network distances (OSMnx)
cd scripts
../$PY exp_main.py                  # single train/test split + greedy vs exact
../$PY exp_cv.py                    # 5-fold temporal cross-validation
../$PY exp_sensitivity.py           # robustness scenarios
../$PY exp_ablation.py              # which ingredient matters
../$PY exp_smoothed_rt.py           # place-based response time
../$PY exp_hours.py                 # opening hours vs 24/7 cabinets
../$PY exp_fairness.py              # price of fairness
../$PY figures.py
../$PY export_prototype.py          # interactive map
cd ../paper && pdflatex -interaction=nonstopmode paper.tex >/dev/null && pdflatex -interaction=nonstopmode paper.tex >/dev/null
echo "done: paper/paper.pdf, prototype/index.html"
