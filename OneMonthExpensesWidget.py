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
    select_transactions_by_card
)
import PieChart
import CommonWidgets


class OneMonthExpensesWidget(QWidget):
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
        Afficher la somme des dépenses sur le mois sélectionné
        """
        title = QLabel("Somme des dépenses par carte sur le mois sélectionné:")
        title.setAlignment(Qt.AlignCenter)
        self.display_sum = QLabel()
        self.display_sum.setAlignment(Qt.AlignCenter)
        self.page_layout.addWidget(title)
        self.page_layout.addWidget(self.display_sum)

        """
        Ajouter le camembert des dépenses avec les catégories de dépenses et
        leur montant associé
        """
        self.chart_layout = QHBoxLayout()
        self.pie_chart_view = QtCharts.QChartView()
        self.chart = QtCharts.QChart()
        self.pie_chart_view.setRenderHint(QPainter.Antialiasing)
        self.checkbox = QCheckBox("Afficher la catégorie Autres", self)
        self.checkbox.toggled.connect(self.checkbox_enclenchee)
        self.chart_layout.addWidget(self.pie_chart_view)
        self.chart_layout.addWidget(self.checkbox)
        self.page_layout.addLayout(self.chart_layout)

    """
    Méthodes
    """

    def update_pie_chart(self, condenser_value):
        """
        Cette méthode calcule puis affiche le camembert des dépenses
        """
        self.updated_chart = self.chart.compute_pie_chart(condenser_value)
        self.pie_chart_view.setChart(self.updated_chart)

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
        # on ne prend en compte que les transactions par carte
        self.transactions_selectionnees = select_transactions_by_card(
            self.transactions_selectionnees)

        if not self.transactions_selectionnees:
            # pas de transaction sélectionnée
            # afficher un message à l'utilisateur
            print("ATTENTION: pas de transaction sélectionnée !")

        # calculer la somme des dépenses et l'afficher
        sum_expenses = transactions_statistics.compute_sum(
            self.transactions_selectionnees)
        self.display_sum.setNum(sum_expenses)

        # mettre à jour le camembert des dépenses
        self.chart = PieChart.ExpensesPieChart(self.transactions_selectionnees)
        self.update_pie_chart(condenser_value=False)

    """
    Checkbox slot
    """
    @Slot()
    def checkbox_enclenchee(self, checked):
        condenser_local = True if checked else False
        self.update_pie_chart(condenser_value=condenser_local)
