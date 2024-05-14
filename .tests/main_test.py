"""
Ce fichier a pour but de construire la source de vérité
à partir des données de test et de lancer tous les tests
"""
import chronological_order_test
import structure_test

raw_file = ".tests/source_of_truth.csv"


def test_main_function():
    with open(raw_file, "r", encoding="utf-8-sig") as file:
        content = file.readlines()
    first_line, transactions = content[0], content[1:]
    # vérifier la bonne structure du fichier
    structure_test.test_first_line(first_line)
    for transaction in transactions:
        structure_test.test_line_length(transaction)
        date, amount, transaction_type, description = transaction.split(",")
        structure_test.test_date_field(date)
        structure_test.test_amount_field(amount)
        structure_test.test_transaction_type_field(transaction_type)
        structure_test.test_description_field(description)
    # vérifier que l'ordre chronologique est respecté
    chronological_order_test.test_chronological_order(transactions)


if __name__ == '__main__':
    test_main_function()
