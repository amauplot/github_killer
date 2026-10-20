import pandas as pd
from pathlib import Path
from conversion_data import conversion_filosofi_pandas

RACINE = Path(__file__).resolve().parent

df_commune_revenu_median = conversion_filosofi_pandas('COM', 'MED_SL')

apl_fin = pd.read_csv(RACINE / "data/processed/apl_fin.csv", dtype={"COM_INSEE": str})
hop = pd.read_csv(RACINE / "BASE_loc_hopitaux.csv", dtype={"COM_INSEE": str})

df = pd.merge(df_commune_revenu_median, apl_fin, on="COM_INSEE", how="left")
df = pd.merge(df, hop, on="COM_INSEE", how="left", suffixes=("", "_hop"))

print(len(df_commune_revenu_median), len(df))
print(df.head())