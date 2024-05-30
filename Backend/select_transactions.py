
"""
L'objectif de ce module est de sélectionner les dernières transactions
(du mois, de l'année, etc) que veut l'utilisateur
"""

from Backend.transaction_exception import (
    is_a_transaction,
    TransactionError,
    check_all_transactions
)

###############################################################################
# Variables globales relatives à ce fichier
###############################################################################
descriptions_epargne = ["Livret A",
                        "SEPA M ANTOINE THIRION",
                        "SEPA Hello bank",
                        "SEPA Fortuneo banque",
                        ]

###############################################################################
# Fonctions
###############################################################################


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
    except KeyError:
        error_msg = f"Le numéro du mois suivant est incorrect: {month}"
        raise KeyError(error_msg)
    return month_string + year + ".csv"


def get_last_month_year(transactions):
    """
    Retourne le dernier mois et la dernière année des transactions fournies
    """
    if is_a_transaction(transactions[0]):
        _, month, year = transactions[0].split(",")[0].split("/")
        for transaction in transactions[1:]:
            if is_a_transaction(transaction):
                _, current_month, current_year = \
                    transaction.split(",")[0].split("/")
                if (current_month != month):
                    month = current_month
                if (current_year != year):
                    year = current_year
            else:
                raise TransactionError(transaction)
        return (int(month), int(year))
    else:
        raise TransactionError(transactions[0])


def select_transactions_of_several_months(transactions, n_month=1, n_year=0):
    """
    @parameter month: sélectionner les transactions des n derniers mois
    @parameter year: sélectionner les transactions des n dernières années
    Par défaut, sélectionner les transactions du mois passé (mois courant)
    """
    selected_transactions = []
    last_month, last_year = get_last_month_year(transactions)
    first_year = last_year
    # on définit les premiers jour, mois et année où commencer la sélection
    n_month += n_year * 12
    first_month = last_month - (n_month - 1)
    if first_month == 0:
        first_year = last_year - 1
        first_month = 12
    elif first_month < 0:
        first_year = last_year + first_month // 12
        first_month = first_month % 12
    for transaction in transactions:
        if is_a_transaction(transaction):
            _, current_month, current_year = \
                transaction.split(",")[0].split("/")
            if first_year < last_year:
                # pour selectionner la transaction, on distingue trois cas:
                # si l'annee courante est égale à la premiere annee, on ignore
                # les transactions correspondantes aux mois >= first_month
                # si l'annee courante est égale à la dernière annee, on ignore
                # les transactions correspondantes aux mois <= last_month
                # sinon, on ignore les transactions correspondantes à tous les
                # mois
                if (int(current_year) == first_year and
                        int(current_month) >= first_month):
                    selected_transactions.append(transaction)
                elif (int(current_year) == last_year and
                      int(current_month) <= last_month):
                    selected_transactions.append(transaction)
                elif (first_year < int(current_year) < last_year):
                    selected_transactions.append(transaction)
            elif first_year == last_year:
                if (int(current_year) == last_year and
                        first_month <= int(current_month) <= last_month):
                    selected_transactions.append(transaction)
            else:
                raise ValueError(
                    "L'année de fin est supérieure à l'année de début")
        else:
            raise TransactionError(transaction)
    # avant de renvoyer les transactions, vérifier qu'elles sont toutes
    # correctes
    check_all_transactions(selected_transactions)
    return selected_transactions


def select_transactions_of_one_month(transactions, n_month=1, n_year=2024):
    """
    @parameter {int} n_month: sélectionner les transactions du mois n
    @parameter {int} n_year: sélectionner les transactions de l'année n
    Par défaut, sélectionner la liste des transactions de janvier 2024
    """
    selected_transactions = []
    for transaction in transactions:
        if is_a_transaction(transaction):
            _, current_month, current_year = \
                transaction.split(",")[0].split("/")
            current_month, current_year = int(current_month), int(current_year)
            if (current_month == n_month and current_year == n_year):
                selected_transactions.append(transaction)
            elif (current_month > n_month and current_year == n_year):
                # arreter de parcourir la liste des transactions
                # puisque les transactions sont rangées par ordre chronologique
                break
        else:
            raise TransactionError(transaction)
    # avant de renvoyer les transactions, vérifier qu'elles sont toutes
    # correctes
    check_all_transactions(selected_transactions)
    return selected_transactions


def select_transactions_by_card(transactions):
    "Sélectionne uniquement les transactions faites par carte"
    return [transaction for transaction in transactions
            if transaction.split(",")[2].strip() == "Carte"]


def select_transactions_by_bank_transfer(transactions):
    "Sélectionne uniquement les transactions faites par virement"
    return [transaction for transaction in transactions
            if transaction.split(",")[2].strip() == "Virement"]


def extract_expenses_revenus_savings(transactions):
    """
    Extrait les dépenses, les revenus et l'épargne à partir de la liste
    des transactions fournie
    """
    expenses = []
    revenus = []
    savings = []
    for transaction in transactions:
        if is_a_transaction(transaction):
            amount = float(transaction.split(",")[1].strip())
            description = transaction.split(",")[-1].strip()
            if amount >= 0:
                # la transaction est un revenu
                revenus.append(transaction)
            else:
                # changer le signe du montant pour le rendre positif
                date, amount, type_transaction, description = \
                    transaction.split(",")
                new_amount = -float(amount)
                new_transaction = ",".join(
                    [date, str(new_amount), type_transaction, description])
                if description in descriptions_epargne:
                    # la transaction est une épargne
                    savings.append(new_transaction)
                else:
                    # la transaction est une dépense
                    expenses.append(new_transaction)
    return (expenses, revenus, savings)
