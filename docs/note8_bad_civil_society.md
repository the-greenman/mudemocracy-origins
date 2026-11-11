# When Civil Society Doesn't Protect Democracy — Investigating H3

*μDemocracy foundation evidence, research note 8. Started 11 November 2026. Follows note 7 (Democratic Origins Dataset), Part III.*

## 1. The puzzle

In note 7, the more civil society and local self-government a country had in the decade before democratising, the *sooner* its new democracy tended to collapse. The sign was the same in every specification:

- CSO participation: hazard ratio 1.46 per SD (95% CI 0.96–2.20)
- Local self-government: hazard ratio 1.17 per SD (95% CI 0.90–1.53)

Under the pre-set rules the verdict was Inconclusive, but the direction is the opposite of the μDemocracy thesis. That makes it the most important result in note 7.

## 2. What the literature says about the "dark side"

**Weimar Germany — Berman (1997).** Dense associational life was organised in parallel pillars (socialist, Catholic, nationalist). In the absence of strong political institutions, it became the infrastructure the Nazis captured. Her formula: *high associationism + weak political institutions = instability.*

**Bowling for Fascism — Satyanath, Voigtländer & Voth (*Journal of Political Economy* 125(2), 2017).** Association density in 229 interwar German towns was measured directly, and political and religious groups were excluded.
- One SD more associations went with at least 15% faster Nazi Party entry.
- All types predicted entry, both "bridging" and "bonding": choirs, animal breeders, gymnasts and veterans alike.
- Crucially, in federal states with more stable governments, association density was **not** correlated with faster Nazi entry.

The danger was conditional on weak government.

**Civic foundations of fascism — Riley (2010).** In Italy, Spain and Romania, fascism arose where voluntary associations grew quickly but dominant-class political parties stayed weak. This is a "crisis of hegemony": civil society outran political organisation. The form of fascism tracked the form of civil society (autonomous in Italy, elite-dominated in Spain, state-dominated in Romania).

**Intercommunal vs intracommunal — Varshney (2002).** Across Indian cities, Hindu–Muslim riots were rare where associational life was *intercommunal*: integrated business groups, unions, parties and professional bodies. Riots were frequent where it was organised only *within* each community. The difference is structure, not density.

**Decentralised despotism — Mamdani (1996).** Colonial indirect rule governed rural Africans through state-appointed "Native Authorities" that defined custom. Local power became ethnic and authoritarian; apartheid's Bantu Authorities Act (1951) was its fullest form. After independence, local institutions inherited that shape. Local government was a channel for ethnic clientage rather than a school of democracy.

**South Africa after 1994.**
- **Traditional authority.** Ntsebeza (*Democracy Compromised*, 2005) shows that traditional authorities, despite their apartheid role, gained powers in rural governance. The 2003 framework risked "imposing chiefs on an unwilling population". Studies of KwaZulu-Natal municipalities record standing tension between chiefs and elected councillors.
- **The Moerane Commission** (KwaZulu-Natal, 2018) found "overwhelming evidence" that access to resources through the tender system was the main root cause of the murder of politicians. Killings were concentrated at local level, among councillors and branch leaders of all parties.
- **The finding.** The South African case shows two distinct local pathologies:
  - *ethnic or traditional authority*, the "tribal faction" route;
  - *patronage competition over state resources*, the tender route.

  The commission's evidence points mainly to the second, though in practice the two interlock.
- **National democracy survived.** V-Dem codes South Africa as democratic continuously from 1995. Local pathology has not, so far, broken national democracy.

**Counterpoint — Bermeo (*Ordinary People in Extraordinary Times*, 2003).** Interwar European and Latin American breakdowns were driven more by elites misreading or manipulating mass polarisation than by ordinary citizens' associations turning anti-democratic. On this view, civil society is not the causal actor at all.

## 3. Five candidate explanations for H3

| Code | Mechanism | Source | What it predicts in our data |
| --- | --- | --- | --- |
| **M1** | Civil society outruns political institutions | Berman; Riley; Satyanath et al. | The CSO effect is harmful where parties are weakly institutionalised and fades where they are strong |
| **M2** | "Bad" civil society: anti-system movements | Berman; Chambers & Kopstein (2001) | Anti-system movement strength predicts breakdown and accounts for part of the CSO effect |
| **M3** | Segmented (bonding) civil society | Varshney; Mamdani; Weimar pillars | The CSO effect is harmful where power and access are organised by social group, such as ethnicity, caste or religion |
| **M4** | Patronage capture of local government | Mamdani; the South Africa tender evidence | Local self-government is harmful where politics is clientelistic |
| **M5** | Measurement artefact: contested hybrid regimes | Methodological alternative | The CSO effect disappears once polarisation and pre-transition regime type are controlled for |

These are not mutually exclusive. M1–M4 are *substantive*: civil society can work against democracy under identifiable conditions. M5 says the result is a *selection effect*: countries democratising out of contested hybrid regimes have busy civil societies and fragile democracies, without one causing the other.

## 4. Pre-registered tests (saved before any test was run)

**Sample and base model.**
- Same as note 7 §II.3: Cox model of breakdown, controlling for log GDP per capita, education, prior democracy, era and political region.
- Country-clustered SEs.
- Run on both the full universe (U1) and the consensus universe (U2).

**New pre-transition measures** (V-Dem v16, means over [*t*−10, *t*−1], each standardised across the analysis sample):

| Field | Variable | Higher means |
| --- | --- | --- |
| `party_z` | `v2xps_party`, party institutionalisation | Stronger parties |
| `antisys_z` | `v2csantimv`, CSO anti-system movements | More anti-system activity |
| `exclusion_z` | `v2xpe_exlsocgr`, exclusion by social group | More group-based exclusion |
| `client_z` | `v2xnp_client`, clientelism index | More clientelistic |
| `polar_z` | `v2cacamps`, political polarisation | More polarised |
| `elec_aut_t1` | `v2x_regime` = 1 at *t*−1 | Electoral (not closed) autocracy before transition |

**Tests and predictions.**

| Test | Model adds | Supporting result |
| --- | --- | --- |
| M1 | `csopart_z`, `party_z`, `csopart_z × party_z` | Interaction HR **< 1** |
| M2 | `antisys_z` to the note-7 H3 model | `antisys_z` HR **> 1**, **and** the log-HR of `csopart_z` shrinks by ≥ ⅓ |
| M3 | `csopart_z`, `exclusion_z`, `csopart_z × exclusion_z` | Interaction HR **> 1** |
| M4 | `locgov_z`, `client_z`, `locgov_z × client_z` | Interaction HR **> 1** |
| M5 | `polar_z` and `elec_aut_t1` to the note-7 H3 model | The log-HR of `csopart_z` shrinks by ≥ ⅓ **and** its 95% CI includes 1 |

**Robustness checks** (for M1, M3 and M4):
- **R-a:** drop returns after short reversals.
- **R-b:** Firth-penalised logit of 10-year survival. It is pre-specified here because the plain logit is known to be inestimable.
- **R-c:** cubic in transition year instead of era dummies.

**Verdicts.**
- **M1, M3, M4:** the §II.5 rules of note 7 apply. *Supported* needs a main-model CI that excludes no effect **and** the predicted direction in ≥ 2 of 3 robustness checks, in **both** universes.
- **M2, M5** (attenuation tests): *Supported* if the condition holds in both universes. *Partial* if it holds in one. *Not supported* otherwise.
- **Power warning, stated in advance:** with ~100 transitions and ~58 breakdowns, interaction tests have low power. An Inconclusive verdict here means "not detectable with this data", not "absent".

**Descriptive case study (no test).** South Africa's V-Dem trajectories for 1980–2025: CSO participation, local government, clientelism, subnational election unevenness, and party institutionalisation.


## 5. Results (run after §4 was saved to the project)

All figures come from `outputs/mechanism_verdicts.csv` and `outputs/mechanism_estimates.csv` in the `mudemocracy-origins` pipeline.

### 5.1 Verdicts

| Test | Key term | Predicted | Estimate (U1) | 95% CI | U1 / U2 | **Final** |
| --- | --- | --- | --- | --- | --- | --- |
| M1 Institutions | CSO × party institutionalisation | HR < 1 | **1.22** | 0.91–1.63 | Inconclusive / **Contradicted** (HR 1.51, 1.09–2.07) | **Inconclusive, runs opposite** |
| M2 Anti-system | Anti-system movements, attenuation | HR > 1 and ≥ ⅓ shrink | HR 1.00; CSO effect shrinks 0% | 0.72–1.39 | not met / not met | **Not supported** |
| M3 Segmentation | CSO × social-group exclusion | HR > 1 | 0.93 | 0.68–1.27 | Inconclusive / Inconclusive | **Inconclusive** |
| M4 Patronage capture | Local government × clientelism | HR > 1 | 0.87 | 0.65–1.16 | Inconclusive / Inconclusive | **Inconclusive** |
| M5 Artefact | Polarisation + electoral autocracy, attenuation | ≥ ⅓ shrink, CI includes 1 | CSO HR 1.46 → 1.40 (10% shrink) | 0.90–2.18 | not met / not met (19%) | **Not supported** |

**None of the five mechanisms explains the H3 pattern.** Across every model, the adverse association between pre-transition civil society and survival barely moves (CSO HR 1.40–1.52 per SD).

### 5.2 What this tells us

**1. The Weimar mechanism, as usually stated, does not travel to post-1945 national data.** Berman, Riley and Satyanath et al. all predict that civil society becomes dangerous where political institutions are *weak*. We find the opposite tendency:
- The adverse association is *stronger* where parties are *more* institutionalised.
- In the consensus universe the interaction clears conventional significance in two of three Cox models.

One reading, which is a hypothesis for testing and not a finding: the dangerous configuration may be civil society *bound to* strong parties. That means party-aligned unions, movements and ethnic associations, the "pillarised" form of Weimar itself, not civil society outrunning weak parties. Examples would be liberation-movement alliances, ethnic party machines, and party-affiliated unions.

**2. Neither "bad civil society" nor polarisation accounts for it.**
- Anti-system movement strength predicts nothing (HR 1.00).
- Adding polarisation and pre-transition regime type removes only 10–19% of the effect.
- The result is not obviously a selection artefact of contested hybrid regimes.

**3. Segmentation and patronage show no national-level signal.** The Varshney and Mamdani mechanisms (M3, M4) both point weakly in the *opposite* direction. That is not evidence against them. Both are claims about the **structure** of local associational life: whether it bridges groups, and who controls local office. A national expert average cannot see structure. Varshney's own evidence is a comparison *between cities within one country*.

**4. Exploratory, not pre-registered: how democracies end.**
- 77 of 84 breakdowns were *erosion* into electoral autocracy, with elections continuing. Only 7 were *collapse* into closed autocracy.
- This holds equally for high- and low-civil-society cases (29 of 31 vs 48 of 53).
- Nearly every transition, whatever its civil society level, followed an electoral autocracy.

So "breakdown" in the modern record mostly means executive-led backsliding, not Weimar-style mass capture. This did not distinguish high-civil-society cases, but it reframes the question. Busy civil societies may be the ones where incumbents can *mobilise* supporters to erode institutions. That fits the Philippines 2016, Zambia, Kenya and Nigeria among the high-civil-society breakdowns.

### 5.3 South Africa (descriptive)

V-Dem trajectories, 1985 → 1995 → 2024:

| Indicator | 1985 | 1995 | 2024 |
| --- | --- | --- | --- |
| CSO participation (0–3) | 2.10 | 2.73 | 2.40 |
| Core civil society index | 0.28 | 0.98 | 0.92 |
| Local government index | 0.70 | 0.70 → 0.96 (2000) | 0.88 |
| Clientelism index | 0.44 | 0.31 | 0.27 |
| Party institutionalisation | 0.66 | 0.76 | 0.72 |
| Regime | Closed autocracy | Electoral democracy → liberal (2000) | Electoral democracy (down from liberal in 2015) |

- **National indicators look healthy.** South Africa has very high civil society participation, elected local government, falling clientelism and a democracy that has lasted 31 years. It is a high-civil-society case that *did not* break down, a counterexample to the cross-national tendency.
- **The local pathologies are real, but invisible nationally.** Traditional-authority power in the former homelands (Ntsebeza) and tender-driven killings of councillors (Moerane Commission) do not register in V-Dem's national scores. The country-level clientelism index actually *fell*.
- **It suggests a different danger.** Local democracy can be captured, by chiefs or by patronage networks, while national democracy stays formally intact. Gibson calls this "subnational authoritarianism".

The danger to μDemocracy may be less "civil society destroys national democracy" (Weimar) and more "**small democracy is hollowed out or captured locally**, while national democracy continues in form".

### 5.4 Conclusions for the μDemocracy thesis

1. **H3 is real enough to take seriously and remains unexplained.** At national level, more civil society before the transition goes with shorter-lived democracy. None of the standard "dark side" mechanisms accounts for it.
2. **"Is it Weimar again?" — not in the simple form.** The weak-institutions version predicts the opposite of what we see. A *pillarised* version, with civil society fused to strong partisan blocs, is consistent with the data and worth testing directly.
3. **Structure, not density, is what the thesis needs to measure.** Every serious account (Varshney, Berman's pillars, Mamdani) says the *kind* of associational life matters:
   - bridging or bonding;
   - autonomous or party-bound;
   - democratic in its internal procedure or not.

   This is exactly what μDemocracy's own unit, the **recorded decision of a small group**, could measure and national indices cannot.
4. **The right next study is subnational.** South Africa's municipalities offer a natural design: traditional-authority areas against non-traditional areas, comparing local democratic quality (ward committees, councillor violence, service protest) over 1995–2025. The KwaZulu-Natal killings data (Moerane; Mary de Haas's monitoring) and Municipal Demarcation Board and IEC results are candidate sources.

### 5.5 Proposed next steps

- **Measure pillarisation directly** with V-Dem party–civil society linkage variables (`v2psorgs`, `v2pscohesv`, and `v2psprlnks` with its linkage types). Pre-register the CSO × pillarisation hypothesis before running it.
- **Scope a South Africa municipal dataset**: wards, traditional-authority overlap, election results, recorded councillor violence, and protest events.
- **Pilot "decision-record density" as a direct measure of small-democracy practice** in one place, such as Tower Hamlets co-ops and associations. It records internal procedure and bridging, not just counts of organisations.
