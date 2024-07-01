def is_a_transaction(transaction):
    """
    Vérifie que la ligne donnée en entrée est bien une transaction.
    Une transaction vérifie deux conditions:
        - elle a exactement 4 champs
        - son premier champ est une date qui comprend exactement 3 valeurs
            (jour, mois, annee)
    Dans les fonctions utilisant cette fonction de vérification, si check
    est False, l'exception TransactionError est levée en indiquant la ligne
    incorrecte
    """
    check = False
    if isinstance(transaction, str):
        fields = transaction.split(",")
        date = fields[0].split("/")
        check = (len(fields) == 5 and len(date) == 3)
    else:
        error_msg = f"La transaction {transaction} n'est pas une string"
        raise AttributeError(error_msg)
    return check


class TransactionError(Exception):
    """
    Cette exception est levée lorsqu'une ligne n'est pas une transaction
    Elle est levée suite à la vérification faite par la fonction
    is_a_transaction
    """

    def __init__(self, line):
        self.line = line

    def __str__(self):
        # line[:-1] permet de retirer le saut de ligne lors de l'affichage du
        # message d'erreur
        return f"La transaction suivante est incorrecte: {self.line[:-1]}"


def check_all_transactions(transactions):
    """
    Vérifie que la liste des transactions passée en paramètre est
    correcte.
    Dans les fonctions de sélection des transactions, on vérifie à
    chaque fois que les transactions sont correctes. Cela évite par
    la suite de vérifier dans les autres fonctions que les transactions
    passées en paramètre sont correctes.
    """
    for transaction in transactions:
        if not is_a_transaction(transaction):
            raise TransactionError(transaction)
