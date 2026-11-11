# μDemocracy — Democratic Origins Dataset

Every democratic transition from 1946 to 2024, classified by **how democracy arrived** (imposed, restored, independence, external release, domestic). Each one carries measures of grassroots democratic practice before and after, and the transitions are tested against pre-registered hypotheses.

The methodology, codebook, pre-registered analysis plan and results are in the project document `mu_research_7_democratic_origins_dataset.md`.

## Rebuild

```
pip install -r requirements.txt
make all
```

- Every raw source is fetched from a public git repository at the commit pinned in `sources.lock`.
- No file is edited by hand.
- `outputs/MANIFEST.json` records the SHA-256 of every output, so a rebuild can be checked byte for byte.

| Step | Script | Output |
| --- | --- | --- |
| Fetch | `00_fetch.sh` | `raw/` (V-Dem v16 via `vdemdata`; NAVCO 2.0 via `AuthoritarianismBook`) |
| Extract | `01_extract.py` | `data/vdem_subset.csv.gz`, `data/navco2.csv` |
| Transitions and origin rules | `02_transitions.py` | `outputs/transitions.csv` |
| Validation and consensus universe | `03_validate_transitions.py` | `outputs/validation_*.csv` |
| Pre-registered models and verdicts | `04_models.py` | `outputs/model_estimates.csv`, `outputs/verdicts.csv`, `outputs/unplanned_estimates.csv` |
| H3 mechanism tests (pre-registered, note 8) | `06_mechanisms.py` | `outputs/mechanism_*.csv`, `outputs/south_africa_trajectory.csv` |
| Exploratory: how breakdowns ended (not pre-registered) | `07_exploratory_breakdown_mode.py` | `outputs/exploratory_*.csv` |
| Exports and manifest | `05_exports.py` | `outputs/sheet_*.csv`, `outputs/MANIFEST.json` |

## Sources (please cite)

- Coppedge et al., *V-Dem Country-Year Dataset v16*, Varieties of Democracy Project. This includes Boix, Miller & Rosato (BMR) and Polity2.
- Chenoweth & Lewis, "Unpacking nonviolent campaigns: Introducing the NAVCO 2.0 dataset", *Journal of Peace Research* 50(3), 2013. The selection used here is redistributed by X. Marquez.

## Research notes

- `docs/note7_democratic_origins.md` covers the dataset, methodology, the pre-registered plan for H1–H4, and results.
- `docs/note8_bad_civil_society.md` covers H3 ("when civil society doesn't protect democracy"): the literature, pre-registered mechanism tests M1–M5, results, and the South Africa case.
- `docs/note9_south_africa.md` covers the South Africa study: design, the frozen S1 test of participation and voice in traditional-authority areas, and results.

## South Africa study

`make sa` runs it. It needs the official Afrobarometer South Africa files (rounds 4-9), which are free from afrobarometer.org/data but may not be redistributed. Put them in `private/afrobarometer/`. `outputs/sa_input_hashes.csv` lists the SHA-256 of each file used, and `outputs/sa_ab_labels_audit.csv` shows how every answer was coded. No respondent-level data is committed.
