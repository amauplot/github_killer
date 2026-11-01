from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import geopandas as gpd
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
df["nb_hopitaux"] = df["nb_hopitaux"].fillna(0).astype(int)
df["revenu_median"] = df["revenu_median"].fillna(0).astype(int)
df["nb_hopitaux_par_habitant"] = df["nb_hopitaux"] / df["pop_tot"]

print(len(df_departement_revenu_median), len(df))
print(df.head())


# Réinitialisation de l'index pour faciliter l'exploitation graphique
df_reset = df.reset_index()


#-----GRAPHIQUES-------

sns.set_theme(style="whitegrid")

# 1. Revenu médian (X) vs Nb d'hôpitaux par habitant (Y)
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_reset, x="revenu_median", y="nb_hopitaux_par_habitant", alpha=0.7
)
plt.title(
    "Relation entre le revenu médian et le nombre d'hôpitaux par habitant par département"
)
plt.xlabel("Revenu médian (€)")
plt.ylabel("Nombre d'hôpitaux par habitant")
plt.tight_layout()
plt.savefig(RACINE / "graph_revenu_vs_hopitaux.png", dpi=300)
plt.show()

# 2. Revenu médian (X) vs APL (Y)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_reset, x="revenu_median", y="apl", alpha=0.7, color="orange")
plt.title("Relation entre le revenu médian et l'APL moyenne par département")
plt.xlabel("Revenu médian (€)")
plt.ylabel("APL moyenne")
plt.tight_layout()
plt.savefig(RACINE / "graph_revenu_vs_apl.png", dpi=300)
plt.show()


# CARTES DE FRANCE 
# Chargement du GeoJSON officiel des départements français
geojson_url = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson"
gdf_deps = gpd.read_file(geojson_url)
gdf_deps["code"] = gdf_deps["code"].astype(str).str.strip()

# Fusion des données géographiques avec vos données
gdf_merged = gdf_deps.merge(df_reset, left_on="code", right_on="DEP", how="left")

# Nombre d'hôpitaux par habitant
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf_merged.plot(
    column="nb_hopitaux_par_habitant",
    ax=ax,
    legend=True,
    cmap="Blues",
    legend_kwds={
        "label": "Nombre d'hôpitaux par habitant",
        "orientation": "horizontal",
    },
    missing_kwds={"color": "lightgrey", "label": "Données manquantes"},
)
ax.set_title(
    "Carte de France du nb d'hôpitaux par habitants dans chaque départements",
    fontsize=14,
)
ax.axis("off")
plt.tight_layout()
plt.savefig(RACINE / "carte_nb_hopitaux_par_habitant.png", dpi=300)
plt.show()

# APL
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf_merged.plot(
    column="apl",
    ax=ax,
    legend=True,
    cmap="Oranges",
    legend_kwds={"label": "APL moyenne", "orientation": "horizontal"},
    missing_kwds={"color": "lightgrey", "label": "Données manquantes"},
)
ax.set_title("Carte de France de l'APL dans chaque département", fontsize=14)
ax.axis("off")
plt.tight_layout()
plt.savefig(RACINE / "carte_apl.png", dpi=300)
plt.show()

# Revenu médian
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gdf_merged.plot(
    column="revenu_median",
    ax=ax,
    legend=True,
    cmap="Greens",
    legend_kwds={"label": "Revenu médian (€)", "orientation": "horizontal"},
    missing_kwds={"color": "lightgrey", "label": "Données manquantes"},
)
ax.set_title("Carte de France du revenu médian dans chaque département", fontsize=14)
ax.axis("off")
plt.tight_layout()
plt.savefig(RACINE / "carte_revenu_median.png", dpi=300)
plt.show()
