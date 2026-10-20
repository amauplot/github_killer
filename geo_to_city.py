#L'objectif est de transformer les données géographiques du document sur les hôpitaux en ville d'appartenance/département en s'aidant du document à ce sujet sur le site de Lino Galiana
#J'ai des problèmes sur le fait de bien sortir le fichier, vérifier?


import os
import requests
import pandas as pd
import numpy as np
import openpyxl
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from shapely.wkt import loads
from cartiflette import carti_download


def telecharger(url, chemin):
    """Télécharge url et l'enregistre dans chemin (sans retélécharger si le fichier existe)."""
    if os.path.exists(chemin):
        return
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    reponse = requests.get(url, timeout=60)
    reponse.raise_for_status()                 # erreur claire si le lien est mort
    with open(chemin, "wb") as f:
        f.write(reponse.content)

URL_APL = "https://www.data.gouv.fr/api/1/datasets/r/c41a1919-fbd7-4d19-a8df-1719bef8b14a"
telecharger(URL_APL, "data/raw/hospitals_point.csv")


# 1. Importation du fichier sur les hôpitaux en format csv (pour celà il est dans l'environnement Onyxia : faudra améliorer l'appel et faire comme dans l'autre fichier en appelant depuis l'URL et seulement en back-up depuis le local).

df = pd.read_csv("data/raw/hospitals_point.csv")

#df = pd.read_csv('hospitals_point.csv')


# 2. Conversion du tableau Pandas en GeoDataFrame
df['geometry'] = df['the_geom'].apply(loads)

#  On indique que le CSV est en Web Mercator (EPSG:3857)
gdf_points = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:3857")

# On le convertit ensuite en degrés (EPSG:4326) pour correspondre à Cartiflette
gdf_points = gdf_points.to_crs("EPSG:4326")


# 3. Téléchargement de la France entière 
communes_borders = carti_download(
    crs=4326,
    values="France", 
    borders="COMMUNE",
    vectorfile_format="geojson",
    filter_by="FRANCE_ENTIERE_DROM_RAPPROCHES",
    source="EXPRESS-COG-CARTO-TERRITOIRE",
    year=2022
)

# 4. La jointure spatiale
resultat = gpd.sjoin(gdf_points, communes_borders, how="left", predicate="within")

# Dictionnaire officiel de correspondance INSEE
dict_regions = {
    11: "Île-de-France", 24: "Centre-Val de Loire", 27: "Bourgogne-Franche-Comté",
    28: "Normandie", 32: "Hauts-de-France", 44: "Grand Est", 52: "Pays de la Loire",
    53: "Bretagne", 75: "Nouvelle-Aquitaine", 76: "Occitanie",
    84: "Auvergne-Rhône-Alpes", 93: "Provence-Alpes-Côte d'Azur", 94: "Corse"
}

# 5. Je remplace les codes région INSEE par leurs noms
resultat['NOM_REGIO'] = resultat['INSEE_REG'].fillna(0).astype(int).map(dict_regions)

resultat = resultat.rename(columns={'INSEE_COM': 'COM_INSEE'})

# 6.Affichage du résultat
print(resultat[['name', 'the_geom', 'NOM_REGIO', 'INSEE_DEP', 'COM_INSEE']])

#Le but sortir la base


resultat.to_csv('BASE_loc_hopitaux.csv', columns=['name', 'geometry', 'INSEE_DEP', 'COM_INSEE', 'NOM', 'STATUT', 'POPULATION', 'AREA','NOM_REGIO'], encoding='utf-8')

#resultat.to_csv('resultat_regions.csv', encoding='utf-8')





#Il faut encore nettoyer cette base (bcp de colonnes inutiles)
#Il faut aussi harmoniser les noms (REG, DEP etc) pour que ça tourne bien avec les autres fichiers
