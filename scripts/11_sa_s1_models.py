"""S1 tests exactly as frozen in docs/note9 §5.1. Outputs: outputs/sa_s1_estimates.csv, sa_s1_verdicts.csv,
sa_trends.csv, sa_r4_who_listens.csv, sa_s1_means.csv"""
import pathlib, numpy as np, pandas as pd, statsmodels.formula.api as smf
R = pathlib.Path(__file__).resolve().parents[1]
H = pd.read_csv(R / 'private/sa_ab_harmonised.csv')
S = H[H['round'].isin([4, 6, 7])].copy()
OUT = ['voice', 'practice', 'structure', 'mobilised_no_voice', 'convivial', 'listen_c', 'free', 'careful', 'fear', 'meet', 'raise_', 'memvol', 'memrel', 'contact_c']

def fit(df, y, single_round=False):
    d = df.dropna(subset=[y, 'traditional', 'age', 'educ', 'weight'])
    f = f'{y} ~ traditional + age + female + educ + C(province)' + ('' if single_round else ' + C(round)')
    m = smf.wls(f, d, weights=d.weight).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(d.cluster)[0]})
    ci = m.conf_int().loc['traditional']
    return dict(coef=m.params['traditional'], ci_low=ci[0], ci_high=ci[1], p=m.pvalues['traditional'], n=len(d),
                n_traditional=int(d.traditional.sum()))
rows = []
for y in OUT:
    rows.append(dict(outcome=y, model='main_pooled', **fit(S, y)))
    for r in [4, 6, 7]:
        rows.append(dict(outcome=y, model=f'Ra_round{r}', **fit(S[S['round'] == r], y, True)))
    rows.append(dict(outcome=y, model='Rb_rural_only', **fit(S[S.rural == 1], y)))
    rows.append(dict(outcome=y, model='Rc_homeland_provinces', **fit(S[S.homeland_province == 1], y)))
E = pd.DataFrame(rows); E.to_csv(R / 'outputs/sa_s1_estimates.csv', index=False)

def g(y, model): return E[(E.outcome == y) & (E.model == model)].iloc[0]
def rounds_sign(y, sign): return sum(1 for r in [4, 6, 7] if np.sign(g(y, f'Ra_round{r}').coef) == sign)
v = g('voice', 'main_pooled'); p_ = g('practice', 'main_pooled'); s_ = g('structure', 'main_pooled'); t = g('mobilised_no_voice', 'main_pooled')
voice = ('Supported' if v.ci_high < 0 and rounds_sign('voice', -1) >= 2 and g('voice', 'Rb_rural_only').coef < 0 and g('voice', 'Rc_homeland_provinces').coef < 0
         else 'Contradicted' if v.ci_low > 0 else 'Inconclusive')
struct = 'Contradicted' if (p_.ci_high < 0 or s_.ci_high < 0) else 'Supported'
typ = ('Supported' if t.ci_low > 0 and rounds_sign('mobilised_no_voice', 1) >= 2 else 'Contradicted' if t.ci_high < 0 else 'Inconclusive')
V = pd.DataFrame([
 dict(part='S1-voice', estimate=round(v.coef, 3), ci=f'{v.ci_low:.3f} to {v.ci_high:.3f}', rounds_in_predicted_direction=f"{rounds_sign('voice', -1)} of 3", verdict=voice),
 dict(part='S1-structure (practice)', estimate=round(p_.coef, 3), ci=f'{p_.ci_low:.3f} to {p_.ci_high:.3f}', rounds_in_predicted_direction='', verdict=struct),
 dict(part='S1-structure (structure)', estimate=round(s_.coef, 3), ci=f'{s_.ci_low:.3f} to {s_.ci_high:.3f}', rounds_in_predicted_direction='', verdict=struct),
 dict(part='S1-type (mobilised without voice)', estimate=round(t.coef, 3), ci=f'{t.ci_low:.3f} to {t.ci_high:.3f}', rounds_in_predicted_direction=f"{rounds_sign('mobilised_no_voice', 1)} of 3", verdict=typ),
 dict(part='S1 overall', estimate=np.nan, ci='', rounds_in_predicted_direction='', verdict='Supported' if (voice, struct, typ) == ('Supported',) * 3 else 'Not supported as a whole (see parts)')])
V.to_csv(R / 'outputs/sa_s1_verdicts.csv', index=False)
pd.set_option('display.width', 220); print(V.to_string(index=False)); print(E[E.model.isin(['main_pooled','Rb_rural_only','Rc_homeland_provinces'])].round(3).to_string(index=False))
print(E[E.outcome.isin(['voice','practice','structure','mobilised_no_voice'])&E.model.str.startswith('Ra')].round(3).to_string(index=False))

def wmean(d, cols): return pd.Series({c: np.average(d[c].dropna(), weights=d.loc[d[c].notna(), 'weight']) if d[c].notna().any() else np.nan for c in cols})
M = S.groupby(['round', 'traditional']).apply(lambda d: wmean(d, OUT)).round(3).reset_index(); M.to_csv(R / 'outputs/sa_s1_means.csv', index=False)
T = H.groupby(['year', 'rural']).apply(lambda d: wmean(d, ['practice', 'voice', 'meet', 'raise_', 'free', 'careful', 'listen_c', 'contact_c', 'contact_tl', 'request'])).round(3).reset_index()
T.to_csv(R / 'outputs/sa_trends.csv', index=False); print(T.to_string(index=False))
W = H[H['round'] == 4].groupby('traditional').apply(lambda d: wmean(d, ['listen_c', 'listen_tl'])).round(3).reset_index()
W.to_csv(R / 'outputs/sa_r4_who_listens.csv', index=False); print(W.to_string(index=False))
