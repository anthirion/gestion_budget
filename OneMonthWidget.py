from PySide6.QtWidgets import (
    QLabel, QWidget, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QCheckBox
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, Slot
from PySide6 import QtCharts

from pathlib import Path
import transactions_statistics
from select_transactions import (
    select_transactions_of_one_month,
    select_transactions_by_card,
    select_transactions_by_bank_transfer,
    extract_expenses_revenus
)
import PieChart
import CommonWidgets

# Variables globales
card_chart_title = "Dépenses par carte"
bank_transfer_chart_title = "Dépenses par virement"


class OneMonthWidget(QWidget):
    def __init__(self, clean_csv_filename):
        super().__init__()
        self.clean_csv_filename = clean_csv_filename
        self.transactions_selectionnees = []

        # Mise en page
        self.page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        self.page_layout.setSpacing(20)

        """
        Le premier widget permet à l'utilisateur de sélectionner
        les paramètres de calcul : 
            - le mois sur lequel faire l'analyse et
            - la ou les banque(s) sélectionnée(s)
        """
        parameters_layout = QHBoxLayout()
        parameters_layout.addWidget(QLabel("Mois sélectionné :"))
        # sélectionner la période en mois
        self.month_selection = QComboBox()
        from_one_to_twelve_strings = [str(i) for i in range(1, 13)]
        self.month_selection.insertItems(0, from_one_to_twelve_strings)
        # définir le mois par défaut à 11
        self.month_selection.setCurrentText("11")
        parameters_layout.addWidget(self.month_selection)
        # periode en années
        parameters_layout.addWidget(QLabel("/"))
        self.year_selection = QComboBox()
        from_2023_to_2026 = [str(i) for i in range(2020, 2031)]
        self.year_selection.insertItems(0, from_2023_to_2026)
        # définir l'année par défaut à 2023
        self.year_selection.setCurrentText("2023")
        parameters_layout.addWidget(self.year_selection)

        # sélectionner la banque
        choice_bank_widget = CommonWidgets.ChoiceBankWidget()
        label = choice_bank_widget.get_label()
        bank_choice = choice_bank_widget.get_bank_choice_combobox()
        parameters_layout.addWidget(label)
        parameters_layout.addWidget(bank_choice)

        """
        Ajouter un bouton qui permet à l'utilisateur de lancer le calcul
        à partir des paramètres définis plus haut
        """
        launch_compute_button = QPushButton("Lancer les calculs")
        launch_compute_button.clicked.connect(self.lancer_calculs)

        # ajouter les widgets et layouts à la mise en page
        self.page_layout.addLayout(parameters_layout)
        self.page_layout.addWidget(launch_compute_button)

        """"
        Afficher la somme des dépenses par carte et par virement
        sur le mois sélectionné
        """
        sums_layout = QHBoxLayout()
        card_sum_layout = QVBoxLayout()
        # définition du titre et label pour les dépenses par carte
        card_title = QLabel(
            "Somme des dépenses par carte sur le mois sélectionné:")
        card_title.setAlignment(Qt.AlignCenter)
        self.sum_card_expenses = QLabel()
        self.sum_card_expenses.setAlignment(Qt.AlignCenter)
        card_sum_layout.addWidget(card_title)
        card_sum_layout.addWidget(self.sum_card_expenses)

        bank_transfer_sum_layout = QVBoxLayout()
        # définition du titre et label pour les dépenses par virement
        bank_transfer_title = QLabel(
            "Somme des dépenses par virement sur le mois sélectionné:")
        bank_transfer_title.setAlignment(Qt.AlignCenter)
        self.sum_bank_transfer_expenses = QLabel()
        self.sum_bank_transfer_expenses.setAlignment(Qt.AlignCenter)
        bank_transfer_sum_layout.addWidget(bank_transfer_title)
        bank_transfer_sum_layout.addWidget(self.sum_bank_transfer_expenses)

        # affichage des widgets précédemment définis
        sums_layout.addLayout(card_sum_layout)
        sums_layout.addLayout(bank_transfer_sum_layout)
        self.page_layout.addLayout(sums_layout)

        """
        Ajouter un camembert des dépenses par cartes avec les catégories de dépenses et
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
        self.updated_chart = PieChart.ExpensesPieChart(
            self.depenses_cartes, condenser_value=condenser_value).pie_chart
        self.updated_chart.setTitle(title)
        pie_chart_view.setChart(self.updated_chart)

    """
    Button slot
    """
    @Slot()
    def lancer_calculs(self):
        """
        Cette méthode lance les calculs lors de l'appui sur le bouton
        """
        # sélectionner les transactions souhaitées par l'utilisateur
        source_of_truth_path = Path(self.clean_csv_filename)
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
            print("ATTENTION: pas de transaction sélectionnée !")

        # on ne sélectionne que les dépenses pour tracer les graphes
        self.depenses, _ = extract_expenses_revenus(
            self.transactions_selectionnees)
        # on extrait les transactions par carte
        self.depenses_cartes = select_transactions_by_card(self.depenses)
        # on extrait les transactions par virement
        self.depenses_virement = select_transactions_by_bank_transfer(
            self.depenses)

        # calculer la somme des dépenses par carte et l'afficher
        sum_card_expenses = transactions_statistics.compute_sum(
            self.depenses_cartes)
        self.sum_card_expenses.setNum(sum_card_expenses)
        sum_bank_transfer_expenses = transactions_statistics.compute_sum(
            self.depenses_virement)
        self.sum_bank_transfer_expenses.setNum(sum_bank_transfer_expenses)

        # mettre à jour le camembert des dépenses par carte
        title = card_chart_title
        self.update_pie_chart(
            self.pie_card_chart_view, title, condenser_value=False)

        # mettre à jour le camembert des dépenses par virement
        title = bank_transfer_chart_title
        self.update_pie_chart(
            self.pie_bank_transfer_chart_view, title, condenser_value=False)

    """
    Checkbox slots
    """
    @Slot()
    def card_checkbox_enclenchee(self, checked):
        condenser_local = True if checked else False
        title = card_chart_title
        self.update_pie_chart(self.pie_card_chart_view,
                              title, condenser_value=condenser_local)

    @Slot()
    def bank_transfer_checkbox_enclenchee(self, checked):
        condenser_local = True if checked else False
        title = bank_transfer_chart_title
        self.update_pie_chart(self.pie_bank_transfer_chart_view,
                              title, condenser_value=condenser_local)
