"""
L'objectif de ce code est de construire un camembert des dépenses du mois en fonction des catégories
de dépenses
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt
# from pprint import pprint


def changer_signe_debits(budget):
    """ 
    pour afficher un camembert, les valeurs doivent être positives
    or dans le csv les débits sont négatifs
    donc on retire les valeurs positives (crédits > débits; très rare) et on prend
    la valeur absolue pour les valeurs négatives
    """
    # on ne garde que les colonnes où le montant est négatif (débits)
    debits = budget[budget["Montant"] < 0]
    # on change le signe des débits pour les rendre positifs
    debits.loc[:, "Montant"] = -debits.loc[:, "Montant"]
    return debits


def get_depenses(transactions):
    """
    on somme les dépenses pour chaque catégorie de dépenses
    """
    transactions_par_categorie = transactions.groupby("Description")
    return transactions_par_categorie.sum()["Montant"]


def get_categories_depenses(transactions):
    transactions_without_duplicates = transactions.drop_duplicates(
        subset="Description")
    tuple_categories = transactions_without_duplicates.groupby("Description")[
        "Description"]
    # on souhaite uniquement récupérer le nom de la categorie
    # ie le premier élément du tuple catégorie
    return [categorie[0] for categorie in tuple_categories]


def display_pie_chart():
    """
    Fonction principale
    """
    csv_filename = "../csv_files/" + sys.argv[1]
    budget = pd.read_csv(csv_filename)
    # rendre les montants positifs pour afficher le camembert
    budget = changer_signe_debits(budget)
    # on ne s'intéresse qu'aux transactions par carte
    transactions_carte = budget[budget["Type"] == "Carte"]
    # on récupère les catégories et dépenses à afficher sur le camembert
    depenses = get_depenses(transactions_carte)
    categories_depenses = get_categories_depenses(transactions_carte)
    # afficher le camembert des dépenses avec les dépenses arrondies au centime près
    plt.pie(depenses, labels=categories_depenses,
            autopct=lambda val: round(val/100. * depenses.sum(), 2),
            )
    plt.show()


if __name__ == "__main__":
    display_pie_chart()
