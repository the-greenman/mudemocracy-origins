"""Write the tables used in the Sheet and a SHA-256 manifest of every output."""
import pathlib, hashlib, json, subprocess, pandas as pd
R = pathlib.Path(__file__).resolve().parents[1]
O = R / 'outputs'
T = pd.read_csv(O / 'transitions.csv')
FLAGS = {('Cyprus', 1975): 'V-Dem codes the 1974 Turkish intervention as ending the junta-backed regime; arguably a restoration',
         ('Madagascar', 1994): 'Regime end type "foreign intervention" is unusual here; verify against case literature',
         ('Bosnia and Herzegovina', 1997): 'Dayton settlement was internationally supervised; V-Dem codes regime end as civil-war loss',
         ('Libya', 2013): 'Lasted 1 year; NATO intervention 2011',
         ('German Democratic Republic', 1990): 'State ceased to exist (unification); censored, not a breakdown',
         ('Malaysia', 2023): 'Semi-autonomy score below 1.5 but no foreign support group, so not hegemon withdrawal'}
T['review_flag'] = [FLAGS.get((c, y), '') for c, y in zip(T.country, T.transition_year)]
first = ['country', 'iso3', 'transition_year', 'origin_category', 'origin_locus', 'id_status', 'consensus_universe',
         'mob_years_10y', 'navco_unarmed_prodem_yrs', 'navco_armed_prodem_yrs', 'prior_dem_years', 'pre_locgov_10y',
         'pre_cso_particip_10y', 'log_gdppc', 'educ', 'spell_years', 'breakdown', 'survived_10y', 'ongoing_2025', 'review_flag']
T = T[first + [c for c in T.columns if c not in first]]
for c in T.columns:
    if T[c].dtype == bool or set(T[c].dropna().unique()) <= {True, False}:
        T[c] = T[c].map({True: 'yes', False: 'no'})
T['survived_10y'] = T.survived_10y.fillna('not yet observable')
T.to_csv(O / 'sheet_transitions.csv', index=False)
E = pd.read_csv(O / 'model_estimates.csv').round(3); E.to_csv(O / 'sheet_estimates.csv', index=False)
manifest = {'sources': {}, 'outputs': {}}
for line in (R / 'sources.lock').read_text().splitlines():
    if line and not line.startswith('#'):
        n, u, c = line.split(); manifest['sources'][n] = {'url': u, 'commit': c}
for f in sorted(O.glob('*.csv')):
    manifest['outputs'][f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
(O / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2))
print(json.dumps(manifest['outputs'], indent=1))
