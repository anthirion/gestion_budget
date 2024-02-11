"""
L'objectif de ce code est de construire un camembert des dépenses du mois en fonction de plusieurs catégories
"""
# Utiliser pandas pour la manipulation des données (+ seaborn ?) et matplotlib pour le camembert
import sys
import pandas as pd
import matplotlib.pyplot as plt

csv_filename = "../csv_files/" + sys.argv[1]

budget = pd.read_csv(csv_filename)
transactions_carte = budget[budget["Type"] == "Carte"]
transactions_virement = budget[budget["Type"] == "Virement"]
# calculer pour chaque catégorie le montant total dépensé
transactions_carte_par_categories = transactions_carte.groupby(
    "Description")
montant_transactions_par_categories = transactions_carte_par_categories.sum()[
    "Montant"]

# pour afficher un camembert, les valeurs doivent être positives
# donc on retire les valeurs positives (crédits > débits; très rare) et on prend
# la valeur absolue pour les valeurs négatives
print(budget.head(10))
# afficher le camembert associé
# labels = transactions_carte_par_categories["Description"]
# sizes = montant_transactions_par_categories
# fig, ax = plt.subplots()
# ax.pie(sizes, labels=labels)
