""""
Ce module extrait la somme des dépenses par mois pour ensuite pouvoir
l'afficher sous forme de diagramme en batons
"""

from select_transactions import is_a_transaction


def spending_barplot(transactions):
    """
    A partir de la liste de transactions correspondant à la période voulue,
    cette fonction extrait la somme des dépenses par mois pour ensuite pouvoir
    l'afficher sous forme de diagramme en batons
    """
    # calculer la somme des dépenses par mois
    # et récupérer le numéro de mois et l'année
    mois = []
    sommes_depenses_mensuelles = []
    if is_a_transaction(transactions[0]):
        _, month, year = transactions[0].split(",")[0].split("/")
        somme = -float(transactions[0].split(",")[1])
        for transaction in transactions[1:]:
            try:
                _, current_month, current_year = transaction.split(",")[
                    0].split("/")
                if (month == current_month and year == current_year):
                    somme += -float(transaction.split(",")[1])
                else:
                    mois.append("/".join([month, year]))
                    sommes_depenses_mensuelles.append(round(somme, 2))
                    month, year = current_month, current_year
                    somme = -float(transaction.split(",")[1])
            except ValueError as e:
                # dans le cas où le sequence unpacking ne marche pas
                print(type(e), e)
                # transaction[:-1] pour retirer le saut de ligne lors du print
                print("La transaction suivante est incorrecte: ",
                      transaction[:-1])
                print("Si c'est la dernière ligne, c'est ok ;) \n")
        # inclure le dernier mois et la dernière somme
        mois.append("/".join([month, year]))
        sommes_depenses_mensuelles.append(round(somme, 2))
        return (mois, sommes_depenses_mensuelles)
    else:
        raise ValueError(
            f"La première ligne n'est pas une transaction: {transactions[0]}")
