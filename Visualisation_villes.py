
#L'objectif de ce fichier est de produire une carte de France sur laquelle les communes contenant au moins un hôpital sont en rouge.
#Cette première visualisation est purement indicative (elle ne tient pas compte de la densité de population, des axes de transports, etc)

#PBMS persistants
#Les DOM TOM : je n'ai pas réussi à les mettre, revenir au tableau initial pour voir si la donnée n'était pas là où si elle s'est perdue
#Frontières des villes corses 

#0- Téléchargement des packages nécessaires
import folium # à installer (permet la création d'une carte interactive)
import geopandas as gpd
import pandas as pd
from pathlib import Path #(pour importer le fichier)
from shapely.ops import unary_union #permet de fusionner les géométries qui se superposent : dans notre cas si deux villes voisines sont concernées, cela permet de ne pas avoir d'espace entre elles/de pleur donner la même frontière
from shapely.wkt import loads #utile pour conversion de données géographiques, faut que je creuse un peu
from cartiflette import carti_download #toujours cartiflette pour les donénes françaises


#1 - Téléchargement des données
RACINE = Path(__file__).resolve().parent
hop = pd.read_csv(RACINE / "BASE_loc_hopitaux.csv", dtype={"COM_INSEE": str})

# 2. Chargement des fonds de carte via CARTIFLETTE
# Contours de toutes les communes de France
print("Téléchargement des communes...")
gdf_communes = carti_download(
    values="France",
    borders="COMMUNE",
    filter_by="FRANCE_ENTIERE_DROM_RAPPROCHES",
    simplification=50, # Allège le produit fini qu'on aura sur Folium
    crs=4326           # Coordonnées standard 
)
# Silhouette nationale 
print("Téléchargement du contour France...")
gdf_france = carti_download(
    values="France",
    borders="REGION", #on prend par région pour avoir leur frontières après sur la carte
    filter_by="FRANCE_ENTIERE_DROM_RAPPROCHES",
    simplification=50,
    crs=4326
)


# 3- Préparation, sachant que pour la Corse dans ma base je ne peux pas passer par le code Insee, donc je retiens les cas où la région est la Corse

gdf_communes["REGION_CLE"] = gdf_communes.get("NOM_REGIO")

condition_corse = gdf_communes["REGION_CLE"] == "Corse" #renvoie TRUE si la ville est en Corse => je les repère pour proposer une gestion meilleure après
condition_insee = gdf_communes["INSEE_COM"].isin(hop["COM_INSEE"]) #on compare les données issues de cartiflette à ma base. Pour chaque commune de cartiflette qui est aussi présente dans ma base hôpital elle renvoie TRUE

gdf_selection = gdf_communes[condition_corse | condition_insee] #j'ai un tableau avec toutes les villes en corse OU qui ont un hôpital, ie celles sur lesquelles je vais travailler après
#PROBLEME : du coup les villes corse après j'ai pas leur frontière, à voir
union_communes = unary_union(gdf_selection.geometry) #si plusieurs
gdf_selection_fusionnee = gpd.GeoDataFrame(geometry=[union_communes], crs=gdf_communes.crs)


# 4- Préparation du fond de carte

m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles=None) #centre la carte sur la france, zoom initial et fond vide

# 5- Carte en blanc, ville en rouge
def style_france_blanc(feature):
    return {"fillColor": "#FFFFFF", "fillOpacity": 1.0, "color": "#D3D3D3", "weight": 1}

def style_commune_rouge(feature):
    return {"fillColor": "#FF0000", "fillOpacity": 0.4, "color": "#FF0000", "weight": 2}

# 6- Ajout des couches préparées (une fond france et une venant des données fusionnées)
folium.GeoJson(gdf_france, style_function=style_france_blanc, name="Fond France").add_to(m)
folium.GeoJson(gdf_selection_fusionnee, style_function=style_commune_rouge, name="Zones Hôpitaux").add_to(m)


# 7- Ajout du marqueur des villes avec des hôpitaux

dict_noms = pd.Series(gdf_communes.NOM.values, index=gdf_communes.INSEE_COM).to_dict()

for index, row in hop.iterrows(): #parcoure hop, ligne par ligne
    est_corse = False
    if "NOM_REGIO" in row and row["NOM_REGIO"] == "Corse":
        est_corse = True

    if est_corse:
    # 1. On transforme le texte WKT en vraie géométrie Shapely
        wkt_geometry = row["geometry"]
        point_geom = loads(wkt_geometry)
    
    # 2. On extrait directement X et Y de cet objet géométrique
        lat = point_geom.y
        lon = point_geom.x
    
        nom_affichage = row.get("nom", row.get("NOM", "Hôpital (Corse)"))


    else:
        code_insee = row["COM_INSEE"]
        commune_geo = gdf_communes[gdf_communes["INSEE_COM"] == code_insee]
        
        if not commune_geo.empty:
            centroid = commune_geo.geometry.iloc[0].centroid
            lat, lon = centroid.y, centroid.x
            nom_affichage = dict_noms.get(code_insee, "Commune hôpital")
        else:
            continue

#dessin du marqueur sur la carte
    folium.CircleMarker(
        location=[lat, lon],
        radius=4,
        color="darkred",
        fill=True,
        fill_color="black",
        fill_opacity=1,
        popup=nom_affichage,
    ).add_to(m)


# 8. Sauvegarde de la carte
m.save("carte_france_blanche_rouge.html")
print("Fait ! La carte a été générée avec succès.")

# Il faut télécharger le fochier html et en l'ouvrant on arrive sur une page web où on peut naviguer sur cette carte. 
# Le problème est que les DOM TOM sont vides (voir si ça vient de la base ou de son traitement) et que la Corse est pas remplie comme je voudrai