#L'objectif est de transformer les données géographiques du document sur les hôpitaux en ville d'appartenance/département en s'aidant du document à ce sujet sur le site de Lino Galiana
#Le code a l'air de fonctionner : il faudrait repasser dessus pour le nettoyer et être sûrs qu'il ne comporte pas d'erreur.

import pandas as pd
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
from shapely.wkt import loads
from cartiflette import carti_download

# 1. Importation du fichier sur les hôpitaux en format csv (pour celà il est dans l'environnement Onyxia).
df = pd.read_csv('hospitals_point.csv')


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

# 6.Affichage du résultat
print(resultat[['name', 'the_geom', 'NOM_REGIO', 'INSEE_DEP', 'INSEE_COM']])
