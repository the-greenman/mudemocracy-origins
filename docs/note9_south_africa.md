# South Africa: Is Local Democracy Practised or Only Named? — Study Design (draft)

*μDemocracy foundation evidence, research note 9. Drafted 11 November 2026. Status: **S1 frozen** (§5.1) on 11 November 2026, before any comparison between area types was run. S2–S4 remain drafts.*

## 1. The question

Notes 7 and 8 found that national counts of civil society and local government do not predict durable democracy, and may predict the opposite. The working explanation: an association or a council can be democratic in name while its internal life is not. Where there is no convivial democratic practice, "civil society" may be a set of competing autocracies — chiefs, party branches, patronage networks — each mobilising its own people.

South Africa is the test case because it has all three in one country: elected ward councillors, traditional councils in the former homelands, and dense party and civic organisation. It also has six rounds of local elections (2000–2021) plus the election of 4 November 2026.

## 2. What the 2026 election showed (provisional figures, 99.9% of voting districts counted)

- **Turnout rose** to about 52%, from 45.8% in 2021, the lowest on record.
- **No party dominates.** Ward ballot: ANC 30.6%, DA 24.5%, MKP 9.7%, EFF 6.2%.
- **Local organising is visible.** More than 230 parties took ward votes, many of them residents' forums and civic movements, and independents took about 1.0%.

Whether this is "desire for more democracy" or fragmentation is the empirical question. The study should be able to tell the two apart.

## 3. Concepts and how to measure them

| Concept | What it means | Candidate measure |
| --- | --- | --- |
| **Practice** | People meet and act together on shared problems | Afrobarometer: attended a community meeting; joined others to raise an issue |
| **Voice** | Speaking up is safe and is heard | Afrobarometer: free to say what you think; fear of political intimidation; councillors / traditional leaders "listen" |
| **Nominal structure** | Organisations and offices exist | Afrobarometer: member of a community group; contact with councillor, traditional leader, party official |
| **Competing autocracies** | High structure and mobilisation, low voice | High *nominal structure* with low *voice* in the same place |
| **Convivial democracy** | High practice and high voice | Both high in the same place |
| **Local democratic demand** | Voters using the local ballot | Turnout and its change 2021→2026; vote share of independents and local civic movements; ward competitiveness |
| **Local democratic failure** | Capture or breakdown | Audit outcomes; councils under administration; political killings; protest |

The central move is to separate **structure** from **voice**. National indices merge them. Afrobarometer asks about each separately, of the same person.

## 4. Data

Checked on 11 November 2026. "Verified" means the repository was cloned and its files inspected. None of these third-party copies has yet been checked against the official source.

| Need | Source | Unit and years | Status |
| --- | --- | --- | --- |
| Local election results | IEC raw files, copied in `Don4chnge/Eduvos-Team-DIRISA-2026` | Voting district; 2000, 2006, 2011, 2016, 2021 | Verified. Third-party copy: totals must be checked against IEC published figures. |
| 2026 results | `ubayd-hattas/SA_DataHub`, `ZolileN/count-room` | Municipality (213) | Verified but **provisional**: the two disagree on registered voters (28.6M vs 29.2M). Final ward-level files are on the IEC site only. |
| Boundary crosswalk, voting-age population | `jaydenmanca/DIRISA_PROJECT` | Municipality, 2000–2026 | Verified |
| Traditional-area exposure | Census 2022 10% sample, household `Geo_type` (same repo) | Municipality share of households in traditional areas | Verified. The coding (urban / traditional / farm) must be confirmed against Stats SA metadata. 2022 only. |
| Former homelands | `afrith/historical-boundary-data` | Transkei, Bophuthatswana, Venda, Ciskei polygons | Verified. The six self-governing homelands, including KwaZulu, are **missing**. |
| Census covariates | `afrith/census-2022-muni-stats` | Municipality; 2011, 2022 | Verified |
| Practice, voice, structure | Afrobarometer rounds 6 (2015) and 7 (2018), unofficial copy in `jayodele10/Afrobarometer` | Individual; municipality names in R6, districts in R7 | Verified, but labels are stripped and question columns are not yet identified. An unofficial copy should not be redistributed. |
| Coalitions and audits | `mapungubwe-institute/coalitions-barometer-data` (CC BY 4.0) | 80 municipalities, 2021–2026 | Verified |
| Violence proxy | SAPS crime by station, `afrith/crime-stats` | Station mapped to municipality; 2020–2025 | Verified (large file) |

**Needs a manual download** (the pipeline can only reach GitHub):

- **Afrobarometer** official South Africa files and codebooks, rounds 1–10, from afrobarometer.org/data (free, short form). This is the most important gap: it gives the practice and voice measures for 2000–2024 and a citable source.
- **IEC 2026 final results** at ward level, from results.elections.org.za.
- **Auditor-General audit outcomes** for all municipalities, from AGSA reports or the Municipal Money API.
- **Traditional council boundaries**, from the Municipal Demarcation Board or CoGTA, on request.
- **Political killings and protest**: Global Initiative assassination database (on request), ACLED (free account).

**What can be built now, from GitHub alone:** a municipality panel of six elections plus provisional 2026 (turnout, competitiveness, independents and civic-movement share), traditional-area exposure, census covariates, and Afrobarometer 2015 participation matched by municipality. That supports first tests of S1 and S3. S2 and S4 need the manual downloads.

## 5. Hypotheses

### 5.1 S1 — frozen before analysis

**Data.** Official Afrobarometer South Africa files, supplied by Greenman on 11 November 2026: rounds 4 (2008), 5 (2011), 6 (2015), 7 (2018), 8 (2021), 9 (2022) and 10 (2024). Three rounds record the type of each sampled area and so can identify traditional-authority areas directly:

| Round | Field | Traditional category | Respondents in it |
| --- | --- | --- | --- |
| 4 (2008) | `EA_GEOTYPE` | TRIBAL_AREA | 548 of 2,400 |
| 6 (2015) | `URBRUR_SAF` | Tribal | 612 of 2,390 |
| 7 (2018) | `EA_TYPE` | TRADITIONAL RESIDENTIAL | 460 of 1,840 |

This replaces the municipality-matching plan in §4 for S1: the comparison is made between respondents, inside the survey. Only the category counts above had been seen when this section was written.

**Measures** (each item coded 0/1; "don't know", refused and missing are dropped; an index is the mean of its available items):

| Index | Items |
| --- | --- |
| **Practice** | Attended a community meeting in the past year (at least once). Joined others to raise an issue (at least once). |
| **Structure** | Active member or leader of a voluntary association or community group. Active member or leader of a religious group. Contacted a local councillor in the past year (at least once). |
| **Voice** | Somewhat or completely free to say what you think. Never or rarely has to be careful what you say about politics. Fears political intimidation or violence "not at all" or "a little bit". |
| Being heard (reported separately) | Councillors "often" or "always" try to listen. |
| **Mobilised without voice** | Practice > 0 and Voice ≤ ⅓ |
| **Convivial** | Practice > 0 and Voice ≥ ⅔ |

**Hypothesis S1.** People in traditional-authority areas take part as much as others but are less free to speak. Specifically:

- **S1-voice:** Voice is lower in traditional areas.
- **S1-structure:** Practice and Structure are not lower in traditional areas.
- **S1-type:** "Mobilised without voice" is more common in traditional areas.

**Model.** Weighted least squares on pooled rounds 4, 6 and 7 with the survey weight (`withinwt`).
- Predictor: traditional area (1/0).
- Controls: round, province, age, sex, education level.
- Standard errors clustered by sampled area. The files carry no area identifier, so a cluster is defined as respondents in the same round sharing province, area type and all recorded area characteristics (the `EA_` fields).

**Robustness.**
- **R-a:** each round separately.
- **R-b:** rural respondents only (traditional areas against commercial-farm and other rural areas).
- **R-c:** only the six provinces that contain former homelands (Eastern Cape, Free State, KwaZulu-Natal, Limpopo, Mpumalanga, North West).

**Verdict rules.**

| Part | Supported | Contradicted |
| --- | --- | --- |
| S1-voice | Coefficient on Voice is negative with a 95% CI excluding 0, **and** negative in at least 2 of 3 single rounds, **and** negative in R-b and R-c | Positive with a 95% CI excluding 0 |
| S1-structure | Neither the Practice nor the Structure coefficient has a 95% CI lying wholly below 0 | Either CI lies wholly below 0 |
| S1-type | Coefficient on "mobilised without voice" is positive with a 95% CI excluding 0, and positive in at least 2 of 3 single rounds | Negative with a 95% CI excluding 0 |

S1 as a whole is **Supported** only if all three parts are. Anything else is reported part by part.

**Stated in advance.** This is a cross-section. A difference between area types shows that the pattern exists, not that traditional authority causes it: traditional areas are also poorer, more remote and overwhelmingly in the former homelands. R-b and R-c narrow that gap; they do not close it.

**Descriptive, no test.**
- Trends in each index for rounds 4–10, urban against rural, where the items exist.
- In round 4, whether traditional leaders or councillors are thought to listen more, by area type.

**Data handling.** The Afrobarometer files are not redistributed. The pipeline reads them from a local folder that is excluded from the repository, and records each file's SHA-256 hash so a rebuild can confirm it used the same files.

### 5.2 S2–S4 — drafts, not frozen

- **S2.** *Voice*, not *structure*, predicts good local outcomes (clean audits, fewer killings, less violent protest).
- **S3.** The 2021→2026 turnout rise and the civic-movement vote are concentrated where *practice* is high and satisfaction with councillors is low — demand for democracy, not apathy. Round 10 (2024) names the district or metro of each respondent (51 areas), which makes a district-level test possible once final 2026 results are published.
- **S4.** Where *structure* is high and *voice* is low, local competition takes violent or patronage forms.

## 6. S1 results (run after §5.1 was frozen)

Figures are from `outputs/sa_s1_verdicts.csv`, `sa_s1_estimates.csv`, `sa_s1_means.csv` and `sa_trends.csv` in the `mudemocracy-origins` repository. Sample: 6,630 respondents in rounds 4, 6 and 7, of whom 1,620 lived in traditional-authority areas.

### 6.1 Verdicts

| Part | Difference in traditional areas | 95% CI | Verdict |
| --- | --- | --- | --- |
| S1-voice | −0.012 (index 0–1) | −0.038 to 0.014 | **Inconclusive.** Lower in 1 of 3 rounds only. |
| S1-structure: Practice | **+0.062** | 0.020 to 0.103 | **Supported** |
| S1-structure: Structure | **+0.029** | 0.003 to 0.055 | **Supported** |
| S1-type: mobilised without voice | +0.026 (share) | −0.003 to 0.055 | **Inconclusive.** Higher in 1 of 3 rounds only. |
| **S1 overall** | | | **Not supported as a whole** |

Differences are adjusted for round, province, age, sex and education.

### 6.2 What it shows

**1. People in traditional areas take part more, not less.** They are about 6 points more likely to attend community meetings and to join others to raise an issue, and more likely to contact a councillor. This holds within the former-homeland provinces.

**2. They were less free to speak in 2008, but not since.**

| Year | Voice index, traditional | Voice index, elsewhere | Mobilised without voice, traditional | Elsewhere |
| --- | --- | --- | --- | --- |
| 2008 | 0.63 | 0.69 | 20% | 10% |
| 2015 | 0.80 | 0.74 | 7% | 10% |
| 2018 | 0.58 | 0.57 | 29% | 29% |

- In 2008 the "competing autocracies" pattern was there: twice as many people in traditional areas took part while not feeling free to speak (adjusted gap +8.5 points, CI 4.3 to 12.7).
- By 2015 the gap had closed or reversed, and in 2018 the two kinds of area were the same.
- One item still differs across the pooled rounds: fear of political intimidation or violence is about 4 points more common in traditional areas (CI 0.4 to 7.5), and 8 points more common than in other rural areas.

**3. The larger change is national, and it happened between 2015 and 2018.**

| Year | Attended a community meeting | Feel free to say what they think | Rarely or never careful what they say | Councillors listen |
| --- | --- | --- | --- | --- |
| 2008 | 48% urban / 57% rural | 77% / 78% | 58% / 49% | 30% / 30% |
| 2015 | 49% / 60% | 87% / 90% | 53% / 63% | 21% / 22% |
| 2018 | 67% / 71% | 64% / 64% | 35% / 36% | 19% / 26% |
| 2021 | 53% / 63% | 66% / 70% | 36% / 42% | 13% / 15% |
| 2022 | 47% / 51% | 73% / 81% | 49% / 45% | 21% / 25% |

- Between 2015 and 2018, participation rose and felt freedom to speak fell sharply, in town and country alike.
- The share who were "mobilised without voice" roughly tripled, from about 10% to about 29%, everywhere.
- Felt freedom partly recovered by 2022. Belief that councillors listen never recovered from its 2008 level.

**4. Who is heard.** In 2008, people in traditional areas were more likely to say traditional leaders listen (42%) than that councillors do (29%).

### 6.3 Reading for the μDemocracy thesis

- **The "democratic in name only" pattern is real and measurable.** Survey questions can separate taking part from being free to speak, and the two move independently. In 2018 they moved in opposite directions.
- **It is not mainly a traditional-authority problem.** The hypothesis that chiefs' areas are where participation lacks voice held in 2008 and not afterwards. The 2018 rise in "mobilised without voice" was national.
- **Participation is not the scarce thing; being heard is.** South Africans attend meetings at high rates. What fell, and stayed low, is the belief that anyone listens. This fits the note 8 finding that counts of participation do not predict durable democracy.
- **A candidate measure for μDemocracy:** the share of people who take part *and* feel free to speak ("convivial"), against the share who take part without feeling free ("mobilised without voice").

### 6.4 Limits

- **Cross-section.** These are differences between kinds of area, not effects of traditional authority.
- **Area type is the survey's own flag**, and its categories changed between rounds (tribal area, tribal, traditional residential).
- **Clusters are approximated**, because the files carry no sampled-area identifier.
- **The 2015→2018 shift needs checking** against question wording and fieldwork changes before it is treated as a real change in the country.
- **Round 10 (2024) is not yet used.** Its file has no question labels; the round 10 codebook is needed to place it on these trends.
- **One coding error was caught and fixed before the results were read as final:** "inactive member" had been counted as active membership. The fix followed the frozen definition; the Structure estimate fell from +0.040 to +0.029 and the verdict did not change.

### 6.5 Next

1. Add round 10 once its codebook is in hand, to see where voice stood in 2024, before the 2026 election.
2. Test S3 with round 10's district identifiers and final 2026 results: did turnout rise most where people take part but do not feel heard?
3. Check the 2015→2018 break against Afrobarometer's own technical notes.
