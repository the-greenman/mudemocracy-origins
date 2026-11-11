# Rebuild everything from pinned public sources:  make all
PY ?= python3 -I
all: outputs/MANIFEST.json

raw/.fetched: sources.lock scripts/00_fetch.sh
	bash scripts/00_fetch.sh && touch $@
data/vdem_subset.csv.gz: raw/.fetched scripts/01_extract.py
	$(PY) scripts/01_extract.py
outputs/transitions.csv: data/vdem_subset.csv.gz scripts/02_transitions.py scripts/03_validate_transitions.py
	$(PY) scripts/02_transitions.py && $(PY) scripts/03_validate_transitions.py
outputs/verdicts.csv: outputs/transitions.csv scripts/04_models.py
	$(PY) scripts/04_models.py
outputs/MANIFEST.json: outputs/verdicts.csv scripts/05_exports.py
	$(PY) scripts/05_exports.py

clean:
	rm -rf data/*.csv* outputs/* raw
.PHONY: all clean
