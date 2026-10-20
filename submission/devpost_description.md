## Inspiration

Every year, around 137,000 Americans suffer a cardiac arrest outside of a hospital, and about nine out of ten do not survive (CARES 2024). When a bystander steps in with an automated external defibrillator (AED) before EMS arrives, the patient's chances of survival basically double (Weisfeldt 2010; Pollack 2018). Yet lay bystanders attach an AED in barely 12.6% of public arrests nationwide.

The problem is practical: the closest AED is almost always too far away to sprint to, or it sits locked behind closed doors on an evening or weekend. I wanted to see if mathematical optimization and open data could answer a question that saves lives: **where should a city put its public defibrillators so bystanders can actually reach them in time?**

## What it does

This research project brings together spatial optimization, probability, and open data to solve prospective AED placement. Using 2,706 geo-referenced cardiac arrests in Virginia Beach, VA (2017–2019; Custodio & Lejeune 2022), I:

- **Built a survival-based placement model:** Rather than drawing arbitrary 100-meter straight-line circles, the model evaluates 929 real-world candidate host facilities (pharmacies, churches, schools, convenience stores, and gas stations from OpenStreetMap). For each arrest, it computes the expected survival gain over actual pedestrian street networks, taking into account empirical EMS response times, published clinical survival curves (Valenzuela et al. 1997), and whether the host building was open at the exact time of the 911 call.
- **Proved the objective is monotone submodular:** This mathematical property guarantees that a fast greedy algorithm achieves at least 63.2% ($1 - 1/e$) of the theoretical optimum. In practice, greedy reached over 99.9% of optimality compared to the exact mixed-integer linear programming (MILP) solution.
- **Enforced neighborhood equity:** I integrated a fairness constraint across CDC Social Vulnerability Index (SVI) quartiles, evaluated its "price of fairness", and proved an asymptotic feasibility bound showing why low-density suburban areas cannot achieve full parity with indoor units alone.

## Key findings

When it comes to placing automated external defibrillators, the goal is saving lives. A survival-based approach delivers major, measurable advantages:

1. **Survival-based placement increases expected survival benefit by 42–67% on unseen arrests** compared to the standard maximal covering model (MCLP) across budgets of 25–200 AEDs (+42% at 25, +63% at 50, +67% at 100, +46% at 200). In 5-fold temporal cross-validation with address-clustered bootstrap confidence intervals, it beats classic covering across all 30 robustness checks and outperforms stronger literature baselines.
2. **Ignoring opening hours makes a plan seem 67–106% more effective than it actually delivers.** Conversely, placing AEDs in 24/7 accessible outdoor cabinets yields 41–63% more benefit than indoor units. In operational terms, **one outdoor cabinet is worth roughly two indoor AEDs**.
3. **Placing AEDs where ambulances were historically slow does not help.** Location only accounts for about 7% of the variation in response times ($R^2 = 0.07$). Averaging over the empirical response-time distribution yields a derived "reach curve" showing how an AED's clinical value declines with distance—losing half its value within about 123 meters of walking and approaching zero by 500 meters.
4. **Fairness is inexpensive, but structural urban geography sets a hard ceiling.** Guaranteeing 85–90% parity across vulnerability quartiles carried no detectable out-of-sample efficiency loss. However, because candidate host facilities are sparse in low-density suburban tracts ($Q_1$ has 0.88 sites/km² vs. 3.0 in urban tracts), full parity is mathematically impossible using building-hosted units alone ($C_1/T_\infty \approx 81\%$). Closing this gap requires outdoor street cabinets, mobile volunteer networks, or drone delivery.

## How I built it

- **Data Pipeline:** 2,706 Virginia Beach OHCA dispatch records; 929 candidate sites with operating schedules queried via OpenStreetMap Overpass API; 52,708-intersection walking network modeled using OSMnx; CDC/ATSDR Social Vulnerability Index (2022); and U.S. Census TIGER tract geometries.
- **Optimization & Theory:** Submodularity proof guaranteeing greedy performance, mixed-integer linear programs formulated in SciPy with the HiGHS solver, lazy greedy ordering, and an analytical feasibility bound ($C_q / T_p$).
- **Validation:** 5-fold temporal cross-validation (including a strict forward-in-time test on 2019 data), address-clustered bootstrap resampling (2,000 iterations), 10 sensitivity scenarios across 30 budget-scenario pairs, and ablation testing.
- **Tools:** Python (pandas, geopandas, networkx, osmnx, scipy, matplotlib), LaTeX (`pdflatex`), and Leaflet / vanilla JavaScript for the interactive web prototype.

## Challenges I ran into

- **Missing response data:** 373 records had response times of exactly zero, meaning the timestamp wasn't recorded. I imputed these based on road distance to stations ($r = 0.21$) and verified that dropping them entirely didn't alter any of the conclusions or method rankings.
- **Data clustering:** Roughly 70% of cardiac arrests in Virginia Beach recur at repeated block addresses (like nursing facilities). Using standard bootstrap resampling made confidence bands look artificially tight, so I implemented address-clustered bootstrap intervals to reflect realistic uncertainty.
- **A fairness loophole:** My first fairness formula let the algorithm look fair simply by pulling benefit away from well-served areas. Fixing that benchmarking bug led directly to proving the feasibility bound.
- **An outside critique:** An independent reviewer caught a walking-distance edge case (where far-away points routed as 0 m) and pointed out that a headline claim only held in-sample. I fixed the network routing, re-ran every experiment out-of-sample, dropped the claim, and found the core findings became even stronger.
- **Falsified initial hypothesis:** I originally expected that steering AEDs to historically slow EMS areas would help. It didn't ($R^2 = 0.07$). Reporting that negative result honestly led to the reach curve.

## Accomplishments I'm proud of

- Developing an optimization model that outperforms the standard maximal covering method by 42–67% on completely unseen cardiac arrests.
- Deriving a concrete, actionable policy rule for municipal health departments: one 24/7 outdoor cabinet is worth roughly two indoor AEDs.
- Proving both a submodular greedy guarantee ($\ge 63.2\%$) and an asymptotic feasibility bound that precisely explains the mathematical limits of geographic equity.

## What I learned

How to translate resuscitation science into rigorous facility-location math, why submodularity provides solid guarantees for real-world heuristics, how to rigorously validate models out-of-sample with clustered spatial data, and that disproving an intuitive hypothesis can lead to a much cleaner model.

## What's next

- Validating survival projections directly against confirmed patient neurological outcomes through clinical CARES registry linkages.
- Modeling time-varying bystander availability using aggregated pedestrian mobility feeds.
- Expanding the optimization framework to co-optimize hybrid deployments combining fixed units, smart street cabinets, and autonomous drone delivery.
- Replicating the framework in other open-data metropolitan areas.

## Prototypes

- **AED Placement Explorer:** An interactive web map where planners can adjust the AED budget slider ($p = 1$ to $200$), switch dynamically between indoor sites, 24/7 outdoor cabinets, and classic MCLP, and view live updates for survival gains, coverage maps, and social vulnerability equity.
- **Heartline:** A companion lightweight progressive web app (PWA) designed for bystanders to locate open AEDs in real time, follow hands-only CPR cadence, and flag neighborhood coverage gaps directly to OpenStreetMap.

## References (selected; full list of 33 in the paper PDF)

- CARES. *2024 Metrics Summary*, 2025.
- Custodio & Lejeune. Spatiotemporal data set for out-of-hospital cardiac arrests. *INFORMS J. Computing*, 2022.
- Valenzuela et al. Estimating effectiveness of cardiac arrest interventions. *Circulation*, 1997.
- Church & ReVelle. The maximal covering location problem. *Papers of the Regional Science Association*, 1974.
- Nemhauser, Wolsey & Fisher. An analysis of approximations for maximizing submodular set functions. *Math. Programming*, 1978.
- Sun et al. Overcoming spatial and temporal barriers to public access defibrillators via optimization. *JACC*, 2016.
- Bertsimas, Farias & Trichakis. The price of fairness. *Operations Research*, 2011.
- Pollack et al. Impact of bystander AED use on survival. *Circulation*, 2018.
- Hansen et al. AEDs inaccessible to more than half of nearby cardiac arrests at night and weekends. *Circulation*, 2013.
