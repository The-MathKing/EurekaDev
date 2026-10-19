# Where Should the Defibrillators Go?

Survival-based, opening-hours-aware and fairness-constrained placement of public AEDs (automated external defibrillators), built entirely from open data for Virginia Beach, VA.

EurekaDev 2026, Research Track (Math & Physics). The paper is [paper/paper.pdf](paper/paper.pdf), and the interactive map is [prototype/index.html](prototype/index.html), a single HTML file you can open in any browser.

## Key findings

The data are 2,706 cardiac arrests in Virginia Beach, 2017–2019.

1. **Survival-based placement beats the standard method.** On arrests the model never saw, choosing sites to maximize expected survival gives 42–67% more benefit than the classic maximal covering location problem (MCLP), for 25–200 AEDs. It also beats stronger baselines in the style of Sun et al. 2016 and Pourghaderi et al. 2021. Validation uses 5-fold temporal cross-validation with address-clustered bootstrap confidence intervals. The advantage holds in all 30 robustness checks.
2. **Opening hours matter a lot.** A plan that assumes every AED is reachable 24/7 overstates its real benefit by 67–106% on held-out arrests. 24/7 outdoor cabinets deliver 41–63% more than indoor AEDs: one cabinet is worth about two indoor AEDs.
3. **Steering AEDs toward historically slow EMS does not help.** Location explains only about 7% of the variation in response time. So the model averages over the city's response-time distribution, which gives a derived "reach curve": an AED loses half its value within about 123 m of walking.
4. **Fairness is cheap but has a hard ceiling.** A fairness floor across Social Vulnerability Index quartiles had no detectable out-of-sample cost. A simple bound, proved in the paper, shows that full parity is impossible with building-hosted AEDs alone.

## The model

For arrest *i* and candidate site *j*, the survival gain *g_ij* is the survival probability if a bystander fetches the AED at *j* minus the survival probability when waiting for EMS. It uses the Valenzuela et al. (1997) logistic survival curve, the real walking distance, the EMS response time, and whether site *j* is open at the time of the call. We choose *p* sites to maximize

    F(X) = sum over arrests i of  max over j in X of  g_ij

*F* is monotone submodular, so greedy is guaranteed at least 63% (1 − 1/e) of optimal. We solve the problem exactly as a mixed-integer program with HiGHS.

## Reproduce

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
./run_all.sh          # downloads data, runs every experiment, rebuilds figures, paper and prototype
```

Building the paper needs a LaTeX installation (`pdflatex`). The full run takes about 30–60 minutes, most of it the walking-network download and the cross-validation.

## Layout

| Path | Contents |
|---|---|
| `scripts/aed.py` | Core model: survival gains, greedy solver, exact MILP, fairness constraints |
| `scripts/hours.py` | Opening-hours parser (OSM `opening_hours`) and category defaults |
| `scripts/prepare.py` | Cleans arrests, imputes missing response times, attaches census tract and SVI |
| `scripts/fetch_sites.py` | Candidate host sites from OpenStreetMap |
| `scripts/walk_distances.py` | Walking-network distances with OSMnx |
| `scripts/exp_*.py` | Experiments: cross-validation, sensitivity, ablation, hours, fairness |
| `scripts/figures.py` | All paper figures |
| `scripts/export_prototype.py` | Builds the interactive map |
| `results/` | CSV outputs of every experiment |
| `research/lit_notes.md` | Literature notes with verified citations |

## Data sources

All data are public.

- **Cardiac arrests:** Custodio & Lejeune (2022), *INFORMS Journal on Computing* 34(1):4–10, [github.com/INFORMSJoC/2020.1022](https://github.com/INFORMSJoC/2020.1022).
- **Candidate sites, opening hours and walking network:** © OpenStreetMap contributors (ODbL).
- **Social Vulnerability Index 2022:** CDC/ATSDR.
- **Census tract boundaries:** U.S. Census Bureau TIGER/Line 2022.

## Limitations

The data record dispatches, not confirmed arrests, so they don't say whether an arrest was witnessed or what the heart rhythm was. Most opening hours (720 of 929 sites) are assumed by category. Survival curves come from published studies, not local outcomes. Results are in "potential survivors", which assumes every arrest is witnessed, shockable and has a willing bystander. See Section 6 of the paper.
