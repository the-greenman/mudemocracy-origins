"""EXPLORATORY (not pre-registered): how did each democratic spell end?
'erosion' = first non-democratic year is an electoral autocracy (elections continue);
'collapse' = closed autocracy (elections suspended: coups, self-coups, war).
Output: outputs/exploratory_breakdown_mode.csv, outputs/exploratory_mode_by_cso.csv"""
import pathlib, pandas as pd
R = pathlib.Path(__file__).resolve().parents[1]
T = pd.read_csv(R/'outputs/transitions.csv'); v = pd.read_csv(R/'data/vdem_subset.csv.gz')
b = T[T.breakdown].copy()
def mode(r):
    nxt = v[(v.country_text_id == r.iso3) & (v.year == r.spell_end_year + 1)]
    return 'unknown' if nxt.empty else ('erosion (electoral autocracy)' if nxt.v2x_regime.iloc[0] == 1 else 'collapse (closed autocracy)')
b['end_mode'] = b.apply(mode, axis=1)
s = b.dropna(subset=['pre_cso_particip_10y']).copy()
cut = T.pre_cso_particip_10y.quantile(2/3)
s['cso_third'] = (s.pre_cso_particip_10y >= cut).map({True: 'top third CSO', False: 'lower two-thirds CSO'})
s[['country','transition_year','spell_end_year','end_mode','pre_cso_particip_10y','elec_aut_t1','origin_category']].to_csv(R/'outputs/exploratory_breakdown_mode.csv', index=False)
tab = pd.crosstab(s.cso_third, s.end_mode); tab.to_csv(R/'outputs/exploratory_mode_by_cso.csv'); print(tab)
print(pd.crosstab(s.cso_third, s.elec_aut_t1))
