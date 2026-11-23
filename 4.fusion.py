import pandas as pd
from pathlib import Path
from conversion_data import conversion_filosofi_pandas

# étant donné que les données ne sont pas toutes au même endroit, on redefinit la racine
RACINE = Path(__file__).resolve().parent

# appel de la fonction conversion en vue de l'obtention de la base contenant les revenus médians
df_commune_revenu_median = conversion_filosofi_pandas('COM', 'MED_SL')
df_commune_revenu_median.rename(columns={df_commune_revenu_median.columns[0]: 'COM_INSEE', df_commune_revenu_median.columns[3]: 'revenu_median'}, inplace=True)

# appel des bases des apl et des hopitaux
apl_fin = pd.read_csv(RACINE / "data/processed/apl_fin.csv", dtype={"COM_INSEE": str})
hop = pd.read_csv(RACINE / "data/processed/BASE_loc_hopitaux.csv", dtype={"COM_INSEE": str})

# -----------------------------------------------------------------------------------------------------------
# on agrège l'APL pour Paris, Lyon et Marseille
# Paris, Lyon et Marseille : l'APL est donnée par arrondissement,
# on recalcule une valeur pour la ville entière

villes = {"75056": ("751", "Paris"),
          "69123": ("6938", "Lyon"),
          "13055": ("132", "Marseille")}

colonnes_apl = ["apl", "apl65", "apl62", "apl60"]

# on s'assure que ces colonnes sont bien des nombres
for col in colonnes_apl + ["pop_std", "pop_tot"]:
    apl_fin[col] = pd.to_numeric(apl_fin[col], errors="coerce")

nouvelles_lignes = []

for code_ville, (debut, nom) in villes.items():
    # les arrondissements de cette ville
    arrondissements = apl_fin[apl_fin["COM_INSEE"].str.startswith(debut)]

    ligne = {"COM_INSEE": code_ville, "commune": nom}

    # populations : somme
    ligne["pop_std"] = arrondissements["pop_std"].sum()
    ligne["pop_tot"] = arrondissements["pop_tot"].sum()

    # chaque APL : moyenne pondérée par la population
    for col in colonnes_apl:
        ligne[col] = (arrondissements[col] * arrondissements["pop_std"]).sum() / ligne["pop_std"]

    # département, région, arrondissement départemental : identiques pour
    # tous les arrondissements de la ville, on prend ceux du premier
    ligne["DEP"] = arrondissements["DEP"].iloc[0]
    ligne["REG"] = arrondissements["REG"].iloc[0]
    ligne["ARR"] = arrondissements["ARR"].iloc[0]

    nouvelles_lignes.append(ligne)
    print(nom, ":", len(arrondissements), "arrondissements")

# on ajoute les 3 villes à la base des APL
apl_fin = pd.concat([apl_fin, pd.DataFrame(nouvelles_lignes)], ignore_index=True)
#--------------------------------------------------------------------------------------------------------

# Une ligne par commune pour les hôpitaux : on les compte
hop_agg = hop.groupby("COM_INSEE").size().reset_index(name="nb_hopitaux")

# fusion de la base des revenus avec celle des APL
df = pd.merge(df_commune_revenu_median, apl_fin, on="COM_INSEE", how="left")

# fusion de la base obtenue avec celle des hopitaux agrégés par commune
df = pd.merge(df, hop_agg, on="COM_INSEE", how="left", suffixes=("", "_hop"))

# remplacement des NAN par 0 pour ce qui concerne le nbre d'hôpitaux
df["nb_hopitaux"] = df["nb_hopitaux"].fillna(0).astype(int)

# Contrôles
print("Doublons COM_INSEE :", df["COM_INSEE"].duplicated().sum())
print("Communes sans APL :", df["apl"].isna().sum())
print("Revenus manquants :", df["revenu_median"].isna().sum())
print("Communes avec au moins un hôpital :", (df["nb_hopitaux"] > 0).sum())

# enrégistrement de la base dans data
df.to_excel(RACINE / "data/processed/df_final.xlsx", index=False)
