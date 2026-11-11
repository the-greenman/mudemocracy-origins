"""Pre-registered models (mu_research_7, Part II §II.3-II.5, §II.7).

Runs H1-H4 on U1 (all V-Dem transitions) and U2 (consensus universe), applies the
pre-set verdict rules, and writes:
  outputs/model_estimates.csv   every estimate
  outputs/verdicts.csv          one verdict per hypothesis variable and universe
Unplanned analyses are written separately to outputs/unplanned_estimates.csv.
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
for loc in ['Imposed', 'Independence', 'External release', 'Restored']:
    T['loc_' + loc.replace(' ', '_')] = (T.origin_locus == loc).astype(int)
T['survived_10y_num'] = T.survived_10y.map({True: 1, False: 0, 'True': 1, 'False': 0})

# H4 outcome: mean of standardised changes in three grassroots indicators
pairs = [('cso_particip_t10', 'pre_cso_particip_10y'), ('locgov_t10', 'pre_locgov_10y'),
         ('engaged_society_t10', 'pre_engaged_10y')]
ch = pd.DataFrame({a: T[a] - T[b] for a, b in pairs})
T['d_grassroots'] = ((ch - ch.mean()) / ch.std()).mean(axis=1, skipna=False)

LOCI = ['loc_Imposed', 'loc_Independence', 'loc_External_release', 'loc_Restored']
HYP = {
    'H1': dict(vars=LOCI, test=['loc_Imposed', 'loc_Independence', 'loc_External_release'], sign=+1),
    'H2': dict(vars=['navco_unarmed_prodem_yrs', 'navco_armed_prodem_yrs'], test=['navco_unarmed_prodem_yrs'], sign=-1),
    'H3': dict(vars=['z_locgov', 'z_csopart'], test=['z_locgov', 'z_csopart'], sign=-1),
}


def dummies(df, cols):
    return pd.get_dummies(df[cols], drop_first=True, dtype=float)


def design(df, hyp_vars, timing):
    X = df[hyp_vars + ['log_gdppc', 'educ', 'prior_dem']].astype(float)
    tim = dummies(df, ['era']) if timing == 'era' else df[['yr1', 'yr2', 'yr3']]
    reg = dummies(df, ['region_pol'])
    return pd.concat([X, tim, reg], axis=1)


def sample(universe, hyp):
    df = T if universe == 'U1' else T[T.consensus_universe]
    if hyp == 'H2':
        df = df[df.navco_unarmed_prodem_yrs.notna()]
    df = df.dropna(subset=['log_gdppc', 'educ']).copy()
    if hyp == 'H3':
        df = df.dropna(subset=['pre_locgov_10y', 'pre_cso_particip_10y'])
        df['z_locgov'] = (df.pre_locgov_10y - df.pre_locgov_10y.mean()) / df.pre_locgov_10y.std()
        df['z_csopart'] = (df.pre_cso_particip_10y - df.pre_cso_particip_10y.mean()) / df.pre_cso_particip_10y.std()
    return df


def drop_constant(X):
    return X.loc[:, X.std() > 0]


def cox(df, hyp_vars, timing='era'):
    X = drop_constant(design(df, hyp_vars, timing))
    d = pd.concat([X, df[['spell_years', 'event', 'iso3']]], axis=1)
    m = CoxPHFitter(penalizer=0.0)
    try:
        m.fit(d, 'spell_years', 'event', cluster_col='iso3')
    except Exception:
        m = CoxPHFitter(penalizer=0.01)
        m.fit(d, 'spell_years', 'event', cluster_col='iso3')
    s = m.summary
    out = {}
    for v in hyp_vars:
        if v in s.index:
            out[v] = (s.loc[v, 'exp(coef)'], s.loc[v, 'exp(coef) lower 95%'], s.loc[v, 'exp(coef) upper 95%'], s.loc[v, 'p'])
    return out, len(d), int(d.event.sum())


def logit(df, hyp_vars, timing='era'):
    df = df[df.survived_10y_num.notna()]
    X = sm.add_constant(drop_constant(design(df, hyp_vars, timing)))
    y = df.survived_10y_num.astype(float)
    try:
        m = sm.Logit(y, X).fit(disp=0, cov_type='cluster', cov_kwds={'groups': pd.factorize(df.iso3)[0]}, maxiter=200)
        if not m.mle_retvals.get('converged', True):
            raise RuntimeError('no convergence')
    except Exception:
        return {v: (np.nan, np.nan, np.nan, np.nan) for v in hyp_vars}, len(df), int(y.sum())
    out = {}
    ci = m.conf_int()
    for v in hyp_vars:
        if v in m.params.index:
            b = m.params[v]
            if abs(b) > 15:  # quasi-separation: not estimable
                out[v] = (np.nan, np.nan, np.nan, np.nan)
            else:
                out[v] = (np.exp(b), np.exp(ci.loc[v, 0]), np.exp(ci.loc[v, 1]), m.pvalues[v])
    return out, len(df), int(y.sum())


rows = []


def record(hyp, universe, model, est, n, k, effect):
    for v, (e, lo, hi, p) in est.items():
        rows.append(dict(hypothesis=hyp, universe=universe, model=model, variable=v, effect=effect,
                         estimate=e, ci_low=lo, ci_high=hi, p=p, n=n, events_or_successes=k))


for U in ['U1', 'U2']:
    for h, cfg in HYP.items():
        base = sample(U, h)
        est, n, k = cox(base, cfg['vars']); record(h, U, 'main_cox', est, n, k, 'HR')
        ra = base[~base.return_after_short_reversal]
        est, n, k = cox(ra, cfg['vars']); record(h, U, 'Ra_drop_short_reversals', est, n, k, 'HR')
        est, n, k = logit(base, cfg['vars']); record(h, U, 'Rb_logit_survived10', est, n, k, 'OR')
        vars_c = cfg['vars'] if h != 'H2' else ['navco_unarmed_any_yrs', 'navco_armed_prodem_yrs']
        bc = base.dropna(subset=['navco_unarmed_any_yrs']) if h == 'H2' else base
        est, n, k = cox(bc, vars_c, timing='cubic')
        if h == 'H2':
            est = {'navco_unarmed_prodem_yrs': est['navco_unarmed_any_yrs'], **{k2: v2 for k2, v2 in est.items() if k2 != 'navco_unarmed_any_yrs'}}
        record(h, U, 'Rc_cubic_year' + ('_anygoal' if h == 'H2' else ''), est, n, k, 'HR')

    # H4: OLS on change in grassroots index, survivors only
    df = T if U == 'U1' else T[T.consensus_universe]
    df = df[(df.survived_10y_num == 1)].dropna(subset=['d_grassroots', 'log_gdppc', 'educ'])
    for model, sub, timing in [('main_ols', df, 'era'), ('Ra_drop_short_reversals', df[~df.return_after_short_reversal], 'era'),
                               ('Rc_cubic_year', df, 'cubic')]:
        X = sm.add_constant(drop_constant(design(sub, LOCI, timing)))
        m = sm.OLS(sub.d_grassroots, X).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(sub.iso3)[0]})
        ci = m.conf_int()
        est = {'loc_Imposed': (m.params['loc_Imposed'], ci.loc['loc_Imposed', 0], ci.loc['loc_Imposed', 1], m.pvalues['loc_Imposed'])} \
            if 'loc_Imposed' in m.params else {}
        record('H4', U, model, est, len(sub), np.nan, 'coef')

E = pd.DataFrame(rows)
E.to_csv(R / 'outputs/model_estimates.csv', index=False)


# ---- verdicts (§II.5) ----
def predicted(effect, sign_cox):
    """Return +1 if 'predicted direction' means estimate > null, else -1, for this effect type."""
    if effect == 'HR':
        return sign_cox
    if effect == 'OR':
        return -sign_cox          # higher hazard <=> lower odds of survival
    return sign_cox               # H4 coef: predicted negative (sign -1)


def verdict(sub, sign_cox):
    null = {'HR': 1, 'OR': 1, 'coef': 0}
    def direction(r):
        if pd.isna(r.estimate):
            return np.nan
        return 1 if r.estimate > null[r.effect] else -1
    def ci_excludes(r):
        nl = null[r.effect]
        return pd.notna(r.ci_low) and (r.ci_low > nl or r.ci_high < nl)
    main = sub[sub.model.str.startswith('main')].iloc[0]
    rob = sub[~sub.model.str.startswith('main')]
    pm = predicted(main.effect, sign_cox)
    dm = direction(main)
    rob_same = sum(1 for _, r in rob.iterrows() if pd.notna(direction(r)) and direction(r) == predicted(r.effect, sign_cox))
    rob_avail = sum(1 for _, r in rob.iterrows() if pd.notna(direction(r)))
    need = 2 if rob_avail >= 3 else rob_avail
    if pd.isna(dm):
        return 'Not estimable', rob_same, rob_avail
    if ci_excludes(main) and dm != pm:
        return 'Contradicted', rob_same, rob_avail
    if ci_excludes(main) and dm == pm and rob_same >= need:
        return 'Supported', rob_same, rob_avail
    if dm == pm and rob_same >= need:
        return 'Suggestive', rob_same, rob_avail
    return 'Inconclusive', rob_same, rob_avail


SIGN = {'H1': +1, 'H2': -1, 'H3': -1, 'H4': -1}
TEST = {'H1': HYP['H1']['test'], 'H2': HYP['H2']['test'], 'H3': HYP['H3']['test'], 'H4': ['loc_Imposed']}
V = []
for h in SIGN:
    for v in TEST[h]:
        res = {}
        for U in ['U1', 'U2']:
            sub = E[(E.hypothesis == h) & (E.universe == U) & (E.variable == v)]
            res[U] = verdict(sub, SIGN[h]) if len(sub) else ('Not estimable', 0, 0)
        order = ['Supported', 'Suggestive', 'Inconclusive', 'Not estimable', 'Contradicted']
        if 'Contradicted' in (res['U1'][0], res['U2'][0]):
            final = 'Contradicted' if res['U1'][0] == res['U2'][0] else 'Inconclusive'
        else:
            final = max(res['U1'][0], res['U2'][0], key=order.index)
        mU1 = E[(E.hypothesis == h) & (E.universe == 'U1') & (E.variable == v) & E.model.str.startswith('main')].iloc[0]
        V.append(dict(hypothesis=h, variable=v, main_estimate_U1=round(mU1.estimate, 2),
                      ci_U1=f"{mU1.ci_low:.2f} to {mU1.ci_high:.2f}", n_U1=mU1.n,
                      verdict_U1=res['U1'][0], robust_same_dir_U1=f"{res['U1'][1]} of {res['U1'][2]}",
                      verdict_U2=res['U2'][0], robust_same_dir_U2=f"{res['U2'][1]} of {res['U2'][2]}", final_verdict=final))
V = pd.DataFrame(V)
V.to_csv(R / 'outputs/verdicts.csv', index=False)
pd.set_option('display.width', 250)
print(V.to_string(index=False))

# ---- Unplanned (labelled): drop education to recover post-2010 cases ----
U = []
for h, cfg in HYP.items():
    base = T.copy()
    if h == 'H2':
        base = base[base.navco_unarmed_prodem_yrs.notna()]
    base = base.dropna(subset=['log_gdppc'])
    if h == 'H3':
        base = base.dropna(subset=['pre_locgov_10y', 'pre_cso_particip_10y'])
        base['z_locgov'] = (base.pre_locgov_10y - base.pre_locgov_10y.mean()) / base.pre_locgov_10y.std()
        base['z_csopart'] = (base.pre_cso_particip_10y - base.pre_cso_particip_10y.mean()) / base.pre_cso_particip_10y.std()
    base['educ'] = 0.0  # constant -> dropped
    est, n, k = cox(base, cfg['vars'])
    for v, (e, lo, hi, p) in est.items():
        U.append(dict(analysis='UNPLANNED: U1 Cox without education control', hypothesis=h, variable=v,
                      HR=e, ci_low=lo, ci_high=hi, p=p, n=n, events=k))
pd.DataFrame(U).to_csv(R / 'outputs/unplanned_estimates.csv', index=False)
print(pd.DataFrame(U).round(3).to_string(index=False))


# ---- Unplanned (labelled): Firth-penalised logit for R-b, because the pre-registered logit
#      is not estimable (perfect separation: every Western Europe & North America case survived) ----
def firth_logit(y, X, maxit=100, tol=1e-8):
    X = np.asarray(X, float); y = np.asarray(y, float); b = np.zeros(X.shape[1])
    for _ in range(maxit):
        p = 1 / (1 + np.exp(-X @ b)); W = p * (1 - p)
        XtWX = X.T @ (X * W[:, None]); inv = np.linalg.pinv(XtWX)
        h = np.einsum('ij,jk,ik->i', X * np.sqrt(W)[:, None], inv, X * np.sqrt(W)[:, None])
        U = X.T @ (y - p + h * (0.5 - p)); step = inv @ U
        b += step
        if np.max(np.abs(step)) < tol: break
    se = np.sqrt(np.diag(inv)); return b, se

F = []
for U in ['U1', 'U2']:
    for h, cfg in HYP.items():
        df = sample(U, h); df = df[df.survived_10y_num.notna()]
        X = sm.add_constant(drop_constant(design(df, cfg['vars'], 'era')))
        b, se = firth_logit(df.survived_10y_num, X)
        for v in cfg['vars']:
            if v in X.columns:
                k = list(X.columns).index(v)
                F.append(dict(analysis='UNPLANNED: Firth logit of survived_10y (R-b substitute)', universe=U, hypothesis=h,
                              variable=v, OR=np.exp(b[k]), ci_low=np.exp(b[k] - 1.96 * se[k]),
                              ci_high=np.exp(b[k] + 1.96 * se[k]), n=len(df)))
F = pd.DataFrame(F)
pd.concat([pd.read_csv(R / 'outputs/unplanned_estimates.csv'), F]).to_csv(R / 'outputs/unplanned_estimates.csv', index=False)
print(F.round(3).to_string(index=False))
