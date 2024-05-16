""""
Ce module extrait la somme des dépenses par mois pour ensuite pouvoir
l'afficher sous forme de diagramme en batons
"""
from collections import defaultdict

from Backend.select_transactions import is_a_transaction


def get_expenses_per_month(transactions):
    """
    A partir de la liste de transactions correspondant à la période voulue,
    cette fonction retourne un dictionnaire qui associe à chaque mois la somme
    des dépenses pour ensuite pouvoir l'afficher sous forme de diagramme en
    batons
    """
    # calculer la somme des dépenses par mois
    # et récupérer le numéro de mois et l'année
    expenses_per_month = defaultdict(float)
    if is_a_transaction(transactions[0]):
        _, month, year = transactions[0].split(",")[0].split("/")
        somme = float(transactions[0].split(",")[1])
        for transaction in transactions[1:]:
            try:
                _, current_month, current_year = transaction.split(",")[
                    0].split("/")
                if (month == current_month and year == current_year):
                    somme += float(transaction.split(",")[1])
                else:
                    month_format = "/".join([month, year])
                    expenses_per_month[month_format] = round(somme, 2)
                    month, year = current_month, current_year
                    somme = float(transaction.split(",")[1])
            except ValueError as e:
                # dans le cas où le sequence unpacking ne marche pas
                print(type(e), e)
                # transaction[:-1] pour retirer le saut de ligne lors du print
                print("La transaction suivante est incorrecte: ",
                      transaction[:-1])
                print("Si c'est la dernière ligne, c'est ok ;) \n")
        # inclure le dernier mois et la dernière somme
        month_format = "/".join([month, year])
        expenses_per_month[month_format] = round(somme, 2)
        return expenses_per_month
    else:
        raise ValueError(
            f"La première ligne n'est pas une transaction: {transactions[0]}")
