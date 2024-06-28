"""
Ce module propose des tests unitaires pour tester :
    - la création de la source de la source de vérité à partir de fichiers
        de transactions bruts
    - les sommes de dépenses (par carte et par virement)
    - la construction des catégories utilisées pour les camemberts des dépenses
    - le diagramme en bâtons
"""

from pathlib import Path

from Backend.create_unique_csv import create_source_of_truth
from tests.structure import check_structure
from tests.chronological_order import check_chronological_order
from tests.sum_expenses import check_period_expenses_sums

test_transactions_directory = "tests/raw_transactions"
source_of_truth_filename = "tests/source_of_truth.csv"


def build_source_of_truth():
    create_source_of_truth(test_transactions_directory,
                           source_of_truth_filename)
    with open(source_of_truth_filename, "r", encoding="utf-8-sig") as file:
        content = file.readlines()
    first_line, transactions = content[0], content[1:]
    return (first_line, transactions)


def test_source_of_truth_build():
    first_line, transactions = build_source_of_truth()
    check_structure(first_line, transactions)
    check_chronological_order(transactions)


def test_sums():
    _, transactions = build_source_of_truth()
    check_period_expenses_sums(transactions)


def test_last():
    """
    Supprimer la source de vérité créée pour les tests
    """
    source_of_truth_path = Path(source_of_truth_filename)
    source_of_truth_path.unlink()
    assert source_of_truth_path.exists() is False
