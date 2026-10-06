#ficher pour convertir nos base de données en données exploitables
#conversion de la base de donnée FILOSOFI
import pandas as pd

#fonction générale pour convertir les données de la base FILOSOFI en tableau pandas exploitable
def conversion_filosofi_pandas(geo_object, filosofi_measure):
    #charger le fichier csv de la base FILOSOFI
    df = pd.read_csv('FILOSOFI_CC_csv/DS_FILOSOFI_CC_2023_data.csv', sep=';', encoding='latin-1', usecols=[0, 1, 2, 8])
    #filtrer les données pour ne garder que les observations de variables qui nous interessent

    df = df[df.iloc[:, 1] == geo_object]
    df = df[df.iloc[:, 2] == filosofi_measure]
    return df
# il suffit d'utiliser la fonction avec DEP et MED_SL pour avoir le tableau avec la médiane du niveau de vie pour les départements
