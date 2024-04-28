from PySide6.QtWidgets import (
    QPushButton, QMessageBox
)
from PySide6.QtCore import Slot
from pathlib import Path

import global_variables
from Backend.transactions_statistics import compute_sum
from Backend.select_transactions import (
    select_transactions_of_one_month,
    select_transactions_by_card,
    select_transactions_by_bank_transfer,
    extract_expenses_revenus_savings
)
from GUI.source_of_truth import (
    get_source_of_truth
)


class LaunchComputeButton(QPushButton):
    """
    Ajouter un bouton qui permet à l'utilisateur de lancer le calcul
    à partir des paramètres définis plus haut
    """

    def __init__(self, month_selection, year_selection,
                 sum_card_expenses, sum_bank_transfer_expenses,
                 method_to_launch, parent=None, **kwds):
        super().__init__(parent)
        self.parent_window = parent
        self.month_selection = month_selection
        self.year_selection = year_selection
        self.sum_card_expenses = sum_card_expenses
        self.sum_bank_transfer_expenses = sum_bank_transfer_expenses
        self.method_to_launch = method_to_launch
        self.method_parameters = kwds

        self.launch_compute_button = QPushButton("Lancer les calculs")
        self.launch_compute_button.clicked.connect(self.lancer_calculs)

    @Slot()
    def lancer_calculs(self):
        """
        Cette méthode lance les calculs lors de l'appui sur le bouton
        à condition d'avoir la source de vérité
        En absence de source de vérité, afficher un message et ne rien faire
        """
        # recherche de la source de vérité
        global_variables.source_of_truth = get_source_of_truth(self)
        if global_variables.source_of_truth:
            source_of_truth_path = Path(global_variables.source_of_truth)
            # sélectionner les transactions souhaitées par l'utilisateur
            transactions = source_of_truth_path.read_text(encoding="utf-8-sig")
            # on split le fichier par transaction
            transactions = transactions.split("\n")
            # on retire la première ligne qui correspond aux noms des colonnes
            # et la dernière transaction qui est vide
            transactions = transactions[1:-1]
            n_month = int(self.month_selection.currentText())
            n_year = int(self.year_selection.currentText())
            self.transactions_selectionnees = select_transactions_of_one_month(transactions,
                                                                               n_month=n_month,
                                                                               n_year=n_year)
            if not self.transactions_selectionnees:
                # pas de transaction sélectionnée
                # afficher un message à l'utilisateur
                QMessageBox.warning(self, "Avertissement",
                                    global_variables.no_transaction_found_msg)

            # on ne sélectionne que les dépenses pour tracer les graphes
            self.depenses, _, _ = extract_expenses_revenus_savings(
                self.transactions_selectionnees)
            # on extrait les transactions par carte
            self.depenses_cartes = select_transactions_by_card(self.depenses)
            # on extrait les transactions par virement
            self.depenses_virement = select_transactions_by_bank_transfer(
                self.depenses)

            # calculer la somme des dépenses par carte et l'afficher
            sum_card_expenses = compute_sum(self.depenses_cartes)
            self.sum_card_expenses.setNum(sum_card_expenses)
            sum_bank_transfer_expenses = compute_sum(self.depenses_virement)
            self.sum_bank_transfer_expenses.setNum(sum_bank_transfer_expenses)

            # mettre à jour le camembert des dépenses par carte
            title = global_variables.card_chart_title
            self.update_pie_chart(
                self.pie_card_chart_view, title, condenser_value=False)

            # mettre à jour le camembert des dépenses par virement
            title = global_variables.bank_transfer_chart_title
            self.update_pie_chart(
                self.pie_bank_transfer_chart_view, title, condenser_value=False)
