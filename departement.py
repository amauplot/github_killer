from pathlib import Path
import pandas as pd
from conversion_data import conversion_filosofi_pandas

RACINE = Path(__file__).resolve().parent

# revenu_par_departement
df_departement_revenu_median = conversion_filosofi_pandas("DEP", "MED_SL")
df_departement_revenu_median.rename(columns={
        df_departement_revenu_median.columns[0]: "DEP",
        df_departement_revenu_median.columns[3]: "revenu_median",
    },
    inplace=True,
)
# verification que DEP est bien au format string
df_departement_revenu_median["DEP"] = (df_departement_revenu_median["DEP"].astype(str).str.strip())

# telechargement du fichier apl_fin.csv et selection des colonnes d'interet
apl_fin = pd.read_csv(RACINE / "data/processed/apl_fin.csv", dtype={"COM_INSEE": str, "DEP": str})
apl_fin = apl_fin[["COM_INSEE", "apl", "pop_tot", "DEP"]]
apl_fin["APL*habitant"] = apl_fin["apl"] * apl_fin["pop_tot"]

# aggregation par departement 
apl_par_departement = (apl_fin.groupby("DEP").agg({"APL*habitant": "sum", "pop_tot": "sum"}).reset_index())
apl_par_departement["apl"] = (apl_par_departement["APL*habitant"] / apl_par_departement["pop_tot"])
apl_par_departement["DEP"] = ( apl_par_departement["DEP"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip())

# donnees sur les hopitaux par departement
df_hopitaux = pd.read_csv(RACINE / "BASE_loc_hopitaux.csv", dtype={"COM_INSEE": str, "INSEE_DEP": str})
df_hopitaux = df_hopitaux[["name", "INSEE_DEP"]]
hopitaux_par_departement = (df_hopitaux.groupby("INSEE_DEP").agg({"name": "count"}).reset_index().rename(columns={"name": "nb_hopitaux"}))
hopitaux_par_departement["INSEE_DEP"] = (hopitaux_par_departement["INSEE_DEP"].astype(str).str.replace(r"\.0$", "", regex=True).str.strip())

# 4. Merging datasets (using apl_par_departement instead of apl_fin)
df = pd.merge(df_departement_revenu_median, apl_par_departement, on="DEP", how="left")
df = pd.merge(df, hopitaux_par_departement, left_on="DEP", right_on="INSEE_DEP", how="left")

df.set_index("DEP", inplace=True)
df = df[["revenu_median", "pop_tot", "apl", "nb_hopitaux"]]

print(len(df_departement_revenu_median), len(df))
print(df.head())

