"""Cross-check V-Dem transition years against BMR and Polity2 (pre-registered §II.5).
A V-Dem transition is 'confirmed' if the other source records a transition in the same
country within +/-2 years. Only transitions inside the other source's coverage are compared.
Output: outputs/validation_transitions.csv, outputs/validation_summary.csv"""
import pathlib, pandas as pd, numpy as np
R = pathlib.Path(__file__).resolve().parents[1]
v = pd.read_csv(R/'data/vdem_subset.csv.gz').sort_values(['country_text_id','year'])
t = pd.read_csv(R/'outputs/transitions.csv').drop(columns=['id_status','consensus_universe'], errors='ignore')
TOL = 2

def source_transitions(var, is_dem):
    out = {}
    cov = {}
    for cid, g in v.groupby('country_text_id'):
        g = g.dropna(subset=[var])
        if g.empty: continue
        dem = is_dem(g[var]).values; yrs = g.year.astype(int).values
        out[cid] = [yrs[i] for i in range(1, len(g)) if dem[i] and not dem[i-1]]
        cov[cid] = (yrs.min(), yrs.max())
    return out, cov

src = {'BMR': source_transitions('e_boix_regime', lambda s: s >= 1),
       'Polity2': source_transitions('e_polity2', lambda s: s >= 6)}
rows = []
for _, r in t.iterrows():
    row = dict(country=r.country, iso3=r.iso3, transition_year=r.transition_year, origin_locus=r.origin_locus)
    for name, (tr, cov) in src.items():
        c = cov.get(r.iso3)
        if c is None or not (c[0] < r.transition_year <= c[1]):
            row[name] = 'not covered'; continue
        near = [y for y in tr.get(r.iso3, []) if abs(y - r.transition_year) <= TOL]
        if near: row[name] = 'confirmed'
        else:
            # already democratic in that source at t (so no transition needed)
            g = v[(v.country_text_id == r.iso3) & (v.year == r.transition_year)]
            val = g['e_boix_regime' if name == 'BMR' else 'e_polity2'].iloc[0] if len(g) else np.nan
            already = (val >= 1) if name == 'BMR' else (val >= 6)
            row[name] = 'source already democratic' if already else 'not a democracy in source'
    rows.append(row)
vt = pd.DataFrame(rows)
vt.to_csv(R/'outputs/validation_transitions.csv', index=False)
summ = []
for name in src:
    s = vt[vt[name] != 'not covered']
    summ.append(dict(source=name, compared=len(s), confirmed=(s[name]=='confirmed').sum(),
        confirmed_pct=round(100*(s[name]=='confirmed').mean(),1),
        source_already_democratic=(s[name]=='source already democratic').sum(),
        not_democracy_in_source=(s[name]=='not a democracy in source').sum()))
either = vt[(vt.BMR != 'not covered') | (vt.Polity2 != 'not covered')]
summ.append(dict(source='Either', compared=len(either),
    confirmed=((either.BMR=='confirmed')|(either.Polity2=='confirmed')).sum(),
    confirmed_pct=round(100*((either.BMR=='confirmed')|(either.Polity2=='confirmed')).mean(),1)))
S = pd.DataFrame(summ); S.to_csv(R/'outputs/validation_summary.csv', index=False); print(S.to_string(index=False))
# by locus
vt['confirmed_either'] = (vt.BMR=='confirmed')|(vt.Polity2=='confirmed')
print(vt[(vt.BMR!='not covered')|(vt.Polity2!='not covered')].groupby('origin_locus').confirmed_either.agg(['count','mean']).round(2))

# ---- Consensus universe (Part II §II.7, defined after validation fell below 75%, before any model was run) ----
t = t.merge(vt[['iso3','transition_year','BMR','Polity2']], on=['iso3','transition_year'], how='left')
conf = (t.BMR == 'confirmed') | (t.Polity2 == 'confirmed')
conv = (~conf) & t.origin_locus.isin(['Restored','Independence']) & \
       ((t.BMR.isin(['source already democratic','not covered'])) & (t.Polity2.isin(['source already democratic','not covered'])))
t['id_status'] = np.select([conf, conv], ['confirmed', 'source convention'], 'disputed')
t['consensus_universe'] = t.id_status != 'disputed'
t.drop(columns=['BMR','Polity2']).to_csv(R/'outputs/transitions.csv', index=False)
print(t.id_status.value_counts().to_string())
print(t.groupby('origin_locus').consensus_universe.agg(['count','sum']).to_string())
