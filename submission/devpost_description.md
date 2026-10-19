## Inspiration

Out-of-hospital cardiac arrest kills about nine in ten of the roughly 137,000 Americans it strikes each year (CARES 2024). When a bystander shocks the patient with an automated external defibrillator (AED) before EMS arrives, survival roughly doubles (Weisfeldt 2010; Pollack 2018). Yet a bystander uses an AED in only 12.6% of public arrests. Often the nearest AED is too far away, or it's locked inside a closed building. I wanted to use math to answer a practical question: **where should a city put its AEDs so they actually save lives?**

## What it does

This is a research project that combines optimization, probability and open data. Using all 2,706 cardiac arrests recorded in Virginia Beach, VA, from 2017 to 2019 (Custodio & Lejeune 2022), I:

- **Built a survival-based placement model.** For every arrest and every one of 929 candidate host sites (pharmacies, churches, schools, gas stations and more, from OpenStreetMap), it computes how much a bystander fetching that AED would raise the chance of survival. The inputs are real walking routes, the actual EMS response time, a published survival curve (Valenzuela et al. 1997), and whether the building was open at that hour.
- **Proved the objective is monotone submodular.** That guarantees a greedy algorithm reaches at least 63% (1 − 1/e) of the optimum. I also solved the problem exactly with integer programming.
- **Added a fairness constraint** across CDC Social Vulnerability Index quartiles, measured its "price of fairness", and proved a bound on when full fairness is possible at all.

## Key findings

1. **Survival-based placement saves 21–64% more expected lives on unseen data** than the standard maximal covering model. This comes from 5-fold temporal cross-validation with bootstrap confidence intervals, and it holds in all 24 robustness scenarios.
2. **Ignoring opening hours overstates an AED plan's benefit by 34–158%.** 24/7 outdoor cabinets recover 23–49%, and 50 outdoor cabinets beat 200 indoor AEDs.
3. **Tested and rejected:** placing AEDs where EMS was historically slow does not help, because location explains only about 7% of the variation in response time.
4. **Fairness is cheap but has a ceiling.** Raising every vulnerability group to 85% of the average costs under 5%, but full parity is impossible with building-hosted AEDs. Low-density suburbs need other tools, such as street cabinets, drones or responder apps.

## How I built it

- **Data:** Custodio & Lejeune OHCA dataset; OpenStreetMap (Overpass API) for 929 candidate sites and their opening hours; a 52,708-intersection walking network built with OSMnx; CDC/ATSDR SVI 2022; Census TIGER tracts.
- **Math:** a facility-location formulation, a submodularity proof, a mixed-integer program solved with HiGHS (via SciPy), lazy greedy, a fairness-constrained MILP, and a feasibility bound.
- **Validation:** 5-fold temporal cross-validation, paired bootstrap confidence intervals, 8 sensitivity scenarios, and an ablation study.
- **Tools:** Python (pandas, geopandas, networkx, osmnx, scipy, matplotlib), LaTeX, and Leaflet for the interactive prototype.

## Challenges I ran into

- **Missing data:** 373 arrests had a response time of exactly 0, which means not recorded rather than instant. I imputed them, and confirmed every result still holds when they're removed.
- **Rare events:** a single test year was too noisy, so I switched to cross-validation with bootstrap confidence intervals.
- **A fairness bug:** my first fairness constraint let the solver "look fair" by ignoring benefit in well-served areas. Fixing it led to the feasibility bound.
- **My own hypothesis failed:** I expected weighting by EMS delay to help, and it didn't. I report that honestly as a finding.

## Accomplishments I'm proud of

- A model that clearly beats the method used in most AED-placement studies, on data it never saw.
- A concrete policy recommendation (24/7 outdoor cabinets) with a measured effect.
- A clean proof plus a bound that matches what the solver found exactly.

## What I learned

How to turn a medical problem into an optimization problem, why submodularity makes greedy algorithms trustworthy, how to validate a model honestly, and that negative results are results too.

## What's next

Validating against actual patient outcomes (the CARES registry), modeling when and where bystanders are likely to be present, mixing fixed AEDs with drones and responder apps, and repeating the study in another city.

## Prototype

**AED Placement Explorer** is an interactive map. Add AEDs one at a time, switch between indoor sites, 24/7 cabinets and the classic method, and watch expected survival and fairness update live.

## References (selected; the full list of 33 is in the PDF)

- CARES. *2024 Metrics Summary*, 2025.
- Custodio & Lejeune. Spatiotemporal data set for out-of-hospital cardiac arrests. *INFORMS J. Computing*, 2022.
- Valenzuela et al. Estimating effectiveness of cardiac arrest interventions. *Circulation*, 1997.
- Church & ReVelle. The maximal covering location problem. *Papers of the Regional Science Association*, 1974.
- Nemhauser, Wolsey & Fisher. An analysis of approximations for maximizing submodular set functions. *Math. Programming*, 1978.
- Sun et al. Overcoming spatial and temporal barriers to public access defibrillators via optimization. *JACC*, 2016.
- Bertsimas, Farias & Trichakis. The price of fairness. *Operations Research*, 2011.
- Pollack et al. Impact of bystander AED use on survival. *Circulation*, 2018.
- Hansen et al. AEDs inaccessible to more than half of nearby cardiac arrests at night and weekends. *Circulation*, 2013.
