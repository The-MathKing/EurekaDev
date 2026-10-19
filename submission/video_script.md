# Video script (target 3:45, about 520 spoken words)

Voiceover over slides and screen recordings. The **[VISUAL]** lines say what goes on screen. Rewrite the spoken lines in your own words, because reading them aloud should sound natural.

---

## 1. Hook (0:00–0:25)

**[VISUAL]** Black screen. A timer counts up from 0:00. Then the title: *Where Should the Defibrillators Go?*

> Every year about 137,000 Americans have a cardiac arrest outside a hospital, and nine in ten of them die. For the most survivable cases, the treatment is simple: an electric shock from a defibrillator, fast. Every minute of waiting lowers the odds. I wanted to find out where a city should put its public defibrillators so they actually save lives.

## 2. The problem (0:25–1:00)

**[VISUAL]** Figure 2 (response-time histogram). Then Figure 1 (survival curves).

> I used a public dataset of every cardiac arrest in Virginia Beach from 2017 to 2019: 2,706 of them, each with the time EMS took to arrive. The median wait was over 7 minutes, and 41 percent of patients waited more than 8. Medical research shows that a bystander with an AED can roughly double survival. But an AED only helps if it's close enough to fetch, and the building it's in is open.

## 3. The math (1:00–1:50)

**[VISUAL]** Animated diagram: an arrest, a walking route to a candidate site, a stopwatch for the "AED ready" time versus the "EMS arrives" time. Then the formula F(X) = Σ max g_ij.

> The standard method in the research is called the maximal covering location problem. It counts how many past arrests are within 100 meters of an AED. I replaced that count with expected survival. For each arrest and each possible site, like a pharmacy, church, school or gas station, I calculated how much a bystander fetching that AED would raise the chance of survival. That uses real walking routes on the city's street map, a published survival curve, and whether the building was actually open at the time of the arrest.
>
> Then I chose the sites that maximize total survival. I proved this function has a property called submodularity, which guarantees a simple greedy algorithm gets at least 63 percent of the best possible answer. I also solved it exactly with integer programming.

## 4. Results (1:50–3:05)

**[VISUAL]** Figure 4 (cross-validation). Then Figure 3 (map, side by side).

> To test it fairly, I trained on some months and tested on months the model had never seen. My model delivered 21 to 64 percent more benefit than the standard method, and it held up across 24 different robustness checks.

**[VISUAL]** Figure 5 (opening hours). Highlight the grey "promised" bars against the blue "delivered" bars.

> The biggest surprise was opening hours. If you plan as if every AED is always reachable, you overestimate the benefit by more than double, because many arrests happen at night when buildings are locked. Putting the same AEDs in 24/7 outdoor cabinets fixes that: 50 outdoor cabinets beat 200 indoor AEDs.

**[VISUAL]** Ablation table, with "own response time" crossed out.

> I also tested an idea I expected to work: putting AEDs where EMS has been slowest. It didn't help. Location explains only 7 percent of the variation in response time, so slow EMS is mostly bad luck, not geography.

**[VISUAL]** Figure 6 (fairness).

> Finally, fairness. I added a constraint so every neighborhood gets a fair share. Getting every group to 85 percent of the average costs less than 5 percent of the total benefit. But I proved that full fairness is impossible here: some suburbs just don't have enough buildings to host AEDs.

## 5. Prototype and close (3:05–3:45)

**[VISUAL]** Screen recording of the AED Placement Explorer. Drag the slider from 1 to 50 AEDs, toggle "24/7 cabinets", click a site popup.

> I built an interactive map so a city planner can add AEDs one at a time and see the expected benefit change live. All the code and data are open source.
>
> My recommendations for Virginia Beach: score sites by survival, not distance; plan with opening hours; use outdoor cabinets; and in sparse suburbs, add tools like drones or responder apps. When an AED can be reached matters as much as where it is. Thanks for watching.

---

## Recording tips

- Record each section separately. A mistake then costs one section, not the whole video.
- Use a headset microphone in a quiet room, and speak a little slower than feels natural.
- Free screen recorders: QuickTime (File → New Screen Recording) or OBS. Edit in iMovie or CapCut.
- Keep the final video under 4:00. Devpost judges stop at 4 minutes.
