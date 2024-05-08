"""
Ce fichier de tests vérifie que les transactions de la source de vérité sont bien
dans l'ordre chronologique
Si ce n'est pas le cas, le test retourne une exception ChronologicalOrderError
"""


class ChronologicalOrderError(Exception):
    """
    Classe définissant une exception qui se déclenche dans le cas où l'ordre
    chronologique n'est pas respecté
    """
    pass


def test_chronological_order(transactions):
    """
    @parameter {list} transactions: liste de transactions 
    Cette classe vérifie que l'ordre chronologique est respecté dans les transactions
    passées en paramètre
    """
    date = transactions[0].split(",")[0]
    day, month, year = date.split("/")
    day, month, year = int(day), int(month), int(year)
    for transaction in transactions[1:]:
        current_date = transaction.split(",")[0]
        current_day, current_month, current_year = current_date.split("/")
        current_day = int(current_day)
        current_month = int(current_month)
        current_year = int(current_year)
        if (current_year == year):
            if (current_month == month):
                if (current_day < day):
                    raise ChronologicalOrderError
                else:
                    day = current_day
            else:
                if (current_month < month):
                    raise ChronologicalOrderError
                else:
                    month = current_month
        else:
            if (current_year < year):
                raise ChronologicalOrderError
            else:
                year = current_year
