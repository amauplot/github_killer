
#L'objectif de ce fichier est de produire une carte de France sur laquelle les communes contenant au moins un hôpital sont en rouge.
#Cette première visualisation est purement indicative (elle ne tient pas compte de la densité de population, des axes de transports, etc)

#Limites
#Les DOM TOM : Absents de la base de données initiales
#IDEE : déformer la limites des villes (agrandir) pour que le revenu médian se voit de plus loin OU conditionner aussi la couleur du point)
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
    simplification=50,
    crs=4326
)

print("Téléchargement du contour France...")
gdf_france = carti_download(
    values="France",
    borders="REGION",
    filter_by="FRANCE_ENTIERE_DROM_RAPPROCHES",
    simplification=50,
    crs=4326
)


# On retire les communes des DROM (codes INSEE commençant par 97) car la base de données utilisées ne les mobilisent pas
#On pourrait ne pas prendre FRANCE_ENTIERE_DROM_RAPPROCHES mais alors on n'aurait pas l'Île-de-France mise en valeur d'où ce choix
gdf_communes = gdf_communes[~gdf_communes["INSEE_COM"].str.startswith("97")].copy()

# On retire les contours des régions d'outre-mer (codes 01, 02, 03, 04, 06)
regions_drom = ["01", "02", "03", "04", "06"]
gdf_france = gdf_france[~gdf_france["INSEE_REG"].isin(regions_drom)].copy()


# 3- Préparation, sachant que pour la Corse dans ma base je ne peux pas passer par le code Insee, donc je retiens les cas où la région est la Corse

# A. Cas général (hors Corse) : correspondance directe par code INSEE
condition_insee = gdf_communes["INSEE_COM"].isin(hop["COM_INSEE"])

# B. Cas de la Corse : repérage des communes contenant un point GPS d'hôpital
hop_corse = hop[hop["NOM_REGIO"] == "Corse"].copy()

if not hop_corse.empty:
    # Conversion du texte WKT en géométrie GeoPandas (CRS 4326)
    hop_corse["geometry"] = hop_corse["geometry"].apply(loads)
    gdf_hop_corse = gpd.GeoDataFrame(hop_corse, geometry="geometry", crs=4326)

    # On filtre Cartiflette sur la Corse via les codes INSEE commençant par 2A ou 2B
    gdf_communes_corse = gdf_communes[gdf_communes["INSEE_COM"].str.startswith(("2A", "2B"))]

    # Jointure spatiale : trouve dans quelle commune tombe chaque hôpital corse
    communes_corse_avec_hop = gpd.sjoin(
        gdf_communes_corse, 
        gdf_hop_corse, 
        how="inner", 
        predicate="contains"
    )
    
    # Liste des vrais codes INSEE (2A... / 2B...) des communes corses ayant un hôpital
    codes_insee_corse_hop = communes_corse_avec_hop["INSEE_COM"].unique()
    condition_corse = gdf_communes["INSEE_COM"].isin(codes_insee_corse_hop)
else:
    condition_corse = pd.Series(False, index=gdf_communes.index)

# C. Sélection finale : uniquement les communes qui ont un hôpital (Corse incluse)
gdf_selection = gdf_communes[condition_corse | condition_insee].copy()

# Fusion des géométries uniquement pour tracer le contour extérieur global
union_communes = unary_union(gdf_selection.geometry)
gdf_selection_fusionnee = gpd.GeoDataFrame(geometry=[union_communes], crs=gdf_communes.crs)



# 4- Préparation du fond de carte

m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles=None) #centre la carte sur la france, zoom initial et fond vide

# 5- Carte en blanc, ville en rouge

# Je voudrais que sur la carte les villes aient une couleur liée au revenu médian donné par la base suivante :
df_final = pd.read_excel(RACINE / "data/processed/df_final.xlsx", dtype={"COM_INSEE": str})

import branca.colormap as cm

# Nettoyage au cas où il y aurait des valeurs manquantes dans la colonne revenu
df_revenus_valides = df_final.dropna(subset=["COM_INSEE", "revenu_median"])

# Création du dictionnaire {code_insee: revenu_median}
dict_revenus = df_revenus_valides.set_index("COM_INSEE")["revenu_median"].to_dict()


# On borne l'échelle entre le 10e et le 90e centile pour éviter que les extrêmes n'écrasent les couleurs 
revenu_min = df_revenus_valides["revenu_median"].quantile(0.10)
revenu_max = df_revenus_valides["revenu_median"].quantile(0.90)

colormap = cm.LinearColormap(
    colors=["blue", "white", "red"], 
    vmin=revenu_min,
    vmax=revenu_max,
    caption="Revenu médian par ville (€) - échelle 10e-90e centiles"
)




# Fonctions de style
def style_france_blanc(feature):
    return {"fillColor": "#FFFFFF", "fillOpacity": 1.0, "color": "#D3D3D3", "weight": 1}

def style_commune_revenu(feature):
    # Cartiflette stocke le code commune sous "INSEE_COM"
    code_insee = feature["properties"].get("INSEE_COM")
    revenu = dict_revenus.get(code_insee)

    if revenu is not None and pd.notna(revenu):
        couleur = colormap(revenu)
        opacite = 0.75
    else:
        # Couleur gris si la commune n'a pas de revenu renseigné (ex: certaines communes corses) => rendre ça plus clair
        couleur = "#E0E0E0"
        opacite = 1

    return {
        "fillColor": couleur,
        "fillOpacity": opacite,
        "color": couleur, # Même couleur que le fond pour éviter les traits entre villes voisines
        "weight": 0.5
    }

def style_contour_exterieur(feature):
    return {"fill": False, "color": "#333333", "weight": 1.5}


# 6- Ajout des couches sur la carte
# Fond France
folium.GeoJson(gdf_france, style_function=style_france_blanc, name="Fond France").add_to(m)

# Couche des villes colorées individuellement selon le revenu médian
folium.GeoJson(
    gdf_selection, 
    style_function=style_commune_revenu, 
    name="Revenu médian des communes"
).add_to(m)

# Contour global autour des zones fusionnées
folium.GeoJson(
    gdf_selection_fusionnee, 
    style_function=style_contour_exterieur, 
    name="Contours des zones"
).add_to(m)

# Ajout de la légende des couleurs sur la carte
colormap.add_to(m)




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
m.save(RACINE / "data/processed/carte_france_villes_hop.html")
print("Fait ! La carte a été générée avec succès.")