from PySide6.QtWidgets import (
    QPushButton, QMessageBox,
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
    Ajouter un bouton qui permet à l'utilisateur de lancer les calculs
    à partir des paramètres saisis dans le layout des paramètres
    """

    def __init__(self, one_month_widget):
        super().__init__()
        self.one_month_widget_ = one_month_widget
        self.transactions_selectionnees = []
        self.depenses = []
        self.depenses_carte, self.depenses_virement = [], []

        self.launch_compute_button = QPushButton("Lancer les calculs")
        # self.launch_compute_button.clicked.connect(self.lancer_calculs)
        self.launch_compute_button.clicked.connect(self.test)

    @Slot()
    def test(self):
        print("hello")

    """
    Slot du bouton de lancement des calculs
    """

    @Slot()
    def lancer_calculs(self):
        """
        Cette méthode lance les calculs lors de l'appui sur le bouton
        à condition d'avoir la source de vérité
        En absence de source de vérité, afficher un message d'avertissement 
        à l'utilisateur et ne rien faire
        """
        print("slot appelé correctement")
        # recherche de la source de vérité
        global_variables.source_of_truth = get_source_of_truth(self)
        if global_variables.source_of_truth:
            source_of_truth_path = Path(global_variables.source_of_truth)
            """ Sélectionner les transactions souhaitées par l'utilisateur """
            transactions = source_of_truth_path.read_text(encoding="utf-8-sig")
            # on split le fichier par transaction
            transactions = transactions.split("\n")
            # on retire la première ligne qui correspond aux noms des colonnes
            # et la dernière transaction qui est vide
            transactions = transactions[1:-1]
            n_month = int(self.one_month_widget_.month_choice.currentText())
            n_year = int(self.one_month_widget_.year_choice.currentText())
            print("période: ", n_month, n_year)
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
            self.depenses_carte = select_transactions_by_card(self.depenses)
            # on extrait les transactions par virement
            self.depenses_virement = select_transactions_by_bank_transfer(
                self.depenses)

            """ Calculer la somme des dépenses et les afficher """
            sum_card_expenses = compute_sum(self.depenses_carte)
            self.one_month_widget_.sum_card_expenses_label.setNum(
                sum_card_expenses)
            sum_bank_transfer_expenses = compute_sum(self.depenses_virement)
            self.one_month_widget_.sum_bank_transfer_expenses_label.setNum(
                sum_bank_transfer_expenses)

            """ Mettre à jour les camembert des dépenses par carte et par virement """
            self.one_month_widget_.pie_charts.update_pie_charts(
                common_condenser_value=False)
