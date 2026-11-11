"""Identify democratic transitions 1946-2024 and classify their origin.

Every rule is documented in mu_research_7 (Part I §4, Part II §II.2).
Input:  data/vdem_subset.csv.gz, data/navco2.csv
Output: outputs/transitions.csv
"""
import pathlib
import numpy as np
import pandas as pd

R = pathlib.Path(__file__).resolve().parents[1]
LOOK_END, LOOK_MOB, START, END = 5, 10, 1946, 2024
NAVCO_FIRST, NAVCO_LAST = 1945, 2006

ET = {0: 'Military coup', 1: 'Non-military coup', 2: 'Self-coup', 3: 'Assassination', 4: 'Natural death of leader',
      5: 'Loss in civil war', 6: 'Loss in inter-state war', 7: 'Foreign intervention', 8: 'Popular uprising',
      9: 'Guided liberalisation', 10: 'Other guided transformation', 11: 'Unguided liberalisation', 12: 'Other'}
REGGEO = {1: 'Western Europe', 2: 'Northern Europe', 3: 'Southern Europe', 4: 'Eastern Europe', 5: 'Northern Africa',
          6: 'Western Africa', 7: 'Middle Africa', 8: 'Eastern Africa', 9: 'Southern Africa', 10: 'Western Asia',
          11: 'Central Asia', 12: 'Eastern Asia', 13: 'South-Eastern Asia', 14: 'Southern Asia', 15: 'Oceania',
          16: 'North America', 17: 'Central America', 18: 'South America', 19: 'Caribbean'}
REGPOL = {1: 'Eastern Europe & Central Asia', 2: 'Latin America & Caribbean', 3: 'Middle East & North Africa',
          4: 'Sub-Saharan Africa', 5: 'Western Europe & North America', 6: 'Asia & Pacific'}
LOCUS = {'1': 'Imposed', '1b': 'Restored', '2': 'Independence', '3': 'External release', '10': 'Unresolved'}

d = pd.read_csv(R / 'data/vdem_subset.csv.gz').sort_values(['country_text_id', 'year'])
d['year'] = d.year.astype(int)
LAST = int(d.year.max())

nav = pd.read_csv(R / 'data/navco2.csv')


def navco_years(cow, y, nonviolent, goals):
    lo, hi = y - LOOK_MOB, y - 1
    if pd.isna(cow) or lo < NAVCO_FIRST or hi > NAVCO_LAST:
        return np.nan
    m = nav[(nav.cown == cow) & nav.year.between(lo, hi) & (nav.prim_method == nonviolent)]
    if goals is not None:
        m = m[m.camp_goals.isin(goals)]
    return float(m.year.nunique())


def latest(g, y, var, back=5):
    s = g[(g.year <= y) & (g.year >= y - back)].dropna(subset=[var])
    return float(s[var].iloc[-1]) if len(s) else np.nan


def at(g, y, var):
    r = g[g.year == y]
    return float(r[var].iloc[0]) if len(r) and pd.notna(r[var].iloc[0]) else np.nan


rows = []
for cid, g in d.groupby('country_text_id'):
    g = g.reset_index(drop=True)
    dem = (g.v2x_regime >= 2).values
    ends = g.groupby('v2regidnr').agg(endyear=('year', 'max'), et=('v2regendtype', 'last')).dropna()
    n = 0
    for i in range(len(g)):
        if not dem[i]:
            continue
        y = int(g.year[i])
        first_obs = i == 0
        if not first_obs and dem[i - 1]:
            continue  # continuing spell (or gap with democracy on both sides)
        n += 1
        if not (START <= y <= END):
            continue
        prev = None if first_obs else g.iloc[i - 1]
        j = i
        while j + 1 < len(g) and dem[j + 1] and g.year[j + 1] - g.year[j] == 1:
            j += 1
        spell_end = int(g.year[j])
        ongoing = spell_end == LAST
        state_ends = (not ongoing) and j + 1 >= len(g)  # no later V-Dem row: state ceased (e.g. GDR)

        win = ends[(ends.endyear >= y - LOOK_END) & (ends.endyear <= y) & (ends.et != 13)]
        ets = sorted(set(int(round(x)) for x in win.et))
        pre = g[(g.year >= y - LOOK_MOB) & (g.year < y)]
        winrows = g[(g.year >= y - LOOK_END) & (g.year <= y)]
        yrs_in = set(winrows.year)
        missing_years = len([z for z in range(max(y - LOOK_END, int(g.year.min())), y) if z not in yrs_in])
        prev_year = None if first_obs else int(prev.year)
        long_gap = prev_year is not None and (y - prev_year > LOOK_MOB)
        dom = None if first_obs or pd.isna(prev.v2svdomaut_osp) else float(prev.v2svdomaut_osp)
        dom_t = g.v2svdomaut_osp[i]
        dom_t = None if pd.isna(dom_t) else float(dom_t)
        foreign_control = (winrows.v2svdomaut_osp.min() < 1.5) or missing_years >= 2
        foreign_support = (not first_obs) and pd.notna(prev.v2regsupgroups_13) and prev.v2regsupgroups_13 >= 0.5
        same_regime = (not first_obs) and prev.v2regidnr == g.v2regidnr[i]
        lastdem = g[(g.year < y) & (g.v2x_regime >= 2)].year.max()
        gap = None if pd.isna(lastdem) else int(y - lastdem)
        restored = gap is not None and gap <= 10
        indep_prev = None if first_obs else prev.v2svindep
        gw = g[(g.year >= y - LOOK_MOB) & (g.year <= y)]
        indep_switch = bool(((gw.v2svindep.shift(1) == 0) & (gw.v2svindep == 1)).any()) or \
            bool((g[(g.year < y) & (g.year >= y - LOOK_MOB)].v2svindep == 0).any())

        # ---- origin rules, first match wins (Part I §4.2) ----
        if first_obs or long_gap or indep_switch:
            cat, rule = '2 Independence', 'R2'
        elif (7 in ets) or (6 in ets and foreign_control) or (dom is not None and dom < 0.5 and indep_prev == 1):
            cat, rule = ('1b Restoration after occupation', 'R1b') if restored else ('1 Foreign-imposed', 'R1')
        elif dom is not None and dom < 0.5:
            cat, rule = '2 Independence', 'R2b'
        elif dom is not None and dom < 1.5 and foreign_support:
            cat, rule = '3 Hegemon withdrawal', 'R3'
        elif 6 in ets:
            cat, rule = '4 War defeat (no occupation)', 'R4'
        elif 8 in ets:
            cat, rule = '5 Popular uprising', 'R5'
        elif any(e in (0, 1, 2, 3, 5) for e in ets):
            cat, rule = '6 Elite rupture', 'R6'
        elif 11 in ets:
            cat, rule = '7 Unguided liberalisation', 'R7'
        elif any(e in (9, 10) for e in ets):
            cat, rule = '8 Guided liberalisation', 'R8'
        elif same_regime:
            cat, rule = '9 Within-regime opening', 'R9'
        else:
            cat, rule = '10 Unresolved', 'R10'
        locus = LOCUS.get(cat.split()[0], 'Domestic')

        cow = g.COWcode[i]
        rows.append(dict(
            country=g.country_name[i], iso3=cid, cow=cow,
            region=REGGEO.get(int(g.e_regiongeo[i]), '') if pd.notna(g.e_regiongeo[i]) else '',
            region_pol=REGPOL.get(int(g.e_regionpol_6C[i]), '') if pd.notna(g.e_regionpol_6C[i]) else '',
            transition_year=y, transition_no=n, origin_category=cat, origin_locus=locus, rule_fired=rule,
            regime_end_types_window='; '.join(ET[e] for e in ets),
            domestic_autonomy_t1=None if dom is None else round(dom, 2), independent_t1=indep_prev,
            mob_years_10y=int((pre.v2cademmob_osp >= 2).sum()) if len(pre) else np.nan,
            mob3_years_10y=int((pre.v2cademmob_osp >= 3).sum()) if len(pre) else np.nan,
            mob_mean_10y=round(pre.v2cademmob_osp.mean(), 2) if len(pre) else np.nan,
            navco_unarmed_prodem_yrs=navco_years(cow, y, 1, [0, 1]),
            navco_unarmed_any_yrs=navco_years(cow, y, 1, None),
            navco_armed_prodem_yrs=navco_years(cow, y, 0, [0, 1]),
            prior_dem_years=int(((g.year < y) & (g.v2x_regime >= 2)).sum()),
            years_since_last_democracy=gap, return_after_short_reversal=(gap is not None and gap <= 5),
            pre_locgov_10y=round(pre.v2xel_locelec.mean(), 3) if len(pre) else np.nan,
            pre_cso_particip_10y=round(pre.v2csprtcpt_osp.mean(), 2) if len(pre) else np.nan,
            pre_ccsi_10y=round(pre.v2xcs_ccsi.mean(), 3) if len(pre) else np.nan,
            pre_engaged_10y=round(pre.v2dlengage_osp.mean(), 2) if len(pre) else np.nan,
            pre_party_10y=round(pre.v2xps_party.mean(), 3) if len(pre) else np.nan,
            pre_antisys_10y=round(pre.v2csantimv.mean(), 3) if len(pre) else np.nan,
            pre_exclusion_10y=round(pre.v2xpe_exlsocgr.mean(), 3) if len(pre) else np.nan,
            pre_client_10y=round(pre.v2xnp_client.mean(), 3) if len(pre) else np.nan,
            pre_polar_10y=round(pre.v2cacamps.mean(), 3) if len(pre) else np.nan,
            elec_aut_t1=(None if first_obs else bool(prev.v2x_regime == 1)),
            log_gdppc=round(np.log(latest(g, y, 'e_gdppc')), 3) if pd.notna(latest(g, y, 'e_gdppc')) else np.nan,
            educ=round(latest(g, y, 'e_peaveduc'), 2) if pd.notna(latest(g, y, 'e_peaveduc')) else np.nan,
            resource_pc=round(np.log1p(latest(g, y, 'e_total_resources_income_pc')), 3)
            if pd.notna(latest(g, y, 'e_total_resources_income_pc')) else np.nan,
            spell_end_year=spell_end, spell_years=spell_end - y + 1, ongoing_2025=ongoing,
            state_ceased=state_ends, breakdown=(not ongoing) and not state_ends,
            survived_10y=(np.nan if (y + 9 > LAST) else (spell_end >= y + 9)),
            polyarchy_t0=round(g.v2x_polyarchy[i], 3),
            ccsi_t10=at(g, y + 10, 'v2xcs_ccsi'), cso_particip_t10=at(g, y + 10, 'v2csprtcpt_osp'),
            locgov_t10=at(g, y + 10, 'v2xel_locelec'), engaged_society_t10=at(g, y + 10, 'v2dlengage_osp'),
            partipdem_t10=at(g, y + 10, 'v2x_partipdem'),
            ccsi_latest=round(g.v2xcs_ccsi.iloc[-1], 3), polyarchy_latest=round(g.v2x_polyarchy.iloc[-1], 3)))

out = pd.DataFrame(rows).sort_values(['transition_year', 'country']).reset_index(drop=True)
for c in ['ccsi_t10', 'locgov_t10', 'partipdem_t10']:
    out[c] = out[c].round(3)
for c in ['cso_particip_t10', 'engaged_society_t10']:
    out[c] = out[c].round(2)
out.to_csv(R / 'outputs/transitions.csv', index=False)
print(len(out), 'transitions;', out.iso3.nunique(), 'countries')
print(out.origin_category.value_counts().sort_index().to_string())
