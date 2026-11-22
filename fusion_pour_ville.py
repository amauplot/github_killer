# à supprimer
#Obtention de la base fusion en filtrant les villes sans hôpitaux

import pandas as pd
from pathlib import Path
from conversion_data import conversion_filosofi_pandas

RACINE = Path(__file__).resolve().parent

df_commune_revenu_median = conversion_filosofi_pandas('COM', 'MED_SL')
df_commune_revenu_median.rename(columns={df_commune_revenu_median.columns[0]: 'COM_INSEE', df_commune_revenu_median.columns[3]: 'revenu_median'}, inplace=True)

apl_fin = pd.read_csv(RACINE / "data/processed/apl_fin.csv", dtype={"COM_INSEE": str})
hop = pd.read_csv(RACINE / "BASE_loc_hopitaux.csv", dtype={"COM_INSEE": str})

df = pd.merge(df_commune_revenu_median, apl_fin, on="COM_INSEE", how="left")
df = pd.merge(df, hop, on="COM_INSEE", how="left", suffixes=("", "_hop"))

print(len(df_commune_revenu_median), len(df))
print(df.head())

df = df = df.dropna(subset=['STATUT']) #il s'agit d'une des variable de la base sur les hôpitaux, en l'enlevant on n'a plus que les 2480 villes ayant au moins un établissements de santé

df.to_excel(RACINE / "data/processed/df_final_ville.xlsx", index=False)

