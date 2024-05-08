"""
Ce fichier a pour but de construire la source de vérité
à partir des données de test et de lancer tous les tests
"""
import chronological_order
import structure

# file_to_test = "/home/thiran/projets_persos/gestion_budget/gestion_budget_app/.tests/transactions_tests.csv"
raw_file = "/home/thiran/projets_persos/gestion_budget/csv_files/clean_csv_files/source_of_truth.csv"


def main_test_function():
    with open(raw_file, "r", encoding="utf-8-sig") as file:
        content = file.readlines()
    first_line, transactions = content[0], content[1:]
    # vérifier la bonne structure du fichier
    structure.test_first_line(first_line)
    for transaction in transactions:
        structure.test_line_length(transaction)
        date, amount, transaction_type, description = transaction.split(",")
        structure.test_date_field(date)
        structure.test_amount_field(amount)
        structure.test_transaction_type_field(transaction_type)
        structure.test_description_field(description)
    # vérifier que l'ordre chronologique est respecté
    chronological_order.test_chronological_order(transactions)


main_test_function()
