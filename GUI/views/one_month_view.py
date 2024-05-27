from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
)
from PySide6.QtCore import Slot

from GUI.tool_widgets.parameters_widget import OneMonthParametersWidget
from GUI.tool_widgets.sums_widget import SumsWidget
from GUI.pie_chart_widget import PieChartWidget
from GUI.source_of_truth import get_source_of_truth

from Backend.transactions_statistics import compute_sum
from Backend.select_transactions import (
    select_transactions_by_card,
    select_transactions_by_bank_transfer,
    extract_expenses_revenus_savings,
    select_transactions_of_one_month,
)

import global_variables as GV


class OneMonthView(QWidget):
    """
    Cette classe construit le widget affichant la vue sur un seul mois des
    dépenses, revenus ou de l'épargne (en fonction du menu sélectionné).
    Les dépenses, revenus ou épargne mensuels sont affichés sous
    forme de 2 camemberts (un pour les transactions par carte et un pour
    les transactions par virement)
    """

    def __init__(self, parent_widget, transaction_type):
        """
        @parameter {str} transaction_type: indique si la vue à afficher
            concerne les dépenses, les revenus ou l'épargne
        """
        super().__init__(parent=parent_widget)
        self.transaction_type = transaction_type
        self.selected_operations = []
        self.transactions, self.transactions_card = [], []
        self.transactions_bank_transfer = []
        self.expenses, self.revenus, self.savings = [], [], []

        # Mise en page
        self.page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        self.page_layout.setSpacing(GV.vertical_spacing)

        """
        Le premier widget permet à l'utilisateur de sélectionner
        les paramètres de calcul:
            - le mois et l'année sur lesquels faire l'analyse et
            - la ou les banque(s) sélectionnée(s)
        """
        parameters_widget = OneMonthParametersWidget(self)
        # récupérer les différents attributs du layout paramètres nécessaires
        # aux calculs ultérieurs
        self.month_choice = parameters_widget.month_selection_combobox
        self.year_choice = parameters_widget.year_selection_combobox
        # ajouter le layout des paramètres au layout principal de la fenetre
        self.page_layout.addWidget(parameters_widget)

        """
        Ajouter un bouton pour lancer les calculs une fois les paramètres
        saisis par l'utilisateur
        """
        launch_compute_button = QPushButton("Lancer les calculs", self)
        launch_compute_button.clicked.connect(self.lancer_calculs)
        self.page_layout.addWidget(launch_compute_button)

        """
        Ajouter un layout affichant les sommes des dépenses mensuelles
        par carte et par virement
        """
        sums = SumsWidget(self)
        self.sum_card_spending_label = sums.sum_card_spending
        self.sum_bank_transfer_spending_label = sums.sum_bank_transfer_spending
        self.page_layout.addWidget(sums)

        """
        Afficher un camembert des dépenses par carte avec les catégories de
        dépenses et leur montant associé et un camembert des dépenses
        par virement
        """
        pies_layout = QHBoxLayout()
        self.pie_chart_card = PieChartWidget(self,
                                             GV.card_chart_title)
        self.card_expenses_checkbox = self.pie_chart_card.checkbox

        self.pie_chart_bank_transfer = \
            PieChartWidget(self,
                           GV.bank_transfer_chart_title)
        self.bank_transfer_expenses_checkbox = \
            self.pie_chart_bank_transfer.checkbox

        # ajouter le layout des camemberts au layout principal de la fenetre
        pies_layout.addWidget(self.pie_chart_card)
        pies_layout.addWidget(self.pie_chart_bank_transfer)
        self.page_layout.addLayout(pies_layout)

    """
    Slot du bouton de lancement des calculs
    """

    @Slot()
    def lancer_calculs(self):
        """
        Cette méthode lance les calculs lors de l'appui sur le bouton
        à condition d'avoir la source de vérité.
        En absence de source de vérité, afficher un message et ne rien faire
        """
        # recherche de la source de vérité
        GV.source_of_truth = get_source_of_truth(self)
        if GV.source_of_truth:
            # sélection des transactions
            source_of_truth_path = Path(GV.source_of_truth)
            # sélectionner les transactions souhaitées par l'utilisateur
            transactions = source_of_truth_path.read_text(encoding="utf-8-sig")
            # on split le fichier par transaction
            transactions = transactions.split(("\n"))
            # on retire la première ligne qui correspond aux colonnes
            # et la dernière transaction qui est vide
            transactions = transactions[1:-1]
            nb_month = int(self.month_choice.currentText())
            nb_year = int(self.year_choice.currentText())
            self.selected_operations = \
                select_transactions_of_one_month(transactions,
                                                 n_month=nb_month,
                                                 n_year=nb_year)
            if not self.selected_operations:
                # pas de transaction sélectionnée
                # afficher un message d'avertissement à l'utilisateur
                QMessageBox.warning(self, "Avertissement",
                                    GV.no_transaction_found_msg)

            self.expenses, self.revenus, self.savings = \
                extract_expenses_revenus_savings(self.selected_operations)

            if (self.transaction_type == "expenses"):
                # les camemberts à afficher sont ceux des dépenses
                self.transactions = self.expenses
            elif (self.transaction_type == "revenus"):
                # les camemberts à afficher sont ceux des revenus
                self.transactions = self.revenus
            elif (self.transaction_type == "savings"):
                # les camemberts à afficher sont ceux de l'épargne
                self.transactions = self.savings
            else:
                raise ValueError("Le type de transaction fourni est incorrect")

            # on extrait les transactions par carte
            self.transactions_card = \
                select_transactions_by_card(self.transactions)
            # on extrait les transactions par virement
            self.transactions_bank_transfer = \
                select_transactions_by_bank_transfer(self.transactions)

            # calculer la somme des transactions par carte et par virement
            # et les afficher
            sum_card_expenses = compute_sum(self.transactions_card)
            sum_bank_transfer_expenses = \
                compute_sum(self.transactions_bank_transfer)
            self.sum_card_spending_label.setNum(sum_card_expenses)
            self.sum_bank_transfer_spending_label.setNum(
                sum_bank_transfer_expenses)

            # décocher les checkbox associées à chaque graphe
            for checkbox in (self.card_expenses_checkbox,
                             self.bank_transfer_expenses_checkbox):
                checkbox.setChecked(False)

            # mettre à jour les camemberts de dépenses par carte et virement
            cv = self.card_expenses_checkbox.isChecked()
            self.pie_chart_card.update_pie_chart(self.transactions_card,
                                                 condenser_value=cv)
            cv = self.bank_transfer_expenses_checkbox.isChecked()
            self.pie_chart_bank_transfer\
                .update_pie_chart(self.transactions_bank_transfer,
                                  condenser_value=cv)
