""""
Ce module trace un diagramme en barres de la période demandée, six mois par défaut
"""

import matplotlib.pyplot as plt
import select_transactions


def spending_barplot(transactions):
    """
    A partir de la liste de transactions correspondant à la période voulue,
    cette fonction extrait la somme des dépenses par mois et l'affiche sous
    forme de diagramme en batons
    """
    # calculer la somme des dépenses par mois
    # et récupérer le numéro de mois et l'année
    mois = []
    sommes_depenses = []
    _, month, year = transactions[0].split(",")[0].split("/")
    somme = -float(transactions[0].split(",")[1])
    for transaction in transactions[1:]:
        _, current_month, current_year = transaction.split(",")[
            0].split("/")
        if (month == current_month and year == current_year):
            somme += -float(transaction.split(",")[1])
        else:
            mois.append("/".join([month, year]))
            sommes_depenses.append(round(somme, 2))
            month, year = current_month, current_year
            somme = -float(transaction.split(",")[1])
    # inclure le dernier mois et la dernière somme
    mois.append("/".join([month, year]))
    sommes_depenses.append(round(somme, 2))
    # tracer le diagramme en batons
    _, ax = plt.subplots()
    bars = ax.bar(mois, sommes_depenses)
    ax.bar_label(bars, fmt='%.2f')
    plt.show()
