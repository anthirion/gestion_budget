from PySide6.QtWidgets import (
    QLabel, QWidget, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout, QCheckBox
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, Slot
from PySide6.QtCharts import (
    QChartView, QPieSeries, QChart
)

from pathlib import Path
import transactions_statistics
from select_transactions import select_transactions_of_several_months
import camembert
import CommonWidgets


class OneMonthExpensesWidget(QWidget):
    def __init__(self, clean_csv_filename):
        super().__init__()
        self.clean_csv_filename = clean_csv_filename
        self.transactions_selectionnees = []

        # Mise en page
        page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        page_layout.setSpacing(20)

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
        from_one_to_eleven_strings = [str(i) for i in range(1, 12)]
        self.month_selection.insertItems(0, from_one_to_eleven_strings)
        parameters_layout.addWidget(self.month_selection)
        # periode en années
        parameters_layout.addWidget(QLabel("/"))
        self.year_selection = QComboBox()
        from_two_thousand_twenty_to_two_thousand_thirty = [
            str(i) for i in range(2020, 2031)]
        self.year_selection.insertItems(
            0, from_two_thousand_twenty_to_two_thousand_thirty)
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

        """"
        Afficher la somme des dépenses sur le mois sélectionné
        """
        title = QLabel("Somme des dépenses sur le mois sélectionné:")
        title.setAlignment(Qt.AlignCenter)
        self.display_sum = QLabel("0")
        self.display_sum.setAlignment(Qt.AlignCenter)

        """
        Afficher le camembert des dépenses avec les catégories de dépenses et
        leur montant associé
        """
        chart_layout = QHBoxLayout()
        self.piechart_view = QChartView()
        self.piechart_view.setRenderHint(QPainter.Antialiasing)
        checkbox = QCheckBox("Afficher la catégorie Autres", self)
        checkbox.toggled.connect(self.checkbox_enclenchee)

        chart_layout.addWidget(self.piechart_view)
        chart_layout.addWidget(checkbox)

        # ajouter les widgets et layouts à la mise en page
        page_layout.addLayout(parameters_layout)
        page_layout.addWidget(launch_compute_button)
        page_layout.addLayout(chart_layout)

    def plot_piechart(self, condenser_value):
        """
        Cette méthode calcule puis affiche le camembert des dépenses
        """
        expenses = camembert.calculer_depenses_par_categories(
            self.transactions_selectionnees, condenser=condenser_value)
        series = QPieSeries()
        for categorie, montant in expenses.items():
            series.append(categorie, montant)
        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.piechart_view.setChart(chart)

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
        transactions = transactions.split(("\n"))
        # on retire la première ligne qui correspond aux colonnes
        transactions = transactions[1:]
        nb_month = int(self.month_selection.currentText())
        nb_year = int(self.year_selection.currentText())
        self.transactions_selectionnees = select_transactions_of_several_months(transactions,
                                                                                n_month=nb_month,
                                                                                n_year=nb_year)
        # calculer la somme des dépenses et l'afficher
        sum_expenses = transactions_statistics.compute_sum(
            self.transactions_selectionnees)
        self.display_sum.setNum(sum_expenses)

        # afficher le camembert des dépenses
        self.plot_piechart(condenser_value=False)

    """
    Checkbox slot
    """
    @Slot()
    def checkbox_enclenchee(self, checked):
        condenser_local = True if checked else False
        self.plot_piechart(condenser_value=condenser_local)
