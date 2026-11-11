# Status and handoff (2026-11-11)

Research is paused here. This file says what exists, what it found, what is untested, and how to resume.

## What exists

| Part | Where | State |
| --- | --- | --- |
| Democratic origins dataset (V-Dem v16 transitions, origin rules, BMR/Polity validation) | `scripts/00`–`05`, `docs/note7_*` | Done, reproducible from pinned sources (`sources.lock`) |
| H1–H4 pre-registered models | `scripts/04_models.py`, `outputs/verdicts.csv` | Run; verdicts inconclusive or suggestive |
| H3 mechanisms M1–M5 (Weimar-style tests) | `scripts/06_mechanisms.py`, `docs/note8_*` | Run; none explains the H3 association |
| South Africa study, S1 (Afrobarometer R4–R10) | `scripts/10`, `11`, `docs/note9_*` | Run; verdicts frozen before analysis |
| Project copies of notes 7–9 | Claude project `claude/mu_research_{7,8,9}_*.md` | Current |
| Google-style Sheet "Democratic Origins Dataset" | Claude Docs sheet | Updated through H3; **not** updated with SA results |

## Findings so far (see the notes for caveats)

- **Origins (H1–H4):** no clear evidence that imposed democracies keep less democratic practice. H3 (more pre-transition civil society or local government goes with shorter-lived democracy) is the interesting result. It is an adverse association that none of the five mechanisms tested explains. The Weimar-style interaction (M1) points the opposite way from the prediction.
- **Breakdowns:** modern breakdowns are mostly gradual erosion (77 of 84), not coups.
- **South Africa S1:** participation is higher, and voice not lower, in traditional-authority areas overall. The 2008 pattern (about 20% vs 10% mobilised-without-voice) disappeared by 2015 and 2018. Felt freedom to speak fell nationally between 2015 and 2018 and again by 2024. Councillors-listen fell from about 30% (2008) to roughly 16–22% (2024).
- **Round 10 (2024)** only carries four comparable items. No Practice or Voice index can be built for 2024. Joining others to request action fell sharply, but the question format changed, so treat that with caution.

## Known limits

- Afrobarometer round 10 has 51 districts with a median of 24 respondents (min 4). District-level tests are not feasible; province-level is descriptive only.
- The 2015→2018 break has **not** been checked against Afrobarometer technical notes (wording or fieldwork changes).
- Local democracy and civil society can be democratic in name only. V-Dem and Afrobarometer measure formal participation, not convivial practice. This is the central measurement problem.
- Round 4–9 raw files are not redistributable: they live in `private/afrobarometer/` (gitignored). A fresh clone needs them re-downloaded from Afrobarometer and placed there, then `make sa`.

## Not yet done (in priority order)

1. **S3:** 2026 turnout vs "practice without being heard". Needs final IEC ward-level results, and province-level only unless a larger survey is found.
2. **Check the 2015→2018 break** against Afrobarometer round 6/7 technical notes.
3. **S2/S4:** need manual downloads (AGSA/Municipal Money audit outcomes, GI-TOC killings, ACLED protest data, IEC ward results). Pre-registered drafts are in note 9 §5.2.
4. **Pillarisation test:** use V-Dem party–civil-society linkage variables (`v2psorgs`, `v2pscohesv`, `v2psprlnks`) and pre-register a CSO × pillarisation interaction (note 8).
5. **Larger SA survey with local identifiers:** HSRC South African Social Attitudes Survey is a candidate; coverage and access unchecked.
6. **Pilot a "decision-record density" measure:** a direct measure of small-scale democratic practice, which links the research to the μDemocracy minutes and record-keeping work.
7. Update the Sheet with SA results.

## How to resume

```
git clone https://github.com/the-greenman/mudemocracy-origins
cd mudemocracy-origins
make all            # rebuild origins dataset from pinned sources
# place Afrobarometer files in private/afrobarometer/ (see note 9 §4), then:
make sa             # rebuild SA harmonisation and S1 tests
```

Working rules carried through all notes: define criteria and verdict rules before running any analysis, disclose deviations (see the revision logs in notes 7 and 9), keep everything reproducible from pinned public sources, and keep non-redistributable data out of git.
