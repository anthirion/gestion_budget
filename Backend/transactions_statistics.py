"""
Ce module calcule des statistiques sur les dépenses données en entrées
Les statistiques calculées sont à ce jour: la somme, la moyenne et la médiane
"""
import statistics


def extract_expenses_amounts(transactions):
    return [float(transaction.split(",")[1]) for transaction in transactions]


def compute_sum(transactions):
    expenses_amounts = extract_expenses_amounts(transactions)
    return round(sum(expenses_amounts), 2)


def compute_mean(transactions):
    expenses_amounts = extract_expenses_amounts(transactions)
    return round(statistics.mean(expenses_amounts), 2)


def compute_median(transactions):
    expenses_amounts = extract_expenses_amounts(transactions)
    return round(statistics.median(expenses_amounts), 2)
