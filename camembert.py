"""
L'objectif de ce code est de construire un camembert des dépenses du mois en fonction des catégories
de dépenses
"""
import sys
import matplotlib.pyplot as plt
from collections import defaultdict


def calculer_depenses_par_categories(filename):
    """
    retourne un dictionnaire dont la valeur correspond à une catégorie de dépense
    et la valeur correspondante est la somme des montants dépensés dans cette catégorie
    """
    depenses = defaultdict(int)
    with open(filename, "r", encoding="utf-8") as csv_file:
        # ignorer la première ligne
        next(csv_file)
        for line in csv_file:
            try:
                _, montant, type_transaction, description = line.split(",")
                # on ne prend en compte que les transactions par carte
                if str(type_transaction) == "Carte":
                    depenses[description] += -float(montant)
            except ValueError as e:
                print(type(e), e)
                # on retire le saut de ligne lors du print
                print("Ligne qui pose problème: ", line[:-1])
                print("Si c'est la dernière ligne, c'est ok ;) \n")
    return depenses


def display_pie_chart():
    """
    Fonction principale
    """
    csv_filename = "../csv_files/" + sys.argv[1]
    depenses = calculer_depenses_par_categories(csv_filename)
    # afficher le camembert des dépenses avec les dépenses arrondies au centime près
    somme_depenses = sum(depenses.values())
    # plt.bar(depenses.keys(), depenses.values())
    plt.pie(depenses.values(), depenses.keys(),
            autopct=lambda val: round(val/100. * somme_depenses, 2),
            )
    plt.show()


if __name__ == "__main__":
    display_pie_chart()
