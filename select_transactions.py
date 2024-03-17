"""
L'objectif de ce module est de sélectionner les dernières transactions (du mois, de l'année, etc) que veut l'utilisateur
"""


def is_a_transaction(transaction):
    """
    Vérifie que la ligne donnée en entrée est bien une transaction.
    Une transaction vérifie deux conditions:
        - elle a exactement 4 champs
        - son premier champ est une date qui comprend exactement 3 valeurs (jour, mois, annee)
    """
    fields = transaction.split(",")
    date = fields[0].split("/")
    return (len(fields) == 4 and len(date) == 3)


def toString(month, year):
    """
    Convertit le numéro de mois et l'année en chaine de caractère
    Ex: 01/2022 -> janv 2022
    """
    # s'assurer que le mois et l'année sont bien des chaines de caractères
    month, year = str(month), str(year)
    month_number_toString = {"01": "janv",
                             "02": "fev",
                             "03": "mars",
                             "04": "avril",
                             "05": "mai",
                             "06": "juin",
                             "07": "juil",
                             "08": "aout",
                             "09": "sept",
                             "10": "oct",
                             "11": "nov",
                             "12": "dec",
                             }
    try:
        month_string = month_number_toString[month]
    except KeyError as e:
        print("Le numéro de mois est incorrect", e)
    return month_string + year + ".csv"


def get_last_month_year(transactions):
    """
    Retourne le dernier mois et la dernière année des transactions fournies
    """
    if is_a_transaction(transactions[0]):
        _, month, year = transactions[0].split(",")[0].split("/")
        for transaction in transactions[1:]:
            if is_a_transaction(transaction):
                _, current_month, current_year = transaction.split(",")[
                    0].split("/")
                if (current_month != month):
                    month = current_month
                if (current_year != year):
                    year = current_year
        return (int(month), int(year))
    else:
        raise ValueError(
            f"La première ligne n'est pas une transaction: {transactions[0]}")


def select_transactions(transactions, n_month=1, n_year=0):
    """
    @parameter day: sélectionner la liste des transactions réaliséees les n derniers jours
    @parameter month: sélectionner la liste des transactions réaliséees les n derniers mois
    @parameter year: sélectionner la liste des transactions réaliséees les n dernières années
    Par défaut, sélectionner la liste des transactions du mois passé (mois courant)
    """
    selected_transactions = []
    last_month, last_year = get_last_month_year(transactions)
    first_year = last_year
    # on définit les premiers jour, mois et année où commencer la sélection
    n_month += n_year * 12
    first_month = last_month - (n_month-1)
    if first_month == 0:
        first_year = last_year - 1
        first_month = 12
    elif first_month < 0:
        first_year = last_year + first_month//12
        first_month = first_month % 12
    for transaction in transactions:
        if is_a_transaction(transaction):
            _, current_month, current_year = transaction.split(",")[
                0].split("/")
            if first_year < last_year:
                # pour selectionner la transaction, on distingue trois cas:
                # si l'annee courante est égale à la premiere annee, on laisse passer
                # les transactions correspondantes aux mois >= first_month
                # si l'annee courante est égale à la dernière annee, on laisse passer
                # les transactions correspondantes aux mois <= last_month
                # sinon, on laisse passer les transactions correspondantes à tous les mois
                if (int(current_year) == first_year and int(current_month) >= first_month):
                    selected_transactions.append(transaction)
                elif (int(current_year) == last_year and int(current_month) <= last_month):
                    selected_transactions.append(transaction)
                elif (first_year < int(current_year) < last_year):
                    selected_transactions.append(transaction)
            elif first_year == last_year:
                if (int(current_year) == last_year and
                        first_month <= int(current_month) <= last_month):
                    selected_transactions.append(transaction)
            else:
                raise ValueError(
                    "L'année de fin est supérieure à l'année de début\n")
    return selected_transactions
