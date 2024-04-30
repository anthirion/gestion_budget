from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QCheckBox, QPushButton, QMessageBox
)
from PySide6.QtGui import QPainter
from PySide6 import QtCharts
from PySide6.QtCore import Slot
from pathlib import Path
import global_variables
from GUI.pie_chart import ExpensesPieChart
from GUI.parameters_layout import ParametersLayout
from GUI.sums_layout import SumsLayout
from GUI.chart_layouts import PieChartLayout
from GUI.launch_compute_button import LaunchComputeButton

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


class OneMonthWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.transactions_selectionnees = []

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
        parameters = ParametersLayout(month_selection_list=self.month_selection_list,
                                      month_selection_default_text="11",
                                      year_selection_list=self.year_selection_list,
                                      year_selection_default_text="2023",
                                      )
        parameters_layout = parameters.parameters_layout
        self.month_selection_choice = parameters.month_selection
        self.year_selection_choice = parameters.year_selection
        self.page_layout.addLayout(parameters_layout)

        # ajouter le bouton pour lancer les calculs
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
        self.chart_layout = QHBoxLayout()
        card_chart_layout = QVBoxLayout()
        # camembert des dépenses par carte
        self.pie_card_chart_view = QtCharts.QChartView()
        self.pie_card_chart_view.setRenderHint(QPainter.Antialiasing)
        self.card_chart = QtCharts.QChart()
        # checkbox pour le camembert des dépenses par carte
        self.card_checkbox = QCheckBox("Afficher la catégorie Autres", self)
        self.card_checkbox.toggled.connect(self.card_checkbox_enclenchee)
        card_chart_layout.addWidget(self.card_checkbox)
        card_chart_layout.addWidget(self.pie_card_chart_view)

        bank_transfer_chart_layout = QVBoxLayout()
        # camembert des dépenses par virement
        self.pie_bank_transfer_chart_view = QtCharts.QChartView()
        self.pie_bank_transfer_chart_view.setRenderHint(QPainter.Antialiasing)
        self.bank_transfer_chart = QtCharts.QChart()
        # checkbox pour le camembert des dépenses par virement
        self.bank_transfer_checkbox = QCheckBox(
            "Afficher la catégorie Autres", self)
        self.bank_transfer_checkbox.toggled.connect(
            self.bank_transfer_checkbox_enclenchee)
        bank_transfer_chart_layout.addWidget(self.bank_transfer_checkbox)
        bank_transfer_chart_layout.addWidget(self.pie_bank_transfer_chart_view)

        # add widgets
        self.chart_layout.addLayout(card_chart_layout)
        self.chart_layout.addLayout(bank_transfer_chart_layout)
        self.page_layout.addLayout(self.chart_layout)

    """
    Méthodes
    """

    def update_pie_chart(self, pie_chart_view, title, condenser_value):
        """
        Cette méthode calcule puis affiche le camembert des dépenses
        """
        transactions = self.depenses_cartes if pie_chart_view == self.pie_card_chart_view \
            else self.depenses_virement
        self.updated_chart = ExpensesPieChart(
            transactions, condenser_value=condenser_value).pie_chart
        self.updated_chart.setTitle(title)
        pie_chart_view.setChart(self.updated_chart)

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
            selected_month = int(self.month_selection_choice.currentText())
            selected_year = int(self.year_selection_choice.currentText())
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
            self.depenses_cartes = select_transactions_by_card(self.depenses)
            # on extrait les transactions par virement
            self.depenses_virement = select_transactions_by_bank_transfer(
                self.depenses)

            # calculer la somme des dépenses par carte et l'afficher
            sum_card_expenses = compute_sum(self.depenses_cartes)
            self.sum_card_expenses_label.setNum(sum_card_expenses)
            sum_bank_transfer_expenses = compute_sum(self.depenses_virement)
            self.sum_bank_transfer_expenses_label.setNum(
                sum_bank_transfer_expenses)

            # mettre à jour le camembert des dépenses par carte
            title = global_variables.card_chart_title
            self.update_pie_chart(
                self.pie_card_chart_view, title, condenser_value=False)

            # mettre à jour le camembert des dépenses par virement
            title = global_variables.bank_transfer_chart_title
            self.update_pie_chart(
                self.pie_bank_transfer_chart_view, title, condenser_value=False)

    """
    Checkbox slots
    """
    @Slot()
    def card_checkbox_enclenchee(self, checked):
        condenser_local = True if checked else False
        title = global_variables.card_chart_title
        self.update_pie_chart(self.pie_card_chart_view,
                              title, condenser_value=condenser_local)

    @Slot()
    def bank_transfer_checkbox_enclenchee(self, checked):
        condenser_local = True if checked else False
        title = global_variables.bank_transfer_chart_title
        self.update_pie_chart(self.pie_bank_transfer_chart_view,
                              title, condenser_value=condenser_local)
