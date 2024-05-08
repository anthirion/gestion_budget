from pathlib import Path
from PySide6.QtWidgets import QMessageBox

import global_variables
from GUI.source_of_truth import (
    get_source_of_truth
)


def select_transactions(parameters, widget, select_function):
    """
    Cette fonction sélectionne les transactions de la source de vérité
    en fonction des paramètres saisis par l'utilisateur
    Elle retourne 1 si la source de vérité a été trouvée, 0 sinon
    @parameter parameters: les paramètres servant à sélectionner les transactions
    @parameter widget: widget où afficher les messages d'avertissement
    @parameter select_function: fonction à utiliser pour sélectionner
                                les transactions
    """
    transactions_selectionnees = []
    # recherche de la source de vérité
    global_variables.source_of_truth = get_source_of_truth(widget)
    if global_variables.source_of_truth:
        source_of_truth_path = Path(global_variables.source_of_truth)
        # sélectionner les transactions souhaitées par l'utilisateur
        transactions = source_of_truth_path.read_text(encoding="utf-8-sig")
        # on split le fichier par transaction
        transactions = transactions.split(("\n"))
        # on retire la première ligne qui correspond aux colonnes
        # et la dernière transaction qui est vide
        transactions = transactions[1:-1]
        nb_month = int(parameters.month_choice.currentText())
        nb_year = int(parameters.year_choice.currentText())
        transactions_selectionnees = select_function(transactions,
                                                     n_month=nb_month,
                                                     n_year=nb_year)
        if not transactions_selectionnees:
            # pas de transaction sélectionnée
            # afficher un message à l'utilisateur
            QMessageBox.warning(widget, "Avertissement",
                                global_variables.no_transaction_found_msg)

        return (1, transactions_selectionnees)

    else:
        return (0, transactions_selectionnees)
