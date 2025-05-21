# -*- coding: utf-8 -*-
"""
Created on Thu May 22 00:26:01 2025
@author: yohan


Entrée : "not_cleaned_df_loto_19-25.csv"
Description : On effectue un nettoyage complet du DataFrame "not_cleaned_df_loto_19-25.csv", 
              en supprimant les colonnes 'promotion_second_tirage' et 'Unnamed: 49' 
              tout en formattant et typant nos variables convenablement.
Sortie : "df_loto_19-25.csv"
"""

# Library
import numpy as np
import pandas as pd

# Chargement du Dataframe
df = pd.read_csv("not_cleaned_df_loto_19-25.csv", sep=";")

# Comprendréhension de la structure du Dataframe
# print("Dimensions :",df.shape)
# print(df.columns)                                                              # Noms de colonnes
# print(df.info())                                                               # Types de données et valeurs manquantes

# Identification des colonnes à supprimer ou nettoyer dans le Dataframe
colonnes_val_manquante = df.isnull().sum()
colonnes_val_manquante = colonnes_val_manquante[colonnes_val_manquante>0]
# print("Nombre de valeurs manquantes par colonne :\n", colonnes_val_manquante)

# Suppresion des colonnes superflues dans le Dataframe
colonnes_a_supprimer = ['date_de_forclusion','promotion_second_tirage','devise','Unnamed: 49']              # Liste des colonnes à supprimer
df = df.drop(columns=[col for col in colonnes_a_supprimer if col in df.columns])

# Nettoyage des colonnes non harmoniser

## Colonne 'jour_de_tirage'
df['jour_de_tirage'] = df['jour_de_tirage'].str.capitalize()

## Colonne 'date_de_tirage'
df['date_de_tirage'] = pd.to_datetime(df['date_de_tirage'], format="%d/%m/%Y")

## Colonne 'annee_numero_de_tirage'
df = df.drop(columns=['annee_numero_de_tirage'])

## Colonne 'jour_de_tirage'
df['jour_de_tirage'] = df['jour_de_tirage'].astype(str)

## Colonne 'rapport_du_rangX'
### Sélection de toutes les colonnes contenant "rapport_du_rangX" et "rapport_codes"
colonnes_rapport = [col for col in df.columns if col.startswith("rapport_du_rang") or col == "rapport_codes_gagnants"]

### Boucle de nettoyage pour chaque colonne
for col in colonnes_rapport:
    df[col] = df[col].astype(str).str.replace(' ', '', regex=False)
    df[col] = df[col].str.replace(',', '.', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')
    
## Colonne 'codes_gagnants'
df['codes_gagnants'] = df['codes_gagnants'].astype(str).str.replace(r'\s*,\s*', ',', regex=True)
df['codes_gagnants'] = df['codes_gagnants'].str.replace(',', ', ', regex=False)

## Colonne 'numero_jokerplus'
df['numero_jokerplus'] = df['numero_jokerplus'].astype(str).str.replace(' ', '', regex=False)
df['numero_jokerplus'] = df['numero_jokerplus'].replace('', np.nan)
df['numero_jokerplus'] = pd.to_numeric(df['numero_jokerplus'], errors='coerce')
df = df[df['numero_jokerplus'].notna()]
df['numero_jokerplus'] = df['numero_jokerplus'].astype(int)

## Nouvelle colonne
df['annee_de_tirage'] = df['date_de_tirage'].dt.year
df['mois_de_tirage'] = df['date_de_tirage'].dt.month
df['jour_de_la_semaine_de_tirage']=df['jour_de_tirage']
df['jour_de_tirage'] = df['date_de_tirage'].dt.day

## Réorganisation des colonnes
colonnes = df.columns.tolist()

colonnes.remove('date_de_tirage')
colonnes.remove('jour_de_la_semaine_de_tirage')
colonnes.remove('jour_de_tirage')
colonnes.remove('mois_de_tirage')
colonnes.remove('annee_de_tirage')

colonnes.insert(0, 'date_de_tirage')
colonnes.insert(1, 'jour_de_la_semaine_de_tirage')
colonnes.insert(2, 'jour_de_tirage')
colonnes.insert(3, 'mois_de_tirage')
colonnes.insert(4, 'annee_de_tirage')

df = df[colonnes]

# Nouveau Dataframe nettoyé
df.to_csv("df_loto_19-25.csv", index=False, sep=';')