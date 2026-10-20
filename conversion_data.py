# Conversion de la base de données FILOSOFI
import os
import zipfile
import requests
import pandas as pd

def telecharger_et_extraire(url, chemin_zip, dossier_destination):
    """Télécharge une archive ZIP si elle n'existe pas et l'extrait."""
    if not os.path.exists(dossier_destination):
        os.makedirs(dossier_destination, exist_ok=True)
        print(f"Téléchargement de {url}...")
        reponse = requests.get(url, timeout=120)
        reponse.raise_for_status()
        
        with open(chemin_zip, "wb") as f:
            f.write(reponse.content)
        print(f"Téléchargement réussi : {chemin_zip}")
        
        print(f"Extraction de l'archive dans {dossier_destination}...")
        with zipfile.ZipFile(chemin_zip, 'r') as zip_ref:
            zip_ref.extractall(dossier_destination)
        print("Extraction terminée.")
    else:
        print(f"Le dossier de destination existe déjà : {dossier_destination}")

# Définition des chemins et de l'URL
URL_FILOSOFI = "https://www.insee.fr/fr/statistiques/fichier/8984752/FILOSOFI_CC_csv.zip"
chemin_zip = "FILOSOFI_CC_csv.zip"
dossier_extraction = "FILOSOFI_CC_csv"
chemin_csv = os.path.join(dossier_extraction, "DS_FILOSOFI_CC_2023_data.csv")

# 1. Téléchargement et décompression automatique de l'archive
telecharger_et_extraire(URL_FILOSOFI, chemin_zip, dossier_extraction)


# 2. Fonction générale pour convertir les données de la base FILOSOFI en tableau pandas exploitable
def conversion_filosofi_pandas(geo_object, filosofi_measure):
    # Charger le fichier csv de la base FILOSOFI en sélectionnant les colonnes utiles
    df = pd.read_csv(chemin_csv, sep=';', encoding='latin-1', usecols=[0, 1, 2, 8])
    
    # Filtrer les données pour ne garder que les observations correspondantes
    df = df[df.iloc[:, 1] == geo_object]
    df = df[df.iloc[:, 2] == filosofi_measure]
    
    # Renommer la 1ère colonne en COM_INSEE
    premiere_colonne = df.columns[0]
    df = df.rename(columns={premiere_colonne: 'COM_INSEE'})
    
    return df


# 3. Appel de la fonction avec 'COM' et 'MED_SL'
df_commune_revenu_median = conversion_filosofi_pandas('COM', 'MED_SL')

# Affichage des premières lignes du résultat
print(df_commune_revenu_median.head())