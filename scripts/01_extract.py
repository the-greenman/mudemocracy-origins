"""Extract the variables used from the pinned raw sources into small CSVs."""
import pyreadr, pandas as pd, pathlib
R=pathlib.Path(__file__).resolve().parents[1]
(R/'data').mkdir(exist_ok=True); (R/'outputs').mkdir(exist_ok=True)
VARS=['country_name','country_text_id','COWcode','year','v2x_regime','v2x_polyarchy','v2regendtype','v2regidnr',
 'v2svdomaut_osp','v2svindep','v2cademmob_osp','v2regsupgroups_13','v2xcs_ccsi','v2csprtcpt_osp','v2xel_locelec',
 'v2dlengage_osp','v2x_partipdem','e_regiongeo','e_regionpol_6C','e_gdppc','e_peaveduc','e_total_resources_income_pc',
 'e_boix_regime','e_polity2',
 'v2xps_party','v2csantimv','v2xpe_exlsocgr','v2xnp_client','v2cacamps','v2elsnlsff']
v=list(pyreadr.read_r(R/'raw/vdemdata/data/vdem.RData').values())[0][VARS]
v.to_csv(R/'data/vdem_subset.csv.gz',index=False)
n=list(pyreadr.read_r(R/'raw/AuthoritarianismBook/data/navco_2.rda').values())[0]
n[['location','country_name','cown','year','id','campaign','prim_method','camp_goals']].to_csv(R/'data/navco2.csv',index=False)
print('vdem',v.shape,'navco',n.shape)
