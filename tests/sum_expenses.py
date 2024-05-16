"""
Ce module vise à tester la somme totales des dépenses inscrites dans la source
de vérité ainsi que les sommes des dépenses sur plusieurs mois
"""

from Backend.transactions_statistics import (
    compute_sum
)
from Backend.select_transactions import (
    select_transactions_of_one_month,
    select_transactions_by_card,
    select_transactions_by_bank_transfer,
    select_transactions_of_several_months,
    extract_expenses_revenus_savings
)


def check_expenses_sum(transactions, card_sum, bank_transfer_sum):
    """
    @parameter {float} card_sum: somme correcte des dépenses par carte
    @parameter {float} bank_transfer_sum: somme correcte des dépenses par
    virement
    Cette fonction vérifie que les sommes des dépenses par carte et
    par virement correspondent aux valeurs passées en paramètres.
    Pour ce faire, elle extraie les dépenses à partir des transactions
    fournies.
    Elle permet de factoriser le code de la fonction de test principale
    """
    all_expenses, _, _ = \
        extract_expenses_revenus_savings(transactions)
    expenses_by_card = \
        select_transactions_by_card(all_expenses)
    expenses_by_bank_transfer = \
        select_transactions_by_bank_transfer(all_expenses)
    assert compute_sum(expenses_by_card) == card_sum
    assert compute_sum(expenses_by_bank_transfer) == bank_transfer_sum
    sum_expenses = round(card_sum + bank_transfer_sum, 2)
    assert compute_sum(all_expenses) == sum_expenses


def check_expenses_sums(transactions):
    """
    Vérifier que les sommes des dépenses mensuelles sont correctes
    """
    # vérifier que la somme des dépenses du mois de janvier 2024 est correcte
    all_january_transactions = \
        select_transactions_of_one_month(transactions,
                                         n_month=1,
                                         n_year=2024)
    check_expenses_sum(all_january_transactions,
                       card_sum=405.6,
                       bank_transfer_sum=5.99)
    # vérifier que la somme des dépenses du mois de février 2024 est correcte
    all_febrary_transactions = \
        select_transactions_of_one_month(transactions,
                                         n_month=2,
                                         n_year=2024)
    check_expenses_sum(all_febrary_transactions,
                       card_sum=391.8,
                       bank_transfer_sum=5.99)
    # vérifier que la somme des dépenses du mois de mars 2024 est correcte
    all_march_transactions = \
        select_transactions_of_one_month(transactions,
                                         n_month=3,
                                         n_year=2024)
    check_expenses_sum(all_march_transactions,
                       card_sum=401.5,
                       bank_transfer_sum=5.99)
    # vérifier que la somme des dépenses du mois de janvier 2025 est correcte
    all_january_transactions = \
        select_transactions_of_one_month(transactions,
                                         n_month=1,
                                         n_year=2025)
    check_expenses_sum(all_january_transactions,
                       card_sum=358.4,
                       bank_transfer_sum=5.99)
    """
    Vérifier que les sommes des dépenses sur plusieurs mois sont correctes
    """
    # vérifier que la somme des dépenses des 3 derniers mois est correcte
    three_last_months_transactions = \
        select_transactions_of_several_months(transactions, n_month=3)
    check_expenses_sum(three_last_months_transactions,
                       card_sum=1204,
                       bank_transfer_sum=round(5.99*3, 2))
    # vérifier que la somme des dépenses des 5 derniers mois est correcte
    three_last_months_transactions = \
        select_transactions_of_several_months(transactions, n_month=5)
    check_expenses_sum(three_last_months_transactions,
                       card_sum=2001.4,
                       bank_transfer_sum=round(5.99*5, 2))
