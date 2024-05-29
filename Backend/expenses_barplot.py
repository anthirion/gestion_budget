""""
Ce module extrait la somme des dépenses par mois pour ensuite pouvoir
l'afficher sous forme de diagramme en batons
"""
from collections import defaultdict


def get_expenses_per_month(transactions):
    """
    @parameter {list} transactions: liste de transactions
    A partir de la liste de transactions correspondant à la période voulue,
    cette fonction retourne un dictionnaire qui associe à chaque mois la somme
    des dépenses pour ensuite pouvoir l'afficher sous forme de diagramme en
    batons
    """
    # calculer la somme des dépenses par mois
    # et récupérer le numéro de mois et l'année
    expenses_per_month = defaultdict(float)
    _, month, year = transactions[0].split(",")[0].split("/")
    somme = float(transactions[0].split(",")[1])
    for transaction in transactions[1:]:
        _, current_month, current_year = \
            transaction.split(",")[0].split("/")
        if (month == current_month and year == current_year):
            somme += float(transaction.split(",")[1])
        else:
            month_format = "/".join([month, year])
            expenses_per_month[month_format] = round(somme, 2)
            month, year = current_month, current_year
            somme = float(transaction.split(",")[1])
    # inclure le dernier mois et la dernière somme
    month_format = "/".join([month, year])
    expenses_per_month[month_format] = round(somme, 2)
    return expenses_per_month
