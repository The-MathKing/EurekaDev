# Literature notes — Response-time-weighted, equity-constrained AED placement (Virginia Beach)

Compiled 2026-10-19. Every source below was located on PubMed, the publisher page, a repository record, or a CDC/CARES document. Numbers are taken from the abstract or document actually read unless flagged **[unverified]** (meaning: the paper exists, but that specific figure comes from a secondary summary or memory and must be checked against full text before citing).

Verification key: PM = PubMed record read; WEB = publisher/repository page or PDF read; SRCH = found only via search-result excerpt (exists, but quoted wording not read in full).

---

## Theme 1 — OHCA burden, survival, time-to-defibrillation, AED effect, guidance

### 1.1 CARES national survival report (2013–2025 aggregate) [WEB — PDF read]
Cardiac Arrest Registry to Enhance Survival (CARES). *CARES Survival Report, All Agencies/National Data, Date of Arrest 01/01/2013–12/31/2025, Non-Traumatic Etiology.* Generated April 20, 2026. https://mycares.net/sitepages/uploads/2026/CARES%202013-2025%20Non-Traumatic%20National%20Survival%20Report.pdf
- N = 1,266,616 non-traumatic EMS-treated OHCAs; survival to hospital discharge 10.2%; CPC 1–2 at discharge 8.1%.
- Location: home/residence 71.6% (survival 8.6%), public setting 17.8% (survival 20.4%), nursing home 10.6% (4.2%).
- Initial shockable rhythm 18.1% of all arrests (survival 28.5%); non-shockable 81.9% (6.2%).
- Bystander CPR 40.8% (excl. nursing home/healthcare); bystander AED use 2.1% of eligible events (survival 32.8% when used vs. 10.2% overall).
- Utstein (bystander-witnessed + shockable) 10.8% of cases, survival 32.5%.

### 1.2 CARES 2024 Metrics Summary [WEB — PDF read]
CARES. *2024 Metrics Summary* (May 16, 2025). https://mycares.net/sitepages/uploads/2025/CARES%2020250516%202024%20Metrics%20Summary.pdf
- 137,119 non-traumatic worked OHCAs reported in 2024; catchment >186 million people; 37 statewide registries.
- Overall survival 10.5%; Utstein 33.4%; Utstein-bystander 37.6%; bystander-witnessed 16.0%; unwitnessed 4.5%.
- Bystander CPR 41.7%; **12.6% of patients who arrested in public had a bystander-applied AED** (female 10.0%, male 13.4%).
- **Median EMS response time 6.4 min**; public setting 18.0% of arrests, residential 71.3%.

### 1.3 Buaprasert et al. 2024 — CARES overview (2022 numbers) [WEB — PMC read]
Buaprasert P, Al-Araji R, Rajdev M, Vellano K, Carr MJ, McNally B. The past, present, and future of the Cardiac Arrest Registry to Enhance Survival (CARES). *Resusc Plus.* 2024;18:100624. doi:10.1016/j.resplu.2024.100624. https://pmc.ncbi.nlm.nih.gov/articles/PMC11043876
- 2022: 147,736 OHCAs reported; survival to discharge 9.3%; bystander CPR 40.0%; bystander AED applied in 11.3% of public-location arrests; Utstein survival 30.7%.

### 1.4 Martin et al. 2025 — AHA Heart Disease & Stroke Statistics [PM]
Martin SS, Aday AW, Allen NB, et al. 2025 Heart Disease and Stroke Statistics: A Report of US and Global Data From the American Heart Association. *Circulation.* 2025;151(8):e41–e660. doi:10.1161/CIR.0000000000001303
- Annual AHA/NIH statistical compendium; its sudden-cardiac-arrest chapter draws on CARES. Use for the headline "US OHCA" sentence; cite CARES directly for exact rates (above). Specific chapter figures not read here **[unverified]**.

### 1.5 Larsen et al. 1993 — survival vs. time intervals (graphic model) [PM]
Larsen MP, Eisenberg MS, Cummins RO, Hallstrom AP. Predicting survival from out-of-hospital cardiac arrest: a graphic model. *Ann Emerg Med.* 1993;22(11):1652–1658. doi:10.1016/S0196-0644(05)81302-2
- 1,667 King County VF arrests (1976–). Linear model: **survival = 67% − 2.3%/min to CPR − 1.1%/min to defibrillation − 2.1%/min to ACLS** (P<.001).
- 67% = predicted survival if all three interventions occurred at collapse; with no treatment survival falls **5.5 percentage points per minute** (sum of coefficients).
- Source of the widely quoted "~7–10% per minute" rule when CPR is absent (the 1.1%/min defib term is conditional on the other terms; cite the full equation, not just one coefficient).

### 1.6 Valenzuela et al. 1997 — logistic survival model [PM]
Valenzuela TD, Roe DJ, Cretin S, Spaite DW, Larsen MP. Estimating effectiveness of cardiac arrest interventions: a logistic regression survival model. *Circulation.* 1997;96(10):3308–3313. doi:10.1161/01.CIR.96.10.3308
- Witnessed VF arrests, n=205 (Tucson) + n=1,667 (King County); outcome = survival to discharge.
- Collapse-to-CPR and collapse-to-defibrillation intervals both significant; a simplified model with only those two intervals performed as well as the full model; site was not a predictor after adjustment, so the model "can be generalized to other US populations".
- Simplified two-interval model: s = (1 + e^(−0.260 + 0.106·I_CPR + 0.139·I_Defib))^(−1), intervals in minutes from collapse. **[WEB — verified as Eq. (2) in the full text of Erkut, Ingolfsson & Erdoğan 2008 (preprint PDF read, see 1.6b); the Valenzuela full text itself is paywalled.]** Erkut et al. note that Valenzuela et al. reported that this function overestimated survival when response time was large. This is the survival-decay curve used for our gains.

### 1.6b Erkut, Ingolfsson & Erdoğan 2008 — survival functions for EMS location [WEB — preprint PDF read]
Erkut E, Ingolfsson A, Erdoğan G. Ambulance location for maximum survival. *Naval Research Logistics.* 2008;55(1):42–58. doi:10.1002/nav.20267. Preprint: https://sites.ualberta.ca/~aingolfs/documents/survival15november07.pdf
- Reviews four published survival functions (Larsen 1993, Valenzuela 1997, Waalewijn 2001, De Maio 2003) and argues for survival-maximizing instead of coverage-maximizing location models; Edmonton EMS case study.
- Reproduces Valenzuela's simplified model as Eq. (2) and De Maio's response-time-only function as Eq. (4) (coefficients above and in 1.6c).
- All four studies define survival as survival to hospital discharge; Larsen and Valenzuela are VF-only, De Maio includes all treated arrests regardless of rhythm.

### 1.6c De Maio et al. 2003 — survival vs EMS defibrillation response interval [PM abstract + WEB via Erkut]
De Maio VJ, Stiell IG, Wells GA, Spaite DW. Optimal defibrillation response intervals for maximum out-of-hospital cardiac arrest survival rates. *Ann Emerg Med.* 2003;42(2):242–250. doi:10.1067/mem.2003.266
- OPALS (Ontario) cohort of adult cardiac-etiology OHCAs; logistic regression of survival on the defibrillation response interval (call to arrival of a defibrillator-equipped vehicle) and covariates; odds of survival fall by a factor 0.77 per minute (95% CI 0.74–0.83) [PM abstract].
- Predicted survival at 90th-percentile response cutoffs: 12.0% (5 min), 9.5% (6), 7.5% (7), 5.9% (8), 4.6% (9) [PM abstract]; concludes the common 8-minute target is not supported as optimal.
- Response-time-only function after averaging over the other covariates, as reproduced by Erkut et al. Eq. (4): s(I) = (1 + e^(−0.679 + 0.262·I))^(−1) **[WEB — from Erkut preprint]**.
- **Caveat:** this form gives 66% at I = 0 and about 23% at 7.2 min, far above De Maio's own population survival rates quoted above. The reproduced form may refer to a specific covariate profile, or the averaging step may have changed the level. Our paper uses it only as a robustness check; the ranking of methods is unchanged under it. Check the De Maio full text before relying on its absolute levels.

### 1.7 Weisfeldt et al. 2010 — bystander AED before EMS [PM]
Weisfeldt ML, Sitlani CM, Ornato JP, et al. Survival after application of automatic external defibrillators before arrival of the emergency medical system: evaluation in the Resuscitation Outcomes Consortium population of 21 million. *J Am Coll Cardiol.* 2010;55(16):1713–1720. doi:10.1016/j.jacc.2009.11.077
- 13,769 OHCAs (2005–07): only **2.1% had an AED applied before EMS arrival**.
- Survival 7% overall; 9% bystander CPR without AED; **24% with AED applied; 38% with AED shock delivered**.
- Adjusted OR for survival with AED application **1.75 (95% CI 1.23–2.50)**, adjusting for EMS response interval among others; extrapolated to ~474 lives/yr in US+Canada.

### 1.8 Pollack et al. 2018 — bystander AED in shockable public OHCA [PM]
Pollack RA, Brown SP, Rea T, et al. Impact of bystander automated external defibrillator use on survival and functional outcomes in shockable observed public cardiac arrests. *Circulation.* 2018;137(20):2104–2113. doi:10.1161/CIRCULATIONAHA.117.030700
- ROC 2011–15: 4,115 observed public OHCAs; 60.8% shockable; bystander shock in only **18.8%** of shockable ones.
- Survival 66.5% vs 43.0% (bystander vs EMS first shock); adjusted OR **2.62 (2.07–3.31)** for survival, 2.73 for favorable function.
- **"The benefit of bystander shock increased progressively as EMS response time became longer."** — direct support for response-time weighting.

### 1.9 Hindborg et al. 2025 — bystander defibrillation benefit by EMS response time [PM]
Hindborg M, Yonis H, Gnesin F, et al. Bystander defibrillation and survival according to emergency medical service response time after out-of-hospital cardiac arrest: a nationwide registry-based cohort study. *Prehosp Emerg Care.* 2025;30(2):232–240. doi:10.1080/10903127.2025.2478211
- Danish registry 2016–22, 3,924 bystander-witnessed shockable OHCAs with bystander CPR; TMLE causal analysis by EMS response-time strata.
- Bystander defibrillation raised 30-day survival for **EMS response 7–9 min in public OHCAs (survival ratio 1.24, 95% CI 1.03–1.49)**; no significant benefit in other strata or residential arrests.
- Closest clinical evidence that PAD value depends on EMS delay; motivates weighting demand by EMS response time rather than treating all arrests equally.

### 1.10 Hansen et al. 2013 — temporal AED inaccessibility, Copenhagen [PM]
Hansen CM, Wissenberg M, Weeke P, et al. Automated external defibrillators inaccessible to more than half of nearby cardiac arrests in public locations during evening, nighttime, and weekends. *Circulation.* 2013;128(20):2224–2231. doi:10.1161/CIRCULATIONAHA.113.003066
- 1,864 public OHCAs (1994–2011), 552 AEDs; coverage defined as OHCA within **100 m** of an AED.
- **61.8%** of public OHCAs occurred evening/night/weekend; only **9.1% of AEDs accessible 24/7**.
- 28.8% covered ignoring hours; limited access cut coverage by **4.1% on weekday daytime but 53.4% evenings/nights/weekends**.

### 1.11 Karlsson et al. 2019 — accessibility and survival, Copenhagen [PM]
Karlsson L, Malta Hansen C, Wissenberg M, et al. Automated external defibrillator accessibility is crucial for bystander defibrillation and survival: a registry-based study. *Resuscitation.* 2019;136:30–37. doi:10.1016/j.resuscitation.2019.01.014
- 2,500 OHCAs (2008–16); 22.6% within 200 m route distance of a registered AED, but **<50% of those AEDs were accessible at the time**.
- Accessible vs inaccessible nearest AED: bystander defibrillation 13.8% vs 4.8%; 30-day survival 28.8% vs 16.4%; in witnessed shockable cases 72.7% vs 44.1%.
- Offices, schools, sports facilities each had **coverage loss >50%** from limited hours — justifies OSM opening_hours modelling.

### 1.12 Deakin et al. 2018 — retrieval distance and night availability, England [PM]
Deakin CD, Anfield S, Hodgetts GA. Underutilisation of public access defibrillation is related to retrieval distance and time-dependent availability. *Heart.* 2018;104(16):1339–1343. doi:10.1136/heartjnl-2018-312998
- 4,012 OHCAs mapped to 2,076 AEDs; walking distance at a **brisk 4 mph**; only **34.3% of AEDs available at night**.
- 5.91% of OHCAs within 100 m walking radius by day, **1.59% out-of-hours**; 36.4% within 500 m.
- An AED could have been retrieved before ambulance arrival in 25.3% of cases.

### 1.13 Karlsson et al. 2021 — straight-line vs route distance [PM]
Karlsson L, Sun CLF, Torp-Pedersen C, et al. Implications for cardiac arrest coverage using straight-line versus route distance to nearest automated external defibrillator. *Resuscitation.* 2021;167:326–335. doi:10.1016/j.resuscitation.2021.07.014
- 100-m coverage falls from 24.2% to 9.5% (Copenhagen) and 6.9% to 3.8% (Toronto) when route distance replaces Euclidean; median route/straight-line ratio **1.6 and 1.4**.
- Justifies network (walking) distance in our coverage set, or a circuity correction if Euclidean is used.

### 1.14 Siddiq, Brooks & Chan 2013 — effect of coverage radius [PM]
Siddiq AA, Brooks SC, Chan TC. Modeling the impact of public access defibrillator range on public location cardiac arrest coverage. *Resuscitation.* 2013;84(7):904–909. doi:10.1016/j.resuscitation.2012.11.019
- Toronto, 1,310 public OHCAs, 25,851 candidate buildings; 600 scenarios of range (10–300 m) × AEDs (10–200).
- With 200 AEDs, raising range 100→200 m covers +15% of arrests; 200→300 m only +10% (diminishing returns).
- AED in every public building: 50% coverage at 50 m, 95% at 300 m. Useful sensitivity benchmark for our radius choice.

### 1.15 ERC Guidelines 2021 — Systems Saving Lives [PM + SRCH]
Semeraro F, Greif R, Böttiger BW, et al. European Resuscitation Council Guidelines 2021: Systems saving lives. *Resuscitation.* 2021;161:80–97. doi:10.1016/j.resuscitation.2021.02.008
- Chapter covers chain of survival, community engagement, dispatcher role, first-responder/AED systems (abstract read).
- Search excerpts of the chapter: recommended density of **2 AEDs/km² and ≥10 first responders/km²**; placing AEDs where **≈1 cardiac arrest per 5 years** is expected is considered cost-effective; register public AEDs with dispatch **[SRCH — confirm wording/page in full text]**.
- The "100 m / 1.5-min brisk walk" rule is used operationally in Chan/Sun/Folke papers (above/below), not stated as such in this abstract **[unverified as ERC wording]**.

### 1.16 AHA 2020 Guidelines, Part 7: Systems of Care [PM + SRCH]
Berg KM, Cheng A, Panchal AR, et al. Part 7: Systems of Care: 2020 American Heart Association Guidelines for Cardiopulmonary Resuscitation and Emergency Cardiovascular Care. *Circulation.* 2020;142(16_suppl_2):S580–S604. doi:10.1161/CIR.0000000000000899
- Recommendation (COR 1, LOE B-NR): "We recommend that public access defibrillation programs for patients with OHCA be implemented in communities at risk for cardiac arrest." Supporting text: 27 of 31 studies of PAD programs found improved outcomes **[SRCH — quoted from search excerpt of the article page]**.
- Also recommends dispatch alerting of nearby willing bystanders via mobile phone (COR 1, LOE B-NR) [SRCH].

---

## Theme 2 — Disparities in bystander response and AED access

### 2.1 Sasson et al. 2012 [PM]
Sasson C, Magid DJ, Chan P, et al. Association of neighborhood characteristics with bystander-initiated CPR. *N Engl J Med.* 2012;367(17):1607–1615. doi:10.1056/NEJMoa1110700
- CARES, 29 sites, 14,225 arrests; bystander CPR 28.6% overall.
- vs high-income white tracts: **low-income Black OR 0.49 (0.41–0.58)**; low-income white 0.65; low-income integrated 0.62; high-income Black 0.77.
- Neighborhood = census tract (income threshold $40,000; >80% one race) — same unit as SVI.

### 2.2 Starks et al. 2017 [PM]
Starks MA, Schmicker RH, Peterson ED, et al. Association of neighborhood demographics with out-of-hospital cardiac arrest treatment and outcomes: where you live may matter. *JAMA Cardiol.* 2017;2(10):1110–1118. doi:10.1001/jamacardio.2017.2671
- ROC 2008–11, 22,816 adult OHCAs by tract % Black residents.
- Bystander CPR and **lay AED use inversely associated with % Black residents**; fewer public-location arrests and shockable rhythms in >75% Black tracts.
- Adjusted survival OR 0.76 (25–50% Black), 0.67 (51–75%), **0.63 (>75%; 0.50–0.79)**; attenuated when site added.

### 2.3 Brown et al. 2025 (NIHR, England) — deprivation gradient [PM]
(Full citation in 3.9.) Historical OHCAs occurred in **more deprived areas while AEDs were placed in more affluent areas**; stakeholder panel agreed current PAD distribution is inequitable with respect to deprivation.

### 2.4 Leung et al. 2021 — equity-aware optimization (Scotland) [PM]
(Full citation in 3.7.) Existing AED distribution across deprivation quintiles differed significantly from the OHCA distribution (P<0.001); optimization shifted AEDs toward deprived quintiles so coverage matched the OHCA distribution.

---

## Theme 3 — Optimization foundations and AED-placement OR literature

### 3.1 Toregas, Swain, ReVelle & Bergman 1971 — LSCP [WEB]
Toregas C, Swain R, ReVelle C, Bergman L. The location of emergency service facilities. *Operations Research.* 1971;19(6):1363–1373. doi:10.1287/opre.19.6.1363
- Set-covering formulation: minimize number of facilities so every demand point is within a response distance/time standard; solved by LP plus a cut.
- Our MCLP is the budgeted dual of this: fix the number of AEDs, maximize covered (weighted) demand.

### 3.2 Church & ReVelle 1974 — MCLP [WEB]
Church R, ReVelle C. The maximal covering location problem. *Papers of the Regional Science Association.* 1974;32:101–118. doi:10.1007/BF01942293
- Introduces MCLP: locate p facilities to maximize population covered within distance S; >1,500 citations; the model behind almost all AED-placement papers (Petravić 2025).

### 3.3 Nemhauser, Wolsey & Fisher 1978 — submodular greedy bound [WEB]
Nemhauser GL, Wolsey LA, Fisher ML. An analysis of approximations for maximizing submodular set functions—I. *Mathematical Programming.* 1978;14:265–294. doi:10.1007/BF01588971
- For nondecreasing submodular f with f(∅)=0 under a cardinality constraint K, greedy achieves ≥ **1 − ((K−1)/K)^K ≥ 1 − 1/e ≈ 0.632** of optimum.
- Weighted MCLP coverage (sum over demand of weight × [covered]) is monotone submodular, so greedy inherits this guarantee; the SVI-quartile fairness constraint breaks the pure cardinality structure, so the bound applies to the unconstrained relaxation only.

### 3.4 Bertsimas, Farias & Trichakis 2011 — price of fairness [WEB — PDF read]
Bertsimas D, Farias VF, Trichakis N. The price of fairness. *Operations Research.* 2011;59(1):17–31. doi:10.1287/opre.1100.0865
- Defines **price of fairness = relative loss in total utility when a fair allocation replaces the utilitarian optimum**; studies proportional and max-min fairness.
- Bounds depend only on number of players n for convex compact utility sets; price of proportional fairness is much smaller than max-min, especially for large n; bounds are tight. (Exact bound formulas not reproduced here **[unverified]**.)
- We report "price of fairness" as (unconstrained expected survival − SVI-constrained expected survival)/unconstrained.

### 3.5 Chan et al. 2013 — first optimization-based AED siting (Toronto) [PM]
Chan TC, Li H, Lebovic G, et al. Identifying locations for public access defibrillators using mathematical optimization. *Circulation.* 2013;127(17):1801–1809. doi:10.1161/CIRCULATIONAHA.113.001953
- 1,310 public OHCAs (2005–10), 1,669 AEDs; **100 m** coverage; baseline 23% coverage, mean distance 281 m.
- Top-30 optimized sites add 112 historical arrests (32% coverage); beats population-guided placement.

### 3.6 Chan, Demirtas & Kwon 2016 — MCLP models for PAD [WEB]
Chan TCY, Demirtas D, Kwon RH. Optimizing the deployment of public access defibrillators. *Management Science.* 2016;62(12):3617–3635. doi:10.1287/mnsc.2015.2312
- Develops MCLP-type models (incl. gradual/decaying coverage) for AED deployment on Toronto data; optimized deployment improves coverage by **~40%** over the existing approach **[SRCH — number from search excerpt]**.

### 3.7 Sun et al. 2016 — spatiotemporal availability [PM]
Sun CLF, Demirtas D, Brooks SC, Morrison LJ, Chan TCY. Overcoming spatial and temporal barriers to public access defibrillators via optimization. *J Am Coll Cardiol.* 2016;68(8):836–845. doi:10.1016/j.jacc.2016.03.609
- Toronto 2006–14: 2,440 public OHCAs, 737 AEDs; **24/7 assumption overstates coverage by 21.5%** (451 vs 354 covered); "one in 5 OHCAs occurred near an inaccessible AED".
- Spatiotemporal optimization gives **25.3% relative gain in actual coverage** over spatial-only (10-fold CV). Direct precedent for our opening-hours layer.

### 3.8 Leung et al. 2021 — socioeconomically equitable placement [PM]
Leung KHB, Brooks SC, Clegg GR, Chan TCY. Socioeconomically equitable public defibrillator placement using mathematical optimization. *Resuscitation.* 2021;166:14–20. doi:10.1016/j.resuscitation.2021.07.002
- Scotland 2011–17: 49,432 suspected OHCAs, 1,532 AEDs, SIMD quintiles; coverage = within 100 m.
- Optimizing for coverage alone already moved AEDs toward deprived areas; **relocating existing AEDs ≈ doubling AED count** in coverage.
- Equity is achieved implicitly (by matching OHCA distribution), not by an explicit fairness constraint — contrast with our hard SVI-quartile constraint.

### 3.9 Brown et al. 2025 — NIHR England optimisation + cost-effectiveness [PM]
Brown TP, Andronis L, El-Banna A, Leung BK, Arvanitis T, Deakin C, et al. Optimisation of the deployment of automated external defibrillators in public places in England. *Health Soc Care Deliv Res.* 2025;13(5):1–179. doi:10.3310/HTBT7685
- OHCAO registry; coverage radius **500 m walking**; median OHCA–AED distance 638 m; 38.9% within 500 m.
- MCLP-adapted models; 1-km grid placement raises coverage to 78.8%; coverage loss when AEDs unavailable outside working hours was greatest for schools.
- ICERs >£30,000/QALY for all alternatives; best strategy (halls/community centres) £32,418/QALY.

### 3.10 Sun et al. 2020 — in-silico trial vs guideline placement [PM]
Sun CLF, Karlsson L, Morrison LJ, Brooks SC, Folke F, Chan TCY. Effect of optimized versus guidelines-based automated external defibrillator placement on out-of-hospital cardiac arrest coverage: an in silico trial. *J Am Heart Assoc.* 2020;9(17):e016701. doi:10.1161/JAHA.120.016701
- Copenhagen 2008–16, 653 public OHCAs; coverage = **100 m route distance**; monthly rolling placement using only past data (a train/test discipline like ours).
- Guideline-based 393 AEDs: 15.8% coverage; optimized: **24.2%** (P<0.001); est. bystander defib 15.6→18.2%, 30-day survival 32.6→34.0%; the 1,573 real AEDs covered 14.4%.

### 3.11 Pourghaderi et al. 2021 — maximize expected survival (Singapore) [PM]
Pourghaderi AR, Kogtikov N, Lees MH, et al. Maximum expected survival rate model for public access defibrillator placement. *Resuscitation.* 2021;170:213–221. doi:10.1016/j.resuscitation.2021.11.039
- 15,345 OHCAs (2010–17); fits a **power-law survival-vs-time-to-defibrillation curve (R² 91.33%)**: 54.9% survival if defibrillated within 2 min, >60% relative reduction if not within 4 min.
- MESR model maximizes expected survival instead of binary coverage; beats a max-coverage model (P<0.05; <0.0001 in 22/30 experiments).
- Closest OR precedent for a survival-decay objective — but decay is driven by bystander AED retrieval time, not by the local EMS response time.

### 3.12 Bitencourt et al. 2025 — ambulance delay zones + MCLP (Brazil) [PM]
Bitencourt MR, et al. Out-of-hospital cardiac arrest ambulance delay zones and AED placement in a southern Brazilian city. *Int J Environ Res Public Health.* 2025;22(2):173. doi:10.3390/ijerph22020173
- 278 OHCAs (2019–22); spatial survival analysis of probability that ambulance exceeds 5 min; MCLP with **150-s bystander reach**, 100 sites.
- Median ambulance response 11.63 min; proposed AEDs cover 76% of OHCAs; mean AED travel 320 s vs ambulance 709 s.
- Uses EMS delay descriptively/comparatively — **does not weight the MCLP objective by response time**.

### 3.13 Starks et al. 2024 — drones/first responders to hit 5-min AED (NC, CARES) [PM]
Starks MA, Chu J, Leung KHB, et al. Combinations of first responder and drone delivery to achieve 5-minute AED deployment in OHCA. *JACC Adv.* 2024;3(7):101033. doi:10.1016/j.jacadv.2024.101033
- 28,292 OHCAs, 48 NC counties; county median response 8.0 min; 16.5% get AED <5 min; optimized drones → 4.8 min median, 56.3% <5 min; est. +34% survival for witnessed arrests with drone <5 min.
- Uses response-time-to-survival regression and optimizes to the response-time distribution (drone bases, not fixed PADs).

### 3.14 Boutilier et al. 2022 — drone network with EMS response times [Consensus abstract]
Boutilier JJ, Chan TCY, et al. Drone network design for cardiac arrest response. *Manufacturing & Service Operations Management.* 2022. (DOI not captured — look up on INFORMS) **[citation details unverified]**
- Location-queuing model that "incorporates existing EMS response times"; optimizing the tail of response time yields more geographically dispersed, equitable networks; 42–76% higher estimated survival.
- Closest OR work that explicitly conditions on existing EMS response times — for drones, not static AEDs.

### 3.15 Buter et al. 2024 — gradual MCLP with greedy/GRASP (Netherlands) [Consensus abstract]
Buter R, et al. Strategic placement of volunteer responder system defibrillators. *Health Care Management Science.* 2024. doi:10.1007/s10729-024-09685-4
- BIP for gradual (partial-coverage) MCLP with distance-decay functions by foot/bike/car; greedy and GRASP heuristics near-optimal; KDE-estimated OHCA density; 29 municipalities, relocation raises coverage 36%→49%.
- Precedent for greedy heuristics on AED MCLP and for decay-shaped coverage.

### 3.16 Dahan et al. 2016 — Paris deployment strategies [PM]
Dahan B, Jabre P, Karam N, et al. Optimization of automated external defibrillator deployment outdoors: an evidence-based approach. *Resuscitation.* 2016;108:68–74. doi:10.1016/j.resuscitation.2016.09.010
- 4,176 OHCAs (2000–10), 33% public; guideline strategy (>1 OHCA in 5 yr) → 170 AEDs, median distance 416 m; grid strategy optimal at 200–400 AEDs; landmark strategy: pharmacies (n=1,466) 142 m, bike-share stations 137 m.

### 3.17 Aeby, Staeger & Dami 2021 — hotspot relocation (Switzerland) [PM]
Aeby D, Staeger P, Dami F. How to improve automated external defibrillator placement for out-of-hospital cardiac arrests: a case study. *PLoS One.* 2021;16(5):e0250591. doi:10.1371/journal.pone.0250591
- 2,971 OHCAs (2014–18), 79.3% at home; 633 AEDs; 100-m coverage 7.5% overall, 4.5% for home arrests; 40 added AEDs → 17.6%; 17 AEDs relocatable with no coverage loss.

### 3.18 Petravić et al. 2025 — scoping review of PAD positioning [PM]
Petravić L, Rogina KG, Miklič R, et al. Strategic PAD positioning: a scoping review. *Scand J Trauma Resusc Emerg Med.* 2025;34(1):3. doi:10.1186/s13049-025-01527-8
- 43 works, mostly North America; **MCLP is the most common model**; most minimize distance to historical/simulated OHCAs.
- Calls for incorporating "population health indicators, and socioeconomic variables" and for prospective/real-world designs — supports our SVI constraint and held-out 2019 test year.

---

## Theme 4 — Data sources

### 4.1 Custodio & Lejeune 2022 — Virginia Beach OHCA dataset [WEB — RePEc/INFORMS]
Custodio JESC, Lejeune MA. Spatiotemporal data set for out-of-hospital cardiac arrests. *INFORMS Journal on Computing.* 2022;34(1):4–10. doi:10.1287/ijoc.2020.1022. Data/code: ijoc.2020.1022.cd.zip (INFORMS supplemental).
- All OHCA dispatches for the City of Virginia Beach with call time, **response time of first unit on scene**, address and coordinates; first-responder station locations; great-circle and road distances station↔incident; validated by city officials; toolkit generates problem instances.
- Years covered and incident counts: read from the data paper/zip before citing **[unverified here]**.

### 4.2 Flanagan et al. 2011 — CDC/ATSDR SVI [WEB]
Flanagan BE, Gregory EW, Hallisey EJ, Heitgerd JL, Lewis B. A social vulnerability index for disaster management. *J Homeland Security and Emergency Management.* 2011;8(1):Article 3. doi:10.2202/1547-7355.1792
- Original SVI: 15 census variables at tract level, 4 themes, percentile ranks.
- Current CDC/ATSDR SVI page (https://www.atsdr.cdc.gov/place-health/php/svi/): **16 ACS variables, four themes**, tract-level rankings (data vintage to be stated from the download used, e.g., SVI 2020/2022).

### 4.3 Lejeune & Margot 2025 (same group, same data) [SRCH]
Lejeune MA, Margot F. Response time minimization for cardiac arrests. *Production and Operations Management.* 2025. **[DOI unverified]**
- Drone-AED network as a queueing/fractional IP minimizing average response time, with cross-validation on unseen OHCA data; relevant because it is the authors' own use of the Virginia Beach data (drones, not fixed PADs).

---

## Novelty check

**Already done (do not claim as new):**
- MCLP for AED siting with 100-m (or 500-m) coverage on historical OHCAs: Chan 2013, Chan/Demirtas/Kwon 2016, Sun 2020, Brown 2025, and ~43 studies in Petravić 2025.
- Time-of-day availability of host sites in the objective: Sun 2016 (JACC) formally; Hansen 2013, Karlsson 2019, Deakin 2018 empirically. Using OSM opening_hours as the availability source is an implementation choice, not a methodological first (Brown 2025 used POI working hours).
- Survival-decay objective (maximize expected survival instead of binary coverage): Pourghaderi 2021 (power-law in time-to-defibrillation); gradual-coverage decay in Chan 2016 and Buter 2024.
- Equity across deprivation strata: Leung 2021 (SIMD quintiles, implicit equity via optimization); Brown 2025 documents deprivation gradient; Boutilier 2022 optimizes response-time tail for regional equity (drones).
- Greedy/heuristics for AED MCLP: Buter 2024 (greedy + GRASP); the 1−1/e guarantee is textbook (Nemhauser 1978).
- Train-on-past/test-on-future: Sun 2020 rolling monthly; Pourghaderi 10-fold CV; Lejeune & Margot 2025 cross-validation.

**Not found in prior work (candidate contributions, stated carefully):**
1. **Weighting each historical OHCA's demand by its own observed EMS response time through a survival-decay curve** (i.e., value of a PAD at location i ∝ survival gained if bystander defibrillation precedes an EMS arrival at t_i). Clinical evidence that PAD benefit depends on EMS delay exists (Pollack 2018; Hindborg 2025), and drone papers (Boutilier 2022; Starks 2024) condition on EMS times, but no static-AED MCLP paper found uses incident-level EMS response time as the demand weight. Bitencourt 2025 is the nearest: it maps ambulance delay zones and runs an MCLP, but keeps the two separate rather than weighting the objective. **Claim as "to our knowledge, first" with that caveat.**
2. **Explicit hard fairness constraint by CDC SVI quartile with a reported price of fairness** (Bertsimas framing) for AED placement. Leung 2021 reports equity outcomes but does not impose a constraint or quantify the efficiency cost; no AED paper found uses SVI.
3. Combination of (1) + (2) + opening-hours availability on a public US city dataset (Custodio & Lejeune) with a strict 2017–18 train / 2019 test split.

**Honest limitation to state:** the dataset's "response time" is EMS first-unit arrival for the historical call; our weighting assumes future arrests at nearby locations face similar delays (spatial persistence of response time). Also, the Virginia Beach data are dispatches, not Utstein-confirmed arrests, so rhythm/witness status may be unavailable.

---

## Key numbers for intro (all verified unless flagged)

- US EMS-treated non-traumatic OHCA: ~137,000 reported to CARES in 2024 (catchment >186 M); survival to discharge **10.5%** (2024), **10.2%** (2013–25 pooled). [CARES]
- Public-location arrests: **17.8%** of OHCAs but survival **20.4%** vs 8.6% at home. [CARES pooled]
- Shockable initial rhythm **18.1%** of all arrests, survival 28.5%; Utstein survival ~33%. [CARES]
- Bystander AED applied in only **12.6%** of public arrests (2024); **2.1%** of all eligible arrests (pooled); 1.9–2.1% in ROC 2005–07. [CARES; Weisfeldt 2010]
- Bystander AED shock → survival 38% (Weisfeldt 2010), 66.5% vs 43% (Pollack 2018, adjusted OR 2.62); CARES unadjusted 47% vs 27% when first shock by bystander vs EMS (2024 Annual Report p.41).
- Survival decay: 67% − 2.3%/min (CPR) − 1.1%/min (defib) − 2.1%/min (ACLS); ≈5.5 points/min untreated. [Larsen 1993]
- Median US EMS response time **6.4 min** (CARES 2024); bystander defibrillation benefit concentrated at EMS response 7–9 min in public (survival ratio 1.24). [Hindborg 2025]; benefit "increased progressively" with EMS response time. [Pollack 2018]
- 24/7 assumption overstates coverage by **21.5%**; spatiotemporal optimization +25.3% actual coverage. [Sun 2016]
- Only 9.1% of Copenhagen AEDs accessible 24/7; coverage loss 53.4% evenings/nights/weekends when 61.8% of public arrests occur. [Hansen 2013]
- Route distance cuts 100-m coverage by a factor 1.4–1.6 vs straight-line. [Karlsson 2021]
- Bystander CPR OR 0.49 in low-income Black vs high-income white tracts. [Sasson 2012]; survival OR 0.63 in >75% Black tracts. [Starks 2017]
- Optimized vs guideline placement: 24.2% vs 15.8% coverage; relocation ≈ doubling AED stock. [Sun 2020; Leung 2021]
- Greedy guarantee 1−1/e ≈ 0.632 for monotone submodular coverage. [Nemhauser 1978]
