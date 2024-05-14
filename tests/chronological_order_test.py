"""
Ce fichier de tests vérifie que les transactions de la source de vérité sont
bien dans l'ordre chronologique.
Si ce n'est pas le cas, le test retourne une exception ChronologicalOrderError
"""


class ChronologicalOrderError(Exception):
    """
    Classe définissant une exception qui se déclenche dans le cas où l'ordre
    chronologique des transactions n'est pas respecté.
    Pour débugguer plus facilement, on affiche la transaction en cause ainsi
    que la transaction précédente
    """

    def __init__(self, transaction_courante, transaction_prec):
        message = f"La transaction qui n'est pas dans l'ordre chronologique \
                    est: {transaction_courante}. \n La transaction précédente \
                    est: {transaction_prec}"
        super().__init__(message)


def check_chronological_order(transactions):
    """
    @parameter {list} transactions: liste des transactions à tester
    Cette classe vérifie que l'ordre chronologique est respecté dans les
    transactions passées en paramètre
    """
    previous_date = transactions[0].split(",")[0]
    previous_day, previous_month, previous_year = previous_date.split("/")
    previous_day = int(previous_day)
    previous_month = int(previous_month)
    previous_year = int(previous_year)
    previous_transaction = ""
    for transaction in transactions:
        current_date = transaction.split(",")[0]
        current_day, current_month, current_year = current_date.split("/")
        current_day = int(current_day)
        current_month = int(current_month)
        current_year = int(current_year)
        if (current_year == previous_year):
            if (current_month == previous_month):
                if (current_day < previous_day):
                    raise ChronologicalOrderError(transaction,
                                                  previous_transaction)
                else:
                    previous_day = current_day
            else:
                if (current_month < previous_month):
                    raise ChronologicalOrderError(transaction,
                                                  previous_transaction)
                else:
                    previous_month = current_month
                    previous_day = current_day
        else:
            if (current_year < previous_year):
                raise ChronologicalOrderError(transaction,
                                              previous_transaction)
            else:
                previous_year = current_year
                previous_month = current_month
                previous_day = current_day
        previous_transaction = transaction


def test_chronological_order():
    raw_file = ".tests/source_of_truth.csv"
    with open(raw_file, "r", encoding="utf-8-sig") as file:
        content = file.readlines()
    _, transactions = content[0], content[1:]
    # vérifier que l'ordre chronologique est respecté
    check_chronological_order(transactions)
