

#L'objectif est de transformer les coordonnées géographiques relatives aux hôpitaux en villes d'appartenance, département d'appartenance et région d'appartenance.
#L'article de Lino Galiana Introduction aux données spatiales avec Geopandas a été utilisé comme point de référence


#1- Packages nécessaire pour l'importation des données depuis internet (os, requests), l'organisation des données (pandas, numpy, geopanda),
#leur visualisation (matplot, ctx qui ne sont pas utilisé à ce stade), le traitement des données géographiques (cartiflette, shapely)
import os
import requests
import pandas as pd
import numpy as np
import openpyxl #(il faut l'installer dans le terminal)
import geopandas as gpd
import contextily as ctx #(il faut l'installer dans le terminal)
import matplotlib.pyplot as plt
from shapely.wkt import loads
from cartiflette import carti_download #(il faut l'installer dans le terminal)

#2- Importation et visualisation des données

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

df = pd.read_csv("data/raw/hospitals_point.csv")

#On regarde les premières lignes
print(df.head(3))

#Pleins d'informations intéressantes, même si elles ne sont pas toujours renseignées. 
# Ex : appartenance au public et au privé. Si on affiche le pourcentage de Na : 
print("Pourcentage de NA public/privé :", df['operator-type'].isna().mean() * 100)
#L'information n'est pas renseignée pour prêt de 65% des hôpitaux

#Par contre d'autres informations sont systématiquement remplies, c'est le cas de la localisation, l'information qui nous intéresse : 
print("Pourcentage de NA localisation :", df['the_geom'].isna().mean() * 100)


# 3- Conversion du tableau Pandas en GeoDataFrame
df['geometry'] = df['the_geom'].apply(loads) #loads permet à python de transformer la chaîne de caractères en données interprétables

#  On indique que le CSV est en Web Mercator (EPSG:3857)
# Cela a été déterminé en comparant les coordonnées données d'hôpitaux dont on connaissait la géolocalisation et en trouvant la projection correspondante. L'usage de EPSG 3857 est fréquente pours les données WEB.
gdf_points = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:3857")

# On le convertit ensuite en EPSG:4326 pour correspondre à Cartiflette
gdf_points = gdf_points.to_crs("EPSG:4326")


# 4- Téléchargement de la France entière (via Cartiflette)
communes_borders = carti_download(
    crs=4326,
    values="France",
    borders="COMMUNE",
    vectorfile_format="geojson",
    filter_by="FRANCE_ENTIERE_DROM_RAPPROCHES",
    source="EXPRESS-COG-CARTO-TERRITOIRE",
    year=2022
)

# 5- La jointure spatiale
resultat = gpd.sjoin(gdf_points, communes_borders, how="left", predicate="within") #left : si on ne trouve pas la valeur pour un hôpital, on le garde avec NA

print(resultat.head(3))

# 6- Nettoyage du résultat
#A- Les régions : il est plus simple de passer par le code INSEE et de remettre les noms.
# Dictionnaire officiel de correspondance INSEE
dict_regions = {
    11: "Île-de-France", 24: "Centre-Val de Loire", 27: "Bourgogne-Franche-Comté",
    28: "Normandie", 32: "Hauts-de-France", 44: "Grand Est", 52: "Pays de la Loire",
    53: "Bretagne", 75: "Nouvelle-Aquitaine", 76: "Occitanie",
    84: "Auvergne-Rhône-Alpes", 93: "Provence-Alpes-Côte d'Azur", 94: "Corse"
}
# Je remplace les codes région INSEE par leurs noms
resultat['NOM_REGIO'] = resultat['INSEE_REG'].fillna(0).astype(int).map(dict_regions)

#B- Pour jointure futures avec d'autres bases, je renomme la colonne relative aux codes INSEE des communes
resultat = resultat.rename(columns={'INSEE_COM': 'COM_INSEE'})

# 7 - Affichage du résultat
print(resultat[['name', 'the_geom', 'NOM_REGIO', 'INSEE_DEP', 'COM_INSEE']])
print("Pourcentage de NA commune insee :", resultat['COM_INSEE'].isna().mean() * 100)
print("Nombre hôpitaux NA commune :", resultat['COM_INSEE'].isna().sum())
#Le code insee n'a pas été trouvé que pour 0,5% des hôpitaux, soit 14 hôpitaux sur 2506.


# 8- Mise en uniformité des résultats (gestion des NA), dans le cadre de la jointure
# A- Traitement de INSEE_DEP (remplace les NaN par une chaîne vide '', sinon formate sur 2 chiffres) => car les NA posait pbm
dep_numeric = pd.to_numeric(resultat['INSEE_DEP'], errors='coerce')
resultat['INSEE_DEP'] = dep_numeric.dropna().astype(int).astype(str).str.zfill(2)
resultat['INSEE_DEP'] = resultat['INSEE_DEP'].fillna('')

# B- Traitement de COM_INSEE (remplace les NaN par une chaîne vide '', sinon formate sur 5 chiffres)
com_numeric = pd.to_numeric(resultat['COM_INSEE'], errors='coerce')
resultat['COM_INSEE'] = com_numeric.dropna().astype(int).astype(str).str.zfill(5)
resultat['COM_INSEE'] = resultat['COM_INSEE'].fillna('')

#A voir si c'est nécessaire de le faire pour les régions (et sous quelle forme)

#9- Exportation du résultat en csv (il s'agit d'une version synthétique de la base, possible d'importer plus ou moins de colonnes)
resultat.to_csv('BASE_loc_hopitaux.csv', columns=['name', 'geometry', 'INSEE_DEP', 'COM_INSEE', 'NOM', 'STATUT', 'POPULATION', 'AREA','NOM_REGIO'], encoding='utf-8')




#10- nombre d'hôpitaux par régions

counts = resultat['NOM_REGIO'].value_counts()

#Calcul du pourcentage (normalize=True multiplié par 100)
percentages = resultat['NOM_REGIO'].value_counts(normalize=True) * 100

# Combinaison des deux dans un seul tableau propre
classement_regions = pd.DataFrame({
    'Nombre': counts,
    'Pourcentage (%)': percentages.round(2)
})

# Affichage du résultat
print(classement_regions)

#Ce tableau me fait poser la Q des dom tom mais je laisse ça à Malo qui s'occupe + de ça