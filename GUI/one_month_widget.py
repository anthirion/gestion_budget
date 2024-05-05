from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QCheckBox, QPushButton, QMessageBox
)
from PySide6.QtGui import QPainter
from PySide6 import QtCharts
from PySide6.QtCore import Slot
from pathlib import Path
import global_variables

from GUI.parameters_layout import ParametersLayout
from GUI.sums_layout import SumsLayout
from GUI.chart_layouts import PieChartsLayout
from GUI.launch_compute_button import LaunchComputeButton

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


class OneMonthWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.transactions_selectionnees = []
        self.depenses = []
        self.depenses_carte = []
        self.depenses_virement = []

        # Mise en page
        self.page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        self.page_layout.setSpacing(20)

        """
        Ajouter un layout permettant à l'utilisateur de saisir les paramètres
        du calcul
        """
        # sélection du mois
        from_one_to_twelve_strings = [str(i) for i in range(1, 13)]
        self.month_selection_list = from_one_to_twelve_strings
        # sélection de l'année
        from_2023_to_2026 = [str(i) for i in range(2020, 2031)]
        self.year_selection_list = from_2023_to_2026
        # définition du layout des paramètres
        parameters = ParametersLayout(month_selection_list=self.month_selection_list,
                                      month_selection_default_text="11",
                                      year_selection_list=self.year_selection_list,
                                      year_selection_default_text="2023",
                                      )
        # récupérer les différents attributs nécessaires du layout paramètres
        parameters_layout = parameters.parameters_layout
        self.month_choice = parameters.month_selection_box
        self.year_choice = parameters.year_selection_box
        # ajouter le layout des paramètres au layout principal de la fenetre
        self.page_layout.addLayout(parameters_layout)

        """
        Ajouter un bouton pour lancer les calculs une fois les paramètres saisis
        par l'utilisateur
        """
        launch_compute_button = QPushButton("Lancer les calculs")
        launch_compute_button.clicked.connect(self.lancer_calculs)
        self.page_layout.addWidget(launch_compute_button)

        """
        Ajouter un layout affichant les sommes des dépenses mensuelles
        par carte et par virement
        """
        sums = SumsLayout()
        self.sum_card_expenses_label = sums.card_expenses_label
        self.sum_bank_transfer_expenses_label = sums.bank_transfer_expenses_label
        sums_layout = sums.sums_layout
        self.page_layout.addLayout(sums_layout)

        """
        Afficher un camembert des dépenses par cartes avec les catégories de dépenses et
        leur montant associé
        et un camembert des dépenses par virement
        """
        self.pie_charts = PieChartsLayout(self)
        self.pie_charts_layout = self.pie_charts.charts_layout

        # ajouter le layout des camemberts au layout principal de la fenetre
        self.page_layout.addLayout(self.pie_charts_layout)

    """
    Slots
    """

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
            selected_month = int(self.month_choice.currentText())
            selected_year = int(self.year_choice.currentText())
            self.transactions_selectionnees = select_transactions_of_one_month(transactions,
                                                                               n_month=selected_month,
                                                                               n_year=selected_year)
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

            # calculer la somme des dépenses par carte et l'afficher
            sum_card_expenses = compute_sum(self.depenses_carte)
            self.sum_card_expenses_label.setNum(sum_card_expenses)
            sum_bank_transfer_expenses = compute_sum(self.depenses_virement)
            self.sum_bank_transfer_expenses_label.setNum(
                sum_bank_transfer_expenses)

            # mettre à jour les camemberts de dépenses par carte et par virement
            self.pie_charts.update_pie_charts(common_condenser_value=False)
