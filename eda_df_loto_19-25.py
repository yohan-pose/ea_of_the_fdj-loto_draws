# -*- coding: utf-8 -*-
"""
Created on Thu May 22 00:26:01 2025
@author: yohan


Entrée : "df_loto_19-25.csv"
Description : On effectue une analyse exploratroire de "df_loto_19-25.csv"
Sortie : 
"""

# Library
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression


# Chargement du DF
df = pd.read_csv("df_loto_19-25.csv", sep=";")

# ReClassification des types des colonnes datetime du DF
# print(df.dtypes)
df['date_de_tirage'] = pd.to_datetime(df['date_de_tirage'], format="%Y-%m-%d")

# Liste des colonnes à exclure de l'analyse numérique
col_not_num_a_exclure = [
    'date_de_tirage',
    'jour_de_la_semaine_de_tirage',
    'jour_de_tirage',
    'mois_de_tirage',
    'annee_de_tirage',
    'combinaison_gagnante_en_ordre_croissant',
    'codes_gagnants',
    'combinaison_gagnant_second_tirage_en_ordre_croissant',
    'numero_jokerplus',
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
couleurs_freq_chance = ['#838eff' if count > 100 else '#83bcff' for count in frequence_chance]

## Tracé du graphique
plt.figure(figsize=(12, 5))
frequence_boules.plot(kind='bar', color=couleurs_freq_boules)
plt.title("Fréquence des numéros tirées")
plt.xlabel("Numéro")
plt.ylabel("Nombre d'apparitions")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

## Tracé du graphique
plt.figure(figsize=(12, 5))
frequence_chance.plot(kind='bar', color=couleurs_freq_chance)
plt.title("Fréquence des numéros chances tirées")
plt.xlabel("Numéro chance")
plt.ylabel("Nombre d'apparitions")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

colonnes_rangs = [f'rapport_du_rang{i}' for i in range(1, 10)]

# Transformation log10 (on ajoute 1 pour éviter log(0))
df_log = df[colonnes_rangs].applymap(lambda x: np.log10(x + 1) if pd.notnull(x) else np.nan)

# Boxplot sur données log-transformées
plt.figure(figsize=(12, 6))
df_log.boxplot(showfliers=True)
plt.title("Distribution des gains par rang (échelle logarithmique)")
plt.xlabel("Rang")
plt.ylabel("log(Gain en euros + 1)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Répartition des cagnottes par jour, mois ou annee
gains_par_jour = df.groupby('jour_de_tirage')['rapport_du_rang1'].mean().sort_index()
gains_par_jour_semaine = df.groupby('jour_de_la_semaine_de_tirage')['rapport_du_rang1'].mean().sort_index()

couleurs_gains_par_jour = ['#838eff' if count > 8*1e6 else '#83bcff' for count in gains_par_jour]
couleurs_gains_par_jour_semaine = ['#838eff' if count == gains_par_jour_semaine.max() else '#83bcff' for count in gains_par_jour_semaine]


## Tracé du graphique
plt.figure(figsize=(8, 4))
gains_par_jour.plot(kind='bar',color=couleurs_gains_par_jour)
plt.title("Cagnotte moyenne du Rang 1 par jour de tirage")
plt.xlabel("Jour")
plt.ylabel("Cagnotte moyenne (€)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

## Tracé du graphique
plt.figure(figsize=(8, 4))
gains_par_jour_semaine.plot(kind='bar',color=couleurs_gains_par_jour_semaine)
plt.title("Cagnotte moyenne du Rang 1 par jour de tirage")
plt.xlabel("Jour")
plt.ylabel("Cagnotte moyenne (€)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# Présence ou absence de gagnants au rang 1
df['gagnant_rang1'] = df['nombre_de_gagnant_au_rang1'] > 0
winner_or_not = df['gagnant_rang1'].value_counts()


# Sélection des colonnes des gains
colonnes_gains = [f'rapport_du_rang{i}' for i in range(1, 10)]

# Matrice de corrélation
correlation = df[colonnes_gains].corr()

# Affichage avec heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Corrélation entre les montants gagnés par rang")
plt.tight_layout()
plt.show()


plt.figure(figsize=(12, 5))
plt.plot(df['date_de_tirage'], df['rapport_du_rang1'], marker='o', linestyle='-', alpha=0.6)
plt.title("Évolution de la cagnotte (rang 1) dans le temps")
plt.xlabel("Date")
plt.ylabel("Montant (euros)")
plt.grid(True)
plt.tight_layout()
plt.show()

df.groupby('jour_de_la_semaine_de_tirage')['rapport_du_rang1'].mean().plot(
    kind='bar', figsize=(8, 4), title="Cagnotte moyenne (rang 1) par jour de tirage")
plt.ylabel("Montant moyen en euros")
plt.grid(axis='y')
plt.tight_layout()
plt.show()


# Filtrer les lignes valides
df_plot = df[['nombre_de_gagnant_au_rang1', 'rapport_du_rang1']].dropna()
df_plot = df_plot[df_plot['nombre_de_gagnant_au_rang1'] > 0]  # éviter division par zéro ou log(0)

# Graphique en échelle logarithmique
plt.figure(figsize=(10, 6))
plt.scatter(
    df_plot['nombre_de_gagnant_au_rang1'],
    df_plot['rapport_du_rang1'],
    alpha=0.6,
    edgecolors='k'
)
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Nombre de gagnants (Rang 1)")
plt.ylabel("Montant de la cagnotte (Rang 1)")
plt.title("Relation entre nombre de gagnants et montant du Rang 1")
plt.grid(True, which="both", ls="--", linewidth=0.5)
plt.tight_layout()
plt.show()

# Sélection et nettoyage des données pertinentes
colonnes = ['rapport_du_rang1', 'rapport_du_rang1_second_tirage']
df_comparaison = df[colonnes].dropna()

# Création du graphique
plt.figure(figsize=(8, 6))
plt.scatter(
    df_comparaison['rapport_du_rang1'],
    df_comparaison['rapport_du_rang1_second_tirage'],
    alpha=0.6,
    edgecolors='k'
)

# Ajout de la diagonale de référence (égalité parfaite)
limites = [
    min(df_comparaison.min()),
    max(df_comparaison.max())
]
plt.plot(limites, limites, 'r--', label="Égalité parfaite")

# Personnalisation du graphique
plt.xlabel("Montant Rang 1 – Tirage principal (€)")
plt.ylabel("Montant Rang 1 – Second tirage (€)")
plt.title("Comparaison des cagnottes Rang 1\nTirage principal vs Second tirage")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Sélection des données valides
df_valide = df[['rapport_du_rang1', 'rapport_du_rang1_second_tirage']].dropna()
df_valide = df_valide[(df_valide['rapport_du_rang1'] > 0) & (df_valide['rapport_du_rang1_second_tirage'] > 0)]

# Passage en log10
X_log = np.log10(df_valide['rapport_du_rang1'].values.reshape(-1, 1))
y_log = np.log10(df_valide['rapport_du_rang1_second_tirage'].values)

# Régression linéaire en log-log
reg = LinearRegression()
reg.fit(X_log, y_log)
y_pred = reg.predict(X_log)

# Tracé du nuage de points + droite de régression
plt.figure(figsize=(10, 6))
plt.scatter(X_log, y_log, alpha=0.5, edgecolors='k', label='Observations')
plt.plot(X_log, y_pred, color='red', label='Régression linéaire')
plt.xlabel("log₁₀(Montant Rang 1 – Tirage principal)")
plt.ylabel("log₁₀(Montant Rang 1 – Second tirage)")
plt.title("Régression log-log entre les montants des deux tirages (rang 1)")
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# Affichage des coefficients
print(f"Équation en log-log : log(y) = {reg.coef_[0]:.2f} × log(x) + {reg.intercept_:.2f}")