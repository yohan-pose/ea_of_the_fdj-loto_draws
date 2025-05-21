# -*- coding: utf-8 -*-
"""
Created on Thu May 22 00:26:01 2025
@author: yohan


Entrée : "df_loto_19-25.csv"
Description : On effectue une analyse exploratroire de "df_loto_19-25.csv"
Sortie : 
"""

# Library
import matplotlib.pyplot as plt
import pandas as pd

# Chargement du DF
df = pd.read_csv("df_loto_19-25.csv", sep=";")

# ReClassification des types des colonnes datetime du DF
# print(df.dtypes)
df['date_de_tirage'] = pd.to_datetime(df['date_de_tirage'], format="%Y-%m-%d")
df['date_de_forclusion'] = pd.to_datetime(df['date_de_forclusion'], format="%Y-%m-%d")

# Liste des colonnes à exclure de l'analyse numérique
col_not_num_a_exclure = [
    'date_de_tirage',
    'date_de_forclusion',
    'jour_de_la_semaine_de_tirage',
    'jour_de_tirage',
    'mois_de_tirage',
    'annee_de_tirage',
    'combinaison_gagnante_en_ordre_croissant',
    'codes_gagnants',
    'combinaison_gagnant_second_tirage_en_ordre_croissant',
    'numero_jokerplus',
    'devise'
]

col_num = df.select_dtypes(include='number').columns
col_utils = [col for col in col_num if col not in col_not_num_a_exclure]
eda_df=df[col_utils].describe()

# Rassembler tous les numéros tirés dans une seule série
boules = pd.concat([df[f'boule_{i}'] for i in range(1, 6)])

# Compter la fréquence de chaque numéro
frequence_boules = boules.value_counts().sort_index()
frequence_chance = df['numero_chance'].value_counts().sort_index()

## Créer une couleur pour chaque barre (rouge si >100, sinon bleu)
couleurs_freq_boules = ['#838eff' if count > 100 else '#83bcff' for count in frequence_boules]

## Tracé du graphique
plt.figure(figsize=(12, 5))
frequence_boules.plot(kind='bar', color=couleurs_freq_boules)
plt.title("Fréquence des boules tirées (mise en évidence si > 100)")
plt.xlabel("Numéro de boule")
plt.ylabel("Nombre d'apparitions")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Répartition des cagnottes par jour, mois ou annee
gains_par_jour = df.groupby('jour_de_tirage')['rapport_du_rang1'].mean().sort_index()

## Tracé du graphique
plt.figure(figsize=(8, 4))
gains_par_jour.plot(kind='bar',color="#83bcff")
plt.title("Cagnotte moyenne du Rang 1 par jour de tirage")
plt.xlabel("Jour")
plt.ylabel("Cagnotte moyenne (€)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Présence ou absence de gagnants au rang 1
df['gagnant_rang1'] = df['nombre_de_gagnant_au_rang1'] > 0
winner_or_not = df['gagnant_rang1'].value_counts()



