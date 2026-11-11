"""Pre-registered H3 mechanism tests (mu_research_8 §4).

M1 civil society x party institutionalisation   (interaction HR < 1)
M2 anti-system movements, attenuation            (antisys HR > 1 and CSO log-HR shrinks >= 1/3)
M3 civil society x social-group exclusion        (interaction HR > 1)
M4 local government x clientelism                (interaction HR > 1)
M5 artefact: polarisation + electoral autocracy  (CSO log-HR shrinks >= 1/3 and CI includes 1)
Outputs: outputs/mechanism_estimates.csv, outputs/mechanism_verdicts.csv, outputs/south_africa_trajectory.csv
"""
import pathlib, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
from lifelines import CoxPHFitter

warnings.filterwarnings('ignore')
R = pathlib.Path(__file__).resolve().parents[1]
T = pd.read_csv(R / 'outputs/transitions.csv')
T['event'] = T.breakdown.astype(int)
T['prior_dem'] = (T.prior_dem_years > 0).astype(int)
T['era'] = pd.cut(T.transition_year, [1945, 1973, 1999, 2024], labels=['e1946_73', 'e1974_99', 'e2000_24']).astype(str)
yc = (T.transition_year - 1985) / 20
T['yr1'], T['yr2'], T['yr3'] = yc, yc ** 2, yc ** 3
T['survived_10y_num'] = T.survived_10y.map({True: 1, False: 0, 'True': 1, 'False': 0})
T['elec_aut_t1'] = T.elec_aut_t1.map({True: 1, False: 0, 'True': 1, 'False': 0})

RAW = {'csopart': 'pre_cso_particip_10y', 'locgov': 'pre_locgov_10y', 'party': 'pre_party_10y',
       'antisys': 'pre_antisys_10y', 'exclusion': 'pre_exclusion_10y', 'client': 'pre_client_10y',
       'polar': 'pre_polar_10y'}


def prep(universe, needed):
    df = T if universe == 'U1' else T[T.consensus_universe]
    df = df.dropna(subset=['log_gdppc', 'educ'] + [RAW[k] for k in needed]).copy()
    for k in needed:
        df[k + '_z'] = (df[RAW[k]] - df[RAW[k]].mean()) / df[RAW[k]].std()
    return df


def design(df, hyp, timing):
    X = df[hyp + ['log_gdppc', 'educ', 'prior_dem']].astype(float)
    tim = pd.get_dummies(df[['era']], drop_first=True, dtype=float) if timing == 'era' else df[['yr1', 'yr2', 'yr3']]
    reg = pd.get_dummies(df[['region_pol']], drop_first=True, dtype=float)
    X = pd.concat([X, tim, reg], axis=1)
    return X.loc[:, X.std() > 0]


def cox(df, hyp, timing='era'):
    X = design(df, hyp, timing)
    d = pd.concat([X, df[['spell_years', 'event', 'iso3']]], axis=1)
    m = CoxPHFitter(penalizer=0.0)
    try:
        m.fit(d, 'spell_years', 'event', cluster_col='iso3')
    except Exception:
        m = CoxPHFitter(penalizer=0.01); m.fit(d, 'spell_years', 'event', cluster_col='iso3')
    s = m.summary
    return {v: (s.loc[v, 'coef'], s.loc[v, 'exp(coef)'], s.loc[v, 'exp(coef) lower 95%'], s.loc[v, 'exp(coef) upper 95%'], s.loc[v, 'p'])
            for v in hyp if v in s.index}, len(d), int(d.event.sum())


def firth(df, hyp):
    df = df[df.survived_10y_num.notna()]
    X = sm.add_constant(design(df, hyp, 'era')); Xa = X.values.astype(float); y = df.survived_10y_num.values.astype(float)
    b = np.zeros(Xa.shape[1])
    for _ in range(100):
        p = 1 / (1 + np.exp(-Xa @ b)); W = p * (1 - p)
        inv = np.linalg.pinv(Xa.T @ (Xa * W[:, None]))
        sw = Xa * np.sqrt(W)[:, None]; h = np.einsum('ij,jk,ik->i', sw, inv, sw)
        step = inv @ (Xa.T @ (y - p + h * (0.5 - p))); b += step
        if np.max(np.abs(step)) < 1e-8: break
    se = np.sqrt(np.diag(inv)); cols = list(X.columns)
    return {v: (b[cols.index(v)], np.exp(b[cols.index(v)]), np.exp(b[cols.index(v)] - 1.96 * se[cols.index(v)]),
                np.exp(b[cols.index(v)] + 1.96 * se[cols.index(v)]), np.nan) for v in hyp if v in cols}, len(df), int(y.sum())


rows = []


def rec(test, U, model, est, n, k, effect='HR'):
    for v, (c, e, lo, hi, p) in est.items():
        rows.append(dict(test=test, universe=U, model=model, variable=v, effect=effect, log_estimate=c,
                         estimate=e, ci_low=lo, ci_high=hi, p=p, n=n, events_or_successes=k))


INTER = {'M1': ('csopart', 'party'), 'M3': ('csopart', 'exclusion'), 'M4': ('locgov', 'client')}
for U in ['U1', 'U2']:
    for test, (a, b) in INTER.items():
        df = prep(U, [a, b]); iv = f'{a}_x_{b}'; df[iv] = df[a + '_z'] * df[b + '_z']
        hyp = [a + '_z', b + '_z', iv]
        rec(test, U, 'main_cox', *cox(df, hyp))
        rec(test, U, 'Ra_drop_short_reversals', *cox(df[~df.return_after_short_reversal], hyp))
        rec(test, U, 'Rb_firth_logit_survived10', *firth(df, hyp), effect='OR')
        rec(test, U, 'Rc_cubic_year', *cox(df, hyp, timing='cubic'))
    # attenuation tests share one sample so the CSO coefficients are comparable
    df = prep(U, ['csopart', 'locgov', 'antisys', 'polar']).dropna(subset=['elec_aut_t1'])
    base = ['locgov_z', 'csopart_z']
    rec('M2/M5', U, 'base_H3', *cox(df, base))
    rec('M2', U, 'add_antisys', *cox(df, base + ['antisys_z']))
    rec('M5', U, 'add_polar_elecaut', *cox(df, base + ['polar_z', 'elec_aut_t1']))

E = pd.DataFrame(rows)
E.to_csv(R / 'outputs/mechanism_estimates.csv', index=False)

# ---- verdicts ----
NULL = {'HR': 1, 'OR': 1}


def interaction_verdict(sub, var, sign):  # sign +1: predicted HR>1 ; -1: predicted HR<1
    def pdir(r):
        return sign if r.effect == 'HR' else -sign   # OR of survival flips
    def d(r):
        return np.nan if pd.isna(r.estimate) else (1 if r.estimate > 1 else -1)
    s = sub[sub.variable == var]
    main = s[s.model == 'main_cox'].iloc[0]; rob = s[s.model != 'main_cox']
    excl = main.ci_low > 1 or main.ci_high < 1
    same = sum(1 for _, r in rob.iterrows() if d(r) == pdir(r))
    if excl and d(main) != pdir(main): return 'Contradicted', same
    if excl and same >= 2: return 'Supported', same
    if d(main) == pdir(main) and same >= 2: return 'Suggestive', same
    return 'Inconclusive', same


V = []
for test, (a, b) in INTER.items():
    var = f'{a}_x_{b}'; sign = -1 if test == 'M1' else +1
    res = {U: interaction_verdict(E[(E.test == test) & (E.universe == U)], var, sign) for U in ['U1', 'U2']}
    order = ['Supported', 'Suggestive', 'Inconclusive', 'Contradicted']
    if 'Contradicted' in (res['U1'][0], res['U2'][0]):
        final = 'Contradicted' if res['U1'][0] == res['U2'][0] else 'Inconclusive'
    else:
        final = max(res['U1'][0], res['U2'][0], key=order.index)
    m = E[(E.test == test) & (E.universe == 'U1') & (E.model == 'main_cox') & (E.variable == var)].iloc[0]
    V.append(dict(test=test, key_term=var, predicted='HR<1' if sign < 0 else 'HR>1', estimate_U1=round(m.estimate, 2),
                  ci_U1=f'{m.ci_low:.2f} to {m.ci_high:.2f}', n_U1=m.n, verdict_U1=res['U1'][0],
                  robust_same_U1=f"{res['U1'][1]} of 3", verdict_U2=res['U2'][0], robust_same_U2=f"{res['U2'][1]} of 3",
                  final_verdict=final))

for test, model, added in [('M2', 'add_antisys', 'antisys_z'), ('M5', 'add_polar_elecaut', 'polar_z')]:
    ok = {}
    detail = {}
    for U in ['U1', 'U2']:
        b0 = E[(E.test == 'M2/M5') & (E.universe == U) & (E.variable == 'csopart_z')].iloc[0]
        b1 = E[(E.test == test) & (E.universe == U) & (E.model == model) & (E.variable == 'csopart_z')].iloc[0]
        shrink = 1 - (b1.log_estimate / b0.log_estimate) if b0.log_estimate != 0 else np.nan
        if test == 'M2':
            a = E[(E.test == test) & (E.universe == U) & (E.model == model) & (E.variable == 'antisys_z')].iloc[0]
            ok[U] = (a.estimate > 1) and shrink >= 1 / 3
            detail[U] = f'antisys HR {a.estimate:.2f} ({a.ci_low:.2f} to {a.ci_high:.2f}); CSO HR {b0.estimate:.2f} -> {b1.estimate:.2f} (shrink {shrink:.0%})'
        else:
            ok[U] = shrink >= 1 / 3 and b1.ci_low <= 1 <= b1.ci_high
            detail[U] = f'CSO HR {b0.estimate:.2f} -> {b1.estimate:.2f} (shrink {shrink:.0%}; CI {b1.ci_low:.2f} to {b1.ci_high:.2f})'
    final = 'Supported' if all(ok.values()) else ('Partial' if any(ok.values()) else 'Not supported')
    V.append(dict(test=test, key_term=added, predicted='attenuation', estimate_U1=np.nan, ci_U1=detail['U1'],
                  n_U1=int(E[(E.test == test) & (E.universe == 'U1')].n.iloc[0]), verdict_U1='met' if ok['U1'] else 'not met',
                  robust_same_U1='', verdict_U2='met' if ok['U2'] else 'not met', robust_same_U2=detail['U2'], final_verdict=final))
V = pd.DataFrame(V)
V.to_csv(R / 'outputs/mechanism_verdicts.csv', index=False)
pd.set_option('display.width', 260); pd.set_option('display.max_colwidth', 90)
print(V.to_string(index=False))

# ---- South Africa descriptive trajectory ----
v = pd.read_csv(R / 'data/vdem_subset.csv.gz')
za = v[(v.country_text_id == 'ZAF') & v.year.between(1980, 2025)][
    ['year', 'v2x_regime', 'v2x_polyarchy', 'v2csprtcpt_osp', 'v2xcs_ccsi', 'v2xel_locelec', 'v2xnp_client',
     'v2elsnlsff', 'v2xps_party', 'v2cacamps', 'v2csantimv']].round(3)
za.to_csv(R / 'outputs/south_africa_trajectory.csv', index=False)
