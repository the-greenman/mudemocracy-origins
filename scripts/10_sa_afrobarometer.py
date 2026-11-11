"""South Africa study, S1 (docs/note9, §5.1): harmonise official Afrobarometer South Africa files.

The data files are NOT redistributed. Download them from afrobarometer.org/data and place them in
private/afrobarometer/ (excluded from git). File hashes are written to outputs/sa_input_hashes.csv.
Output: outputs/sa_ab_harmonised_summary.csv (no microdata), private/sa_ab_harmonised.csv, outputs/sa_ab_labels_audit.csv
"""
import pathlib, hashlib, re, glob
import numpy as np, pandas as pd, pyreadstat

R = pathlib.Path(__file__).resolve().parents[1]
P = R / 'private/afrobarometer'
MAP = {  # round: (file pattern, year, {item: variable})
 4: ('*saf_r4*', 2008, dict(free='Q15A', memrel='Q22A', memvol='Q22B', meet='Q23A', raise_='Q23B', contact_c='Q25A',
                             careful='Q46', fear='Q47', listen_c='Q54B', listen_tl='Q54C')),
 5: ('*saf_r5*', 2011, dict(free='Q17A', memrel='Q25A', memvol='Q25B', meet='Q26A', raise_='Q26B', contact_c='Q30A',
                             careful='Q56A', fear='Q54', listen_c='Q62B')),
 6: ('*saf_r6*', 2015, dict(free='Q15A', memrel='Q19A', memvol='Q19B', meet='Q20A', raise_='Q20B', contact_c='Q24A',
                             contact_tl='Q24E', careful='Q51A', fear='Q49', listen_c='Q59B', request='Q27A')),
 7: ('*SAF_R7*', 2018, dict(free='Q14', memrel='Q20A', memvol='Q20B', meet='Q21A', raise_='Q21B', contact_c='Q25A',
                             contact_tl='Q25E', careful='Q42A', fear='Q40', listen_c='Q54B', request='Q26A')),
 8: ('*saf_r8*', 2021, dict(free='Q10A', meet='Q11A', raise_='Q11B', contact_c='Q12A', contact_tl='Q12D',
                             careful='Q40D', listen_c='Q38B', listen_tl='Q38C')),
 9: ('*SAF_R9*', 2022, dict(free='Q9A', meet='Q10A', raise_='Q10B', contact_c='Q11B', contact_tl='Q11E',
                             careful='Q33D', listen_c='Q34B')),
}
# item -> (regex for labels coded 1, regex for labels coded 0); anything else is missing
RULE = dict(
 free=(r'somewhat free|completely free', r'not at all free|not very free'),
 memrel=(r'^active member|official leader', r'not a member|inactive member'),
 memvol=(r'^active member|official leader', r'not a member|inactive member'),
 meet=(r'^yes', r'^no'), raise_=(r'^yes', r'^no'), request=(r'^yes', r'^no'),
 contact_c=(r'only once|a few times|often', r'never'), contact_tl=(r'only once|a few times|often', r'never'),
 careful=(r'never|rarely', r'often|always'),
 fear=(r'not at all|a little bit', r'a lot|somewhat'),
 listen_c=(r'often|always', r'never|only sometimes|once sometimes'), listen_tl=(r'often|always', r'never|only sometimes|once sometimes'))
HOMELAND = re.compile(r'eastern cape|free state|kwazulu|limpopo|mpumalanga|north west', re.I)

frames, audit, hashes = [], [], []
for rnd, (pat, year, items) in MAP.items():
    f = glob.glob(str(P / pat))[0]
    hashes.append(dict(round=rnd, file=pathlib.Path(f).name, sha256=hashlib.sha256(open(f, 'rb').read()).hexdigest()))
    d, m = pyreadstat.read_sav(f)
    lab = dict(zip(m.column_names, m.column_labels)); vl = m.variable_value_labels
    o = pd.DataFrame({'round': rnd, 'year': year}, index=d.index)
    o['weight'] = d['withinwt'] if 'withinwt' in d else d['withinwt_ea']
    o['province'] = d.REGION.map(vl['REGION']).str.strip().str.title()
    o['rural'] = (d.URBRUR == 2).astype(int)
    if rnd == 4: o['traditional'] = (d.EA_GEOTYPE == 3).astype(int)
    elif rnd == 6: o['traditional'] = (d.URBRUR_SAF == 6).astype(int)
    elif rnd == 7: o['traditional'] = (d.EA_TYPE.str.strip() == 'TRADITIONAL RESIDENTIAL').astype(int)
    else: o['traditional'] = np.nan
    for item, var in items.items():
        one, zero = RULE[item]; codes = {}
        for code, text in vl[var].items():
            t = str(text).strip().lower()
            v = 1.0 if re.search(one, t) else (0.0 if re.search(zero, t) else np.nan)
            if re.search(r"don.t know|refused|missing|not asked|not applicable", t): v = np.nan
            codes[code] = v
            audit.append(dict(round=rnd, item=item, variable=var, question=lab[var], code=code, label=text, coded_as=v))
        o[item] = d[var].map(codes)
    def find(rx):
        c = [k for k, l in lab.items() if l and re.search(rx, str(l), re.I)]
        return c[0]
    a, e, g = find(r'^Q\d+[a-z]?\.? ?Age$|^Q1\. Age'), find(r'Education of respondent'), find(r"gender of respondent|respondent.s gender")
    o['age'] = d[a].where(d[a].between(18, 110)); o['educ'] = d[e].where(d[e].between(0, 9)); o['female'] = (d[g] == 2).astype(int)
    eac = sorted(c for c in d.columns if c.startswith('EA_') and d[c].dtype != object)
    o['cluster'] = f'r{rnd}_' + d.REGION.astype(str) + '_' + o.traditional.astype(str) + '_' + d.URBRUR.astype(str) + '_' + d[eac].astype(str).agg(''.join, axis=1)
    frames.append(o)
# Round 10 (2024): CSV with answer text. Question numbers checked against the round 10 questionnaire:
# Q10A free to say what you think; Q11A joined others to request action from government;
# Q12C contacted a traditional leader; Q36B local councillors listen. Community meetings, contacting a
# councillor and "careful what you say" were not asked in round 10.
f10 = glob.glob(str(P / '*SAF_R10*.csv'))
if f10:
    r = pd.read_csv(f10[0], low_memory=False)
    hashes.append(dict(round=10, file=pathlib.Path(f10[0]).name, sha256=hashlib.sha256(open(f10[0], 'rb').read()).hexdigest()))
    o = pd.DataFrame({'round': 10, 'year': 2024}, index=r.index)
    o['weight'] = r['withinwt_ea']; o['province'] = r.REGION.str.strip().str.title(); o['rural'] = (r.URBRUR == 'Rural').astype(int)
    o['traditional'] = np.nan; o['district'] = r['LOCATION.LEVEL.1'].str.strip().str.title()
    for item, var in dict(free='Q10A', request='Q11A', contact_tl='Q12C', listen_c='Q36B').items():
        one, zero = RULE[item]
        def code(t):
            t = str(t).strip().lower()
            if re.search(r"don.t know|refused|missing|nan", t): return np.nan
            return 1.0 if re.search(one, t) else (0.0 if re.search(zero, t) else np.nan)
        o[item] = r[var].map(code)
        for t in r[var].dropna().unique(): audit.append(dict(round=10, item=item, variable=var, question='(see round 10 questionnaire)', code='', label=t, coded_as=code(t)))
    frames.append(o)
H = pd.concat(frames, ignore_index=True)
H['homeland_province'] = H.province.str.contains(HOMELAND).astype(int)
H['practice'] = H[['meet', 'raise_']].mean(axis=1)
H['structure'] = H[['memvol', 'memrel', 'contact_c']].mean(axis=1)
H.loc[H['round'] > 7, 'structure'] = np.nan   # membership not asked after round 7
H['voice'] = H[['free', 'careful', 'fear']].mean(axis=1)
H.loc[H['round'] == 10, ['practice', 'voice']] = np.nan   # indices not constructible in round 10
H['mobilised_no_voice'] = ((H.practice > 0) & (H.voice <= 1/3)).astype(float).where(H.practice.notna() & H.voice.notna())
H['convivial'] = ((H.practice > 0) & (H.voice >= 2/3)).astype(float).where(H.practice.notna() & H.voice.notna())
H.to_csv(R / 'private/sa_ab_harmonised.csv', index=False)
pd.DataFrame(audit).to_csv(R / 'outputs/sa_ab_labels_audit.csv', index=False)
pd.DataFrame(hashes).to_csv(R / 'outputs/sa_input_hashes.csv', index=False)
print(H.groupby('round').agg(n=('weight', 'size'), trad=('traditional', 'sum'), clusters=('cluster', 'nunique'),
      age_na=('age', lambda s: s.isna().sum()), educ_na=('educ', lambda s: s.isna().sum())).to_string())
A = pd.DataFrame(audit); bad = A[A.coded_as.isna() & ~A.label.astype(str).str.contains(r"on.t know|Refused|Missing|Not asked|Not Applicable", case=False)]
print('labels left uncoded:\n', bad[['round', 'item', 'label']].drop_duplicates().to_string())
