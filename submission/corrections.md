# Corrections after the review: numbers to update in paper.tex

Every number below is out-of-sample: sites are chosen on four half-years and scored on the held-out fifth, using the 5-fold temporal cross-validation. Confidence intervals come from a bootstrap that resamples address clusters, so repeat addresses aren't counted as independent. The results file is given in brackets.

## What changed and why

1. **Walking-distance bug (critical).** Arrests and sites were snapped to the nearest walking path without adding the distance to that path. Some pairs that were kilometres apart came out as 0 m. Fixed in `walk_distances.py`: snap distances are added, the distance is never shorter than the straight line, and points more than 150 m from the network count as unreachable.
2. **The cabinet and hours results were in-sample.** Sites were planned and scored on the same arrests. They are now out-of-sample.
3. **The tie-breaker used test-fold data.** It now uses training data only.
4. **Unequal budgets.** At 200 AEDs the classic method could only use about 106 sites. Every method now places exactly *p* AEDs.
5. **Confidence intervals were too narrow.** They now come from the clustered bootstrap.
6. **The main model is now "expected survival".** It averages over the citywide distribution of response times instead of using each arrest's own. This follows from RQ3, and it performs the same while needing less data. Say this openly in the paper: the per-arrest version was tested first.
7. **The De Maio curve got the wrong input.** It now uses the response interval measured from the 911 call.

## Sentences in your rewrite that are now wrong

| Where | Your text says | Replace with |
|---|---|---|
| Abstract, conclusion | 21–64% more than standard | **42–67% more for 25–200 AEDs** (+42% at 25, +63% at 50, +67% at 100, +46% at 200; significant for p ≥ 25) [cv2_results.csv] |
| RQ2 results, Discussion | assuming 24/7 overstates gains by 119–158% | **67–106%** out-of-sample (p=25: 70%, p=50: 73%, p=100: 67%, p=200: 71%, p=10: 106%) [hours2.csv] |
| RQ2 results | hours-aware plan +49% at p=50, cabinets another +49% | Hours-aware plan delivers **18.6** at p=50, versus 15.1 for the hours-blind plan (+23%). The same model with **24/7 cabinets delivers 26.1 (+41%)**. At 100 AEDs: 38.2 vs 24.5 (+56%). [cv2_results.csv] |
| RQ2 results | midnight–3am indoor gets < 1/4 of cabinet benefit | recompute from hours_profile2.csv, or delete |
| RQ2 results | generous hours: 34–47%, cabinets 23–28% | **not rerun yet. Delete, or I can rerun it.** |
| Discussion, rec. 1 | 50 cabinets beat 200 indoor (59.7 vs 55.8) | **Delete. It was in-sample and is false out-of-sample** (50 cabinets 26.1 vs 200 indoor 28.4). Correct claim: **25 cabinets ≈ 50 indoor AEDs (19.1 vs 18.6), and 100 cabinets beat 200 indoor AEDs (38.2 vs 28.4)**, so a 24/7 cabinet is worth about **two** indoor AEDs. |
| Discussion, rec. 2 | walks of 200–500 m still often reach patients first | An AED **loses half its value within ~123 m** of walking, keeps ~9% at 300 m and ~1% at 500 m (new Fig. 8, reach curve). Say: "value decays smoothly with distance; a hard 100 m cutoff throws away the useful 100–250 m range." |
| Discussion, rec. 4 | 85% parity costs under 5% | In-sample (main model): **90% parity costs 0.1% at p=50**, and 95% costs 0.9%. At p=25, 90% costs 2.6%. **Out-of-sample, the fairness constraint has no detectable cost**: at φ=0.85, total was 19.7 vs 18.6 unconstrained (within noise). [fairness.csv, fairness_oos.csv] |
| Discussion, rec. 4 / RQ4 | least-vulnerable quartile (Q1) is worst served | With the corrected distances, the worst served is **Q2**, which contains the large rural south of the city and has the **lowest site density (0.65 sites/km²)**. Out-of-sample per 100 arrests: Q1 0.77, **Q2 0.46**, Q3 0.77, Q4 0.80. The geography point still holds: it's density, not income. |
| Estimated clinical impact | 4.3 survivors (2.8 OOS), cabinets 6.5 | Use OOS only: 18.6 × 0.108 ≈ **2.0** extra survivors over 30 months for 50 indoor AEDs, and 26.1 × 0.108 ≈ **2.8** with cabinets. Keep your caveats. Also add that the 0.108 factor applies to all dispatches, including home arrests, so it's an upper bound. |
| Limitations | excluding imputed records produced identical conclusions | "...did not change the ranking of methods: our model still beat the classic one at p = 25, 50 and 100 (all 95% CIs above zero)." [sensitivity2.csv] |
| Background | Weisfeldt: survival roughly doubles, 38% vs 7% | That compares the shocked subgroup with *everyone*. Use instead: **24% with an AED applied vs 9% with bystander CPR alone** (Weisfeldt 2010), and Pollack's 66.5% vs 43.0%. |
| Background / abstract | 137,000 Americans each year | "about 137,000 arrests reported to CARES in 2024 (a registry covering about 186 million people)." It isn't the US total. |
| Lit review | Hindborg: benefit grows with delay | Hindborg found benefit **specifically when EMS took 7–9 minutes** in public arrests. The "grows progressively" quote is Pollack 2018. |

## Data numbers that changed

- **Within 100 m walking of any candidate site: 3.1%** (was 7.2%). Within 300 m: 21.0%. Within 500 m: 40.5%.
- 51 arrests and 46 sites are more than 150 m from the walking network and are treated as unreachable on foot.
- **Robustness:** 10 assumptions × 3 budgets = 30 checks. **Ours beats classic in 30/30, and the CI excludes zero in 28/30.** The two exceptions are a 300 m walk limit at p=25 and dropping the top-20 addresses at p=25. New this time: AED setup time of 1.5 min, and EMS arrival-to-shock of 2 min. [sensitivity2.csv]
- **Forward split** (train 2017–18, test 2019 H1): ours beats classic at every budget: 1.83 vs 1.15, 3.47 vs 2.10, 4.51 vs 2.24, 6.69 vs 2.29, 7.00 vs 2.98. **Per fold, it wins 23 of 25.** [cv2_results.csv fold4 column]

## Stronger baselines to report (Table 2 replacement)

These are out-of-sample potential survivors over 30 months, all methods with exactly p AEDs.

| Method | p=10 | 25 | 50 | 100 | 200 |
|---|---|---|---|---|---|
| Random | 0.8 | 1.5 | 3.1 | 6.1 | 11.8 |
| Classic MCLP, 100 m (assumes 24/7) | 3.2 | 8.3 | 11.4 | 14.7 | 19.5 |
| MCLP 100 m + opening hours (Sun 2016 style) | 4.8 | 8.9 | 11.2 | 14.8 | 19.9 |
| MCLP 300 m | 5.5 | 9.2 | 11.6 | 17.4 | 24.4 |
| Survival, no hours (Pourghaderi 2021 style) | 5.7 | 11.2 | 15.1 | 22.8 | 27.1 |
| Survival + hours, own response time | 5.5 | 13.3 | 17.3 | 24.0 | 28.3 |
| Survival + hours, median response time | 5.8 | 12.2 | 19.9 | 24.7 | 28.1 |
| **Expected survival (main)** | 5.3 | **11.7** | **18.6** | **24.5** | **28.4** |
| Main model in 24/7 outdoor cabinets | 11.7 | 19.1 | 26.1 | 38.2 | 46.4 |

At p=50 and p=100 the main model significantly beats random, all three MCLP variants, and survival-without-hours (clustered 95% CIs above zero). The three response-time variants (own, median, distribution) are not significantly different from each other, which is the RQ3 result.

**100 m coverage** (the classic method's own metric, open AED within 100 m): ours ≥ classic for p ≥ 50 (1.0% vs 0.9% at 50, 1.2% vs 1.0% at 100).

## New results to add (more novelty)

1. **Reach curve (new Fig. 8, left).** The expected survival gain from an AED at walking distance d is the survival gain averaged over the city's real EMS response times. It's derived, not assumed. **Half-value distance: ~123 m** at 1.4 m/s. This explains why the 100 m guideline is roughly right, and why a hard cutoff is wrong.
2. **Distributional model.** Because location explains only 7% of response-time variance, plan with E_R[g], the gain averaged over response times. The average of monotone submodular functions is still monotone submodular, so the greedy guarantee still holds. It **needs only a city's response-time distribution**, not incident-level times, so it transfers to cities that don't publish incident data.
3. **Bound, corrected and budget-free.** With an AED at every site, Q1 can get at most C₁ = 0.0123 per arrest, while the all-sites citywide average is T∞ = 0.0153. So parity relative to the all-sites average is capped at **φ ≤ 0.81**, whatever the budget. Per budget, the bound C_min / T_p is 0.89 at p=100, and the solver found 0.85 feasible and 0.90 infeasible, consistent with it. At p=25 and 50 the bound exceeds 1, so the budget limits fairness, not the bound. State it as a *necessary* condition.

---

# Round 2: fixes from the re-grade (score 3.6 → 4.0)

Paper text changes for you to make, because you're editing paper.tex. Find each spot with Cmd+F on the quoted words. The numbers come from `results/descriptives.json` and the CSVs named above.

1. **Coverage metric is mislabelled (major).** Search for *"does not lose on the classic method's own metric"* (RQ1 results), *"we also report the classic method's own metric"* (Experimental procedure, Metric bullet), and *"on which our plan does not lose"* (Limitations). The measure we reported counts an arrest only if an **open** AED is within 100 m. The classic method's own measure ignores hours. Suggested replacement for the RQ1 sentence:
   > On simple 100 m coverage the picture is mixed. Counting only AEDs that were open at the time, our plan covered as many or more held-out arrests for p ≥ 50 (26 vs. 25 at p = 50; 32 vs. 28 at p = 100). Ignoring opening hours (the classic method's own measure), the classic plan covered more at small budgets (43 vs. 40 at p = 50), and the two were tied from p = 100 (48 vs. 47; 53 vs. 53).

   In the Limitations, replace the last clause with: *"we partly guard against this by also reporting simple 100 m coverage, where the two methods are close."*
2. **Abstract: "also beats stronger baselines from the literature".** Change it to *"and, for 50–100 AEDs, also significantly beats stronger baselines from the literature"*. At p = 10 ours is slightly below two of them.
3. **RQ3: "did not help either".** Change it to *"made no significant difference either"*. It was slightly higher at p = 25 and 50, but not significantly.
4. **RQ4: "no quartile can be guaranteed more than about 81%".** Only the least-served quartile is capped. Change it to *"the least-served quartile (Q₁) can never receive more than about 81% of that best-possible citywide level, whatever the budget."*
5. **Discussion, recommendation 4: "85–90% parity cost at most 2.6% … no detectable cost".** Change it to: *"a floor of 85% cost at most 0.6% in-sample and showed no detectable cost on held-out arrests (though we did not compute a confidence interval for that comparison); 90% was still cheap where feasible but infeasible at p = 100."* At RQ4 "total benefit was if anything slightly higher", add *"(no confidence interval computed)"*.
6. **"Halves within about 123 m".** This is at brisk walking pace (1.4 m/s); it is 88 m at 1.0 m/s and 176 m at 2.0 m/s. Add *"at a brisk walking pace"* in the abstract, RQ3 and the conclusion.
7. **Honest framing of the reach curve (reviewer's novelty note).** In the Literature Review gap (iii), or right after the reach-curve definition, add: *"Because \bar g_{ij} depends only on distance and opening hours, the main model is a gradual-coverage MCLP \cite{chan2016,buter2024}; what is new is that its distance decay is derived from the survival curve and the city's own EMS delays rather than chosen by hand."*
8. **Estimated clinical impact.** After the 2.0 / 2.8 survivors sentence, add: *"Because the 10.8% factor is applied to every dispatch, including the 71% of arrests that happen at home, these are upper bounds."*
9. **Limitations, new sentence:** *"Fifty-one arrests more than 150 m from any walkable path score zero under every method; they lower all quartiles' maximum benefit C_q slightly but do not favour any method."*
10. **De Maio caveat.** In Table 1's De Maio row, or in Robustness, add: *"De Maio's curve, as reproduced by Erkut et al., gives higher absolute survival than De Maio's own population rates, so we use it only to check that the ranking of methods is unchanged."*
11. **Figure 5 caption (right panel).** Add: *"The indoor and cabinet plans are optimized separately, so they use different sites; that is why indoor can exceed cabinets in some time blocks."*
12. **Wording that's inaccurate rather than just stylistic:**
    - "validated logistic models" → "published logistic models". They come from other cities and weren't validated here.
    - "telemetry sidebar" → "side panel".
    - "smart cabinets" (RQ2) → "outdoor 24/7 cabinets". Nothing in the model is smart.
    - "indispensable multiplier" overclaims for about 1 survivor per year. Something like *"a valuable complement during the first minutes of public shockable arrests"* is safer.
13. **"Fully reproducible from public records" (Prototype section)** is now true: `run_all.sh` runs exactly the scripts behind the paper. No change needed.
14. **Prototype screenshot (the reviewer asked for one).** It's at `figures/fig9_prototype.png`. Paste this at the end of the Prototype section:
    ```latex
    \begin{figure}[htbp]
    \centering
    \includegraphics[width=\linewidth]{fig9_prototype.png}
    \caption{The AED Placement Explorer with 50 indoor AEDs. Numbers in the tool use all arrests (in-sample), so they are higher than the out-of-sample results in Section 5.}
    \label{fig:proto}
    \end{figure}
    ```
