# Democratic Origins Dataset — Methodology and Codebook (v0.2)

*μDemocracy foundation evidence, research note 7. Drafted 11 November 2026. v0.2: pre-registered analysis run (Part III). Status: open to revision.*

## 1. Purpose

The μDemocracy thesis is that national democracy rests on everyday practices of self-government ("small democracy"), and that democracy installed from above without those practices is brittle.

This dataset is the first step in testing that claim against the post-1945 record. It answers two questions:

1. **Origin.** For every country that became democratic between 1946 and 2024, did democracy arrive from outside (imposed, inherited at independence, released by a withdrawing hegemon) or from inside (uprising, elite rupture, negotiated or gradual opening)?
2. **Grassroots signal.** How much democratic practice existed before the transition, and did democracy then survive and deepen?

The design principle: **no country is classified by judgement.** Every category is assigned by a written rule applied mechanically to published expert data. Where a rule produces a doubtful result, the case is *flagged for review*, never silently recoded.

## 2. Sources

| Source | What it supplies | Version |
| --- | --- | --- |
| V-Dem Country-Year dataset (Varieties of Democracy Institute) | Regime classification, regime end type, autonomy, mobilisation, civil society and local government indicators | v16 (R package `vdemdata` 16.0, March 2026), coverage 1789–2025 |
| V-Dem Episodes of Regime Transformation (ERT) | Cross-check of transition years | v16 |

Literature that shaped the categories (used for definitions, not as data):

- Miller, *Shock to the System* (Princeton, 2021) — 139 transitions 1800–2014 coded by path (domestic shocks, international shocks, electoral continuity).
- Kadivar, "Mass Mobilization and the Durability of New Democracies," *ASR* 83(2), 2018; and *Popular Politics and the Path to Durable Democracy* (Princeton, 2022) — longer unarmed mobilisation predicts more durable democracy.
- Downes & Monten, "Forced to Be Free?" *International Security* 37(4), 2013 — foreign-imposed regime change rarely democratises unless prior representative experience, development and homogeneity are present; restorations are a distinct case.
- Nomikos (correspondence, 2013/14) — separates foreign-imposed *democratisation* (intended) from regime change generally.

Miller's case list (book appendix) and Kadivar's mobilisation coding are not published as downloadable data. They are planned as **validation sources** (§9), not inputs.

## 3. Unit of analysis

**A democratic transition** is a country-year *t* where:

- V-Dem's Regimes of the World indicator (`v2x_regime`) is 2 (electoral democracy) or 3 (liberal democracy) in year *t*; and
- it was 0 or 1 (closed or electoral autocracy) in the last observed year before *t*, or *t* is the country's first observed year.

Scope: 1946 ≤ *t* ≤ 2024. A country can have several transitions; `transition_no` counts them. Result: **159 transitions in 107 countries**, 1946–2024.

A **democratic spell** runs from *t* to the last consecutive year with `v2x_regime` ≥ 2.

## 4. Origin classification

### 4.1 Inputs (all from V-Dem, observed at or before *t*)

| Input | V-Dem variable | Definition used |
| --- | --- | --- |
| Regime end types in window | `v2regendtype`, `v2regidnr` | End type of every V-Dem regime whose last year falls in [*t*−5, *t*]. "Still exists" (13) is ignored. |
| Domestic autonomy at *t*−1 | `v2svdomaut_osp` (0–2) | < 0.5 = non-autonomous (colony/occupation); 0.5–1.5 = semi-autonomous (satellite/protectorate); ≥ 1.5 = autonomous |
| Foreign control in window | as above | Minimum autonomy in [*t*−5, *t*] below 1.5, **or** two or more missing country-years in that window (V-Dem omits years when a state was not sovereign, e.g. Germany 1945–48) |
| Independence | `v2svindep` | A 0→1 switch, or any non-independent year, within [*t*−10, *t*] |
| Foreign support | `v2regsupgroups_13` | Share of experts saying the regime relied on "a foreign government or colonial power" ≥ 0.5 at *t*−1 |
| Recent democracy | `v2x_regime` history | Years since the last democratic year before *t* (`years_since_last_democracy`) |

### 4.2 Rules, applied in order (first match wins)

| Rule | Category | Condition |
| --- | --- | --- |
| R2 | **2 Independence** | New state first observed as democratic; or independence gained within 10 years; or state re-emerges after >10 years without a V-Dem record (e.g. Baltic states 1990) |
| R1 / R1b | **1 Foreign-imposed**, or **1b Restoration after occupation** | A regime in the window ended by *foreign intervention* (7); **or** by *loss in inter-state war* (6) while foreign control was present; **or** the state was independent but non-autonomous at *t*−1. If the country had been democratic within the previous 10 years → **1b Restoration**, otherwise **1 Foreign-imposed** |
| R2b | **2 Independence** | Non-autonomous and not independent at *t*−1 (colonial rule) |
| R3 | **3 Hegemon withdrawal** | Semi-autonomous at *t*−1 **and** the regime relied on a foreign power |
| R4 | **4 War defeat (no occupation)** | Loss in inter-state war in the window, state autonomous throughout |
| R5 | **5 Popular uprising** | A regime in the window ended by popular uprising (8) |
| R6 | **6 Elite rupture** | Ended by coup, self-coup, assassination or civil-war loss (0, 1, 2, 3, 5) |
| R7 | **7 Unguided liberalisation** | Ended by liberalisation *not* guided by sitting leaders, e.g. unexpected election loss (11) |
| R8 | **8 Guided liberalisation** | Ended by liberalisation or transformation guided by sitting leaders (9, 10) |
| R9 | **9 Within-regime opening** | No regime ended in the window; the same V-Dem regime governed on both sides of the threshold (Miller's "electoral continuity": e.g. Mexico, Taiwan, Senegal) |
| R10 | **10 Unresolved** | None of the above (currently 0 cases) |

### 4.3 Locus (the summary question: imposed or self-made?)

| Locus | Categories | Meaning |
| --- | --- | --- |
| Imposed | 1 | Built under foreign control, with no recent democratic past |
| Restored | 1b | Foreign power removed an occupier and a recent democracy resumed |
| Independence | 2 | Democracy arrived with statehood. Ambiguous for this question: an independence movement can itself be mass practice (India). Read alongside mobilisation. |
| External release | 3 | Domestic actors democratised once an external hegemon let go |
| Domestic | 4–9 | Democracy arrived through processes inside the country |

### 4.4 Why these choices

- **Windows.** The 5-year end-type window catches multi-step transitions, such as Portugal's 1974 coup followed by guided liberalisation to 1976. The 10-year mobilisation window follows the scale of Kadivar's duration measure.
- **Precedence.** External conditions are tested before domestic ones because the research question is about outside installation.
- **Restoration is separated** because Downes & Monten show that restoring a previous democracy says nothing about building one. Norway and the Netherlands in 1945 are not Japan in 1952.
- **War defeat alone is not imposition.** Greece in 1974 lost in Cyprus, but Greeks rebuilt their own democracy.

## 5. Grassroots indicators (the "small democracy" proxies)

All are averages over the 10 years before *t*, so they describe the society the democracy was born into.

| Field | V-Dem source | What it captures | Known weakness |
| --- | --- | --- | --- |
| `mob_years_10y` | `v2cademmob_osp` ≥ 2 | Years with *many* pro-democracy mobilisation events (Kadivar-style duration) | Measures protest events, not organisation. Older decades are thinly coded. |
| `pre_locgov_10y` | `v2xel_locelec` | Elected local government operating without unelected interference | Formal institutions, not lived practice. Colonial local councils score high. |
| `pre_cso_particip_10y` | `v2csprtcpt_osp` (0–3) | Whether being active in voluntary associations is normal | Expert perception. Can rise in unstable hybrid regimes. |
| `pre_ccsi_10y` | `v2xcs_ccsi` | Civil society autonomy and activity | Mostly measures state repression of CSOs |
| `prior_dem_years` | `v2x_regime` | Years of national democracy before *t* | National, not small, democracy; Downes & Monten's "prior experience" |

Civil society is a poor proxy for small democracy, as noted at the outset. These fields are carried because they are the best cross-national series available, not because they measure the thing itself.

## 6. Outcomes

| Field | Definition |
| --- | --- |
| `spell_years` | Length of the democratic spell beginning at *t* |
| `survived_10y` | Spell lasted ≥ 10 years. Left blank ("not yet observable") where *t* + 9 > 2025 |
| `ongoing_2025` | Spell still running in 2025, the last V-Dem year |
| `broke_down` | Spell ended before 2025 (includes GDR, which ended by unification) |
| `ccsi_t10`, `cso_particip_t10`, `locgov_t10`, `engaged_society_t10`, `partipdem_t10` | The same grassroots indicators measured 10 years after *t*: did small democracy deepen? |

## 7. Inference policy

1. **No hand-coding.** A country's category comes only from the rules in §4.2. Changing a classification means changing a rule, which applies to every case.
2. **Rules are fixed before results.** Rules were revised during development only to correct category errors visible in well-documented cases (the liberated Western European democracies were first caught as "imposed"; Namibia and the Baltic states as "foreign" or "unresolved"; Malaysia 2023 as "hegemon withdrawal"). Each revision changed a definition, not a case, and is logged in §10.
3. **Review flags, not recoding.** Doubtful outputs carry a `review_flag` explaining the doubt: Cyprus 1975, Madagascar 1994, Bosnia 1997, Libya 2013, GDR 1990, Malaysia 2023.
4. **Every field cites its V-Dem variable.** The build script is reproducible from V-Dem v16.

## 8. First-pass results (descriptive only)

| Locus | Transitions | Survived 10 yrs* | Median spell (yrs) |
| --- | --- | --- | --- |
| Restored | 8 | 88% | 80 |
| Imposed | 7 | 71% | 51 |
| Independence | 32 | 72% | 23 |
| External release | 4 | 100% | 36 |
| Domestic | 108 | 62% | 11 |

*Share of transitions that can be observed for 10 years.

**What this does and does not show.**

- **Imposed democracies are few and unusual.** Seven cases. The durable ones (Germany, Italy, Japan) are exactly the cases Downes & Monten describe: wealthy, homogeneous, with prior representative institutions. Libya (2013, lasted one year) is the typical modern case.
- **The headline is confounded by era.** Transitions from 1946–73 survived at 86%, from 1974–99 at 73%, and from 2000–24 at 45%. Imposed and restored cases cluster in the post-war period.
- **Mobilisation does not yet show Kadivar's effect overall.** Within the 1974–99 wave, the gradient points his way: 10-year survival is 69% with no mobilisation years, 75% with 1–4, and 78% with 5–10. In the other eras it is flat or reversed.
- **High pre-transition CSO participation is associated with *lower* survival in every era.** One plausible reading is that busy civil society in a hybrid regime marks contested, unstable politics. That would echo Berman's Weimar warning. This needs testing, not narrating.

**Conclusion of the first pass.** The dataset does not yet support or refute the μDemocracy thesis. It establishes the case universe and an origin coding that can be audited. The proxies are still too crude to settle the question.

## 9. Next steps

1. **Validate the origin coding** against Miller's appendix list (139 transitions with paths). Report agreement rates by category.
2. **Replicate Kadivar's measure.** Mobilisation *duration* from NAVCO (Chenoweth) campaign data, rather than V-Dem event intensity.
3. **Add controls** before any inference: GDP per capita (Maddison/V-Dem `e_gdppc`), era, region, and ethnic fractionalisation. Use survival models rather than percentages.
4. **Find better small-democracy proxies**, for example:
   - cooperative density (ICA)
   - union density (ILO/ICTWSS)
   - World Values Survey active association membership
   - historical local self-government (pre-colonial councils, municipal charters)
5. **Define "lasting democratic practice" for imposed cases**: whether post-transition local government and engaged-society scores rose and stayed up.

## 10. Rule revision log

| # | Change | Cases affected | Reason |
| --- | --- | --- | --- |
| 1 | Added R9 Within-regime opening | 45 cases (now) assigned | Threshold crossed with no regime change (Miller's electoral continuity) |
| 2 | Loss in war counts as imposition only with foreign control | Greece 1975 → War defeat | War defeat without occupation is domestically rebuilt |
| 3 | Added 1b Restoration (democratic within 10 years) | Belgium, Denmark, Netherlands, Norway, Luxembourg, France 1946–47; Solomon Islands | Restorations differ from installation (Downes & Monten) |
| 4 | Independence tested first; missing-record re-emergence counts | Namibia, Baltic states, Armenia → Independence | New statehood is its own origin |
| 5 | Hegemon withdrawal requires a foreign support group | Malaysia 2023 out | Autonomy score alone was not discriminating |
| 6 | Missing country-years count as foreign control | Germany 1949 → Imposed | V-Dem omits occupied 1945–48 |

## Part II — Pre-registered analysis plan (v0.2)

*Written and saved to the project on 11 November 2026, **before** any model below was run. Results are reported against these criteria, whatever they show.*

### II.1 Hypotheses

The μDemocracy thesis predicts:

- **H1 — Origin.** Democracies whose origin locus is *Imposed*, *Independence* or *External release* break down sooner than *Domestic* ones, holding constant wealth, education, prior democratic experience, era and region.
- **H2 — Unarmed mobilisation (Kadivar replication).** More years of primarily *nonviolent* campaigns for regime change or institutional reform in the 10 years before transition → lower hazard of breakdown. *Armed* campaigns are expected to show no such benefit; this is the contrast that identifies organisation rather than conflict.
- **H3 — Grassroots infrastructure.** Higher pre-transition local self-government (`pre_locgov_10y`) and CSO participation (`pre_cso_particip_10y`) → lower hazard of breakdown.
- **H4 — Practice deepening.** Among democracies that survive 10 years, imposed-origin cases show a smaller rise in grassroots indicators (CSO participation, local government, engaged society) from the 10 years before to year *t*+10 than domestic-origin cases.

The first-pass descriptives (Part I §8) already pointed against H3. It is kept as written: the plan must not be edited to fit what we have seen.

### II.2 New data (all pinned; see §II.6)

| Field | Source | Definition |
| --- | --- | --- |
| `navco_unarmed_prodem_yrs` | NAVCO 2.0 campaign-years (Chenoweth & Lewis 2013), via `xmarquez/AuthoritarianismBook` | Distinct years in [*t*−10, *t*−1] with ≥ 1 campaign in the country (matched on COW code) where `prim_method` = 1 (nonviolent) and `camp_goals` ∈ {0 regime change, 1 institutional reform} |
| `navco_unarmed_any_yrs` | as above | Same, any goal (adds policy change, secession, autonomy, anti-occupation) |
| `navco_armed_prodem_yrs` | as above | Same as the first, but `prim_method` = 0 (violent) |
| `log_gdppc` | V-Dem `e_gdppc` (Fariss et al.) | Natural log of GDP per capita, latest non-missing value in [*t*−5, *t*] |
| `educ` | V-Dem `e_peaveduc` | Mean years of education, 15+, latest in [*t*−5, *t*] |
| `resource_pc` | V-Dem `e_total_resources_income_pc` | log(1 + resource income per capita), latest in [*t*−5, *t*] |
| `bmr_transition` | V-Dem `e_boix_regime` (Boix, Miller & Rosato) | Year BMR codes 0→1 |
| `polity_transition` | V-Dem `e_polity2` | Year Polity2 crosses from < 6 to ≥ 6 |

**NAVCO coverage rule.** NAVCO 2.0 runs 1945–2006. H2 uses only transitions where the full window lies inside coverage: 1956 ≤ *t* ≤ 2007. Everywhere else NAVCO fields are left blank, never zero.

### II.3 Models

**Breakdown.** One row per transition. Time = `spell_years`. Event = spell ended before 2025 **and** the state continued to exist (GDR 1990 is censored, not a breakdown).

**Main model: Cox proportional hazards.**
- Covariates: the hypothesis variable(s), `log_gdppc`, `educ`, `prior_dem` (any prior democratic year, 0/1), era (1946–73 / 1974–99 / 2000–24) and political region (V-Dem `e_regionpol_6C`).
- Standard errors clustered by country.
- Hazard ratio (HR) < 1 = longer survival.

| Model | Hypothesis variable(s) | Sample |
| --- | --- | --- |
| M1 | Origin locus (reference = Domestic) | All transitions |
| M2 | `navco_unarmed_prodem_yrs` and `navco_armed_prodem_yrs` | 1956–2007 |
| M3 | `pre_locgov_10y` and `pre_cso_particip_10y`, standardised (per 1 SD) | All transitions |
| M4 | OLS on Δ grassroots index (mean of the three standardised changes), Imposed vs Domestic, same controls, robust SEs | Transitions that survived 10 years |

### II.4 Robustness checks (each hypothesis)

- **R-a:** drop returns after short reversals (`return_after_short_reversal` = yes).
- **R-b:** logistic model of `survived_10y` instead of Cox.
- **R-c:** replace era and region with a cubic in transition year plus region (H1–H3); for H2, also use `navco_unarmed_any_yrs`.

### II.5 Decision criteria

| Verdict | Condition |
| --- | --- |
| **Supported** | Main-model estimate in the predicted direction with the 95% CI excluding no effect, **and** same sign in at least 2 of 3 robustness checks |
| **Suggestive** | Predicted direction in the main model and at least 2 robustness checks, but the CI includes no effect |
| **Inconclusive** | Mixed signs, or CI includes no effect with no consistent direction |
| **Contradicted** | Main-model CI excludes no effect in the *opposite* direction |

**Transition identification (validation, descriptive).** A V-Dem transition counts as *confirmed* by BMR or Polity if that source records a transition in the same country within ±2 years. Agreement of ≥ 75% with either source is taken as adequate. Below that, the case universe itself is revisited before any substantive claim.

**Miller validation** is deferred until the appendix list is available.

### II.6 Reproducibility

- All inputs are fetched from public git repositories at pinned commits (`sources.lock`).
- Python packages are pinned (`requirements.txt`).
- `make all` rebuilds every table from raw sources. No intermediate file is edited by hand. A file's SHA-256 is recorded in the output manifest.

### II.7 Revision triggered by §II.5 (recorded before any model was run)

**What triggered it.** V-Dem transition years were confirmed by BMR or Polity2 (±2 years) in **60.4%** of the 134 comparable cases (BMR 49.3%, Polity2 47.6%), below the pre-set 75%.

**Diagnosis.** The disagreement is mostly definitional:

- **Stricter threshold.** BMR and Polity2 are minimalist measures that count competitive elections. V-Dem's Regimes of the World also requires elections to be reasonably free and fair. Many V-Dem transitions — especially *Within-regime openings*, such as El Salvador 1999, Guatemala 2000, Philippines 2010 — are quality upgrades of countries the other sources already code as democratic.
- **Coverage conventions.** BMR and Polity2 do not code wartime occupation or colonial periods, so restorations (Belgium, Netherlands, Norway 1946) and new states (Botswana 1967) cannot appear as transitions there.
- **Other differences.** Some transitions are dated 3–5 years apart, and some V-Dem spells last three years or less.

**Rule added.** Each transition receives an `id_status`:

| Status | Condition | Count |
| --- | --- | --- |
| Confirmed | BMR or Polity2 records a transition within ±2 years | 81 |
| Source convention | Origin locus is Restored or Independence, and both sources are either already democratic or do not cover the year | 26 |
| Disputed | Neither of the above | 52 |

The **consensus universe** is the 107 transitions that are *confirmed* or *source convention*.

**How results are read.** Every model in §II.3 is run on both the full V-Dem universe (U1, as pre-registered) and the consensus universe (U2). A hypothesis is reported as **supported** only if it meets §II.5 in *both*. Where the two differ, the verdict is the weaker of the two.


## Part III — Results of the pre-registered analysis (v0.2)

*Run 11 November 2026 after Part II was saved. Every number below comes from `outputs/verdicts.csv` and `outputs/model_estimates.csv`, and a clean rebuild reproduces both byte for byte.*

### III.1 Verdicts

| Hypothesis | Variable | Main estimate (U1) | 95% CI | N | Verdict U1 / U2 | **Final** |
| --- | --- | --- | --- | --- | --- | --- |
| H1 Origin | Imposed vs Domestic | HR 0.66 | 0.09–4.82 | 105 | Inconclusive / Inconclusive | **Inconclusive** |
| H1 Origin | Independence vs Domestic | HR 0.80 | 0.24–2.61 | 105 | Inconclusive / Inconclusive | **Inconclusive** |
| H1 Origin | External release vs Domestic | HR 0.21 | 0.03–1.49 | 105 | Inconclusive / Inconclusive | **Inconclusive** |
| H2 Unarmed mobilisation | NAVCO nonviolent pro-democracy years | HR 0.92 per year | 0.75–1.13 | 79 | Suggestive / Suggestive | **Suggestive** |
| H3 Grassroots infrastructure | Local self-government (per SD) | HR 1.17 | 0.90–1.53 | 101 | Inconclusive / Inconclusive | **Inconclusive** (leans against) |
| H3 Grassroots infrastructure | CSO participation (per SD) | HR 1.46 | 0.96–2.20 | 101 | Inconclusive / Inconclusive | **Inconclusive** (leans against) |
| H4 Practice deepening | Imposed vs Domestic, Δ grassroots (SD) | −0.46 | −1.47 to 0.55 | 70 | Suggestive / Suggestive | **Suggestive** (fragile) |

HR < 1 means longer survival. Hazard ratios are from Cox models with country-clustered SEs, controlling for log GDP per capita, education, prior democracy, era and region. The consensus universe (U2) gave the same verdicts throughout.

**Nothing is Supported. Nothing is Contradicted.**

### III.2 What each result means

**H1 — Origin does not visibly predict survival once wealth and education are held constant.**
- All three "external" loci point the *opposite* way from the prediction (HR < 1), but the intervals are very wide.
- Only 7 imposed cases enter the model, with 2 breakdowns. The data cannot tell origin apart from the conditions Downes & Monten identified: imposed democracies that lasted (Germany, Italy, Japan) were rich and educated.
- **Reading:** origin as such is not the story. If it matters, it works through the conditions that came with it.

**H2 — Weak support for Kadivar, and the key contrast fails.**
- Each extra year of nonviolent pro-democracy campaigning goes with about 8% lower breakdown hazard, the same direction in every check, but not statistically distinguishable from no effect.
- The identifying contrast did *not* hold. Years of **armed** pro-democracy campaigns show an equal or stronger association (HR 0.80, CI 0.61–1.03).
- Kadivar's finding is therefore not cleanly reproduced with NAVCO 2.0, these controls, and this case universe. The likely reasons:
  - NAVCO 2.0 is campaign-level and sparse: the median case has zero campaign years.
  - The sample is 79 transitions.
  - Kadivar used his own original coding.

**H3 — Pre-transition civil society and local government go with *shorter* survival.**
- This is the same sign in every specification. With the CSO measure it is near the conventional threshold (p ≈ 0.07).
- Under the pre-set rules the verdict is Inconclusive, not Contradicted, because the intervals include no effect. The pattern is consistent, though, and should be stated plainly: **on these proxies, more pre-existing civil society did not protect new democracies.**
- Two readings remain open:
  - **The proxies are wrong.** Expert-rated CSO participation and formal local government are not lived democratic practice. This is the "poor proxy" problem flagged at the outset.
  - **The Berman effect.** Associational life in a contested hybrid regime can mark polarised, unstable politics rather than democratic habit.
- These readings make different predictions and can be separated with better data (§III.4).

**H4 — Suggestive by the rules, but the raw data runs the other way.**
- Before controls, imposed democracies deepened grassroots practice *more* than domestic ones: +0.98 vs +0.21 SD, a change from the 10 years before to year *t*+10.
- Post-war West Germany's engaged-society score rose from 0.3 to 3.6 on a 0–5 scale.
- The negative adjusted coefficient rests on 5 imposed cases and is driven by the controls. **It should not be cited as evidence that imposed democracies fail to grow small democracy.** Read with the raw data, it is closer to the opposite.

### III.3 Deviations and limits, all disclosed

1. **Transition validation fell below threshold (60% vs 75%).** This triggered §II.7. Verdicts were identical in both universes.
2. **The pre-registered logistic check (R-b) was not estimable** anywhere: perfect separation, because every Western Europe & North America case survived. Verdicts were therefore judged on 2 of 2 available robustness checks. An *unplanned* Firth-penalised logit (`unplanned_estimates.csv`) agrees in direction for H2 and H3.
3. **Education data ends around 2010**, so the main models drop post-2015 transitions (N 155 → 105). An *unplanned* model without education (N = 155) gives the same directions and the same lack of significance.
4. **Small numbers.** The theoretically central categories are tiny: Imposed n = 7, External release n = 4. Cross-national statistics cannot settle H1 on its own.

### III.4 What this means for the μDemocracy thesis

The national-level, cross-country record **does not yet show** that democratic practice beforehand makes new democracies last. It does not refute it either. Three things follow:

- **The proxy problem is the binding constraint.** V-Dem measures civil society *as seen by country experts*, not people practising self-government. The thesis needs measures of practice: decision-making in associations, cooperatives, unions, congregations and local assemblies.
- **Imposed democracies are the wrong test case.** They are too few, too rich and too post-war. The richer test is *within* countries: do regions or towns with denser self-government sustain democracy better? Italy is the obvious case (Putnam's *Making Democracy Work*), and India's panchayats offer another.
- **Unarmed mobilisation remains the most promising lead,** in line with Kadivar, and it is the one closest to the thesis: organisation-building *as* democratic practice. It needs a better campaign-duration measure than NAVCO 2.0 provides.

### III.5 Next steps (proposed)

1. Get Kadivar's replication data (ask the author) or NAVCO 1.3 / 3.0, and re-run H2 under the same pre-registered rules.
2. Build a **practice** measure: union density (ICTWSS / ILO), cooperative membership (ICA), and World Values Survey *active* membership. Define the measure before seeing the results, as here.
3. Design a within-country study (Italian regions, Indian states, or UK local authorities), where small democracy can be measured directly.
4. Validate the origin coding against Miller's appendix list when it is available.

## Files

- **Dataset Sheet:** "Democratic Origins Dataset" (tabs: Transitions, Verdicts, Model estimates, Validation, Summary, Codebook)
- **Pipeline:** `mu-origins` (scripts, `sources.lock`, `requirements.txt`, Makefile). `make all` rebuilds every output, and `outputs/MANIFEST.json` holds their SHA-256 hashes.
- **Pinned sources:**
  - `vdeminstitute/vdemdata` @ f4dd269 (V-Dem v16)
  - `xmarquez/AuthoritarianismBook` @ 5171622 (NAVCO 2.0 selection)
