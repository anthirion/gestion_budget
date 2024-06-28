"""
Ce fichier de tests vérifie la bonne structure de la source de vérité càd:
    - chaque ligne est composée de quatre champs
    - les champs sont (sauf pour la première ligne): date, montant, type de la
                                                    transaction, description
    - la première ligne décrit les champs: Date, Montant, Type, Description
"""


def check_first_line(first_line):
    """
    Cette fonction vérifie que la première ligne correspond bien aux
    descriptions des champs du fichier csv
    """
    first_line = first_line.strip()
    assert first_line == "Date,Amount,Type,Description,Bank"


def check_line_length(line):
    """
    @parameter {string} line: ligne à tester
    Cette fonction teste que la ligne contient bien 4 champs
    """
    assert len(line.split(",")) == 5


def check_date_field(date):
    """
    @parameter {string} date: champ à tester
    Cette fonction teste que le paramètre en entrée est une date de type
    dd/mm/yyyy
    """
    assert len(date.split("/")) == 3
    jour, mois, annee = date.split("/")
    jour, mois, annee = jour.strip(), mois.strip(), annee.strip()
    # vérifier que le type est bien dd/mm/yyyy
    for element in (jour, mois):
        assert isinstance(element, str) is True
        assert len(element) == 2
    assert isinstance(annee, str) is True
    assert len(annee) == 4
    # vérifier que le jour, mois, annee sont dans le bon intervalle
    int_jour, int_mois, int_annee = int(jour), int(mois), int(annee)
    assert 0 <= int_jour <= 31
    assert 1 <= int_mois <= 12
    assert int_annee >= 2000


def check_amount_field(amount):
    """
    @parameter {string} amount: champ à tester
    Cette fonction teste que le paramètre en entrée est un montant de type
    float
    """
    try:
        amount = amount.strip()
        float(amount)
    except ValueError:
        return f"The amount {amount} is not a float"


def check_transaction_type_field(transaction_type):
    """
    @parameter {string} transaction_type: champ à tester
    Cette fonction teste que le paramètre en entrée est un type de transaction
    (str) avec deux valeurs possibles: Carte ou Virement
    """
    assert isinstance(transaction_type, str) is True
    transaction_type = transaction_type.strip()
    assert (transaction_type == "Carte" or
            transaction_type == "Virement") is True


def check_description_field(description):
    """
    @parameter {string} description: champ à tester
    Cette fonction teste que le paramètre en entrée est une description de
    type str
    """
    description = description.strip()
    assert isinstance(description, str) is True


def check_structure(first_line, transactions):
    # vérifier la bonne structure du fichier
    check_first_line(first_line)
    for transaction in transactions:
        check_line_length(transaction)
        date, amount, transaction_type, description = \
            transaction.split(",")[:4]
        check_date_field(date)
        check_amount_field(amount)
        check_transaction_type_field(transaction_type)
        check_description_field(description)
