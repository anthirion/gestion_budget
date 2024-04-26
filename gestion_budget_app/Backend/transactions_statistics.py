"""
Ce module calcule des statistiques sur les dépenses données en entrées
Les statistiques calculées sont à ce jour: la somme, la moyenne et la médiane
"""
import statistics


def extract_expenses_amounts(transactions):
    return [float(transaction.split(",")[1]) for transaction in transactions]


def compute_sum(transactions):
    expenses_amounts = extract_expenses_amounts(transactions)
    return sum(expenses_amounts)


def compute_mean(transactions):
    expenses_amounts = extract_expenses_amounts(transactions)
    return statistics.mean(expenses_amounts)


def compute_median(transactions):
    expenses_amounts = extract_expenses_amounts(transactions)
    return statistics.median(expenses_amounts)
