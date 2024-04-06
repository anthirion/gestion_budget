from PySide6.QtWidgets import (
    QLabel, QWidget, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, Slot
from PySide6.QtCharts import QChartView, QPieSeries, QChart

from pathlib import Path
import expenses_statistics
import select_transactions
import camembert


class ExpensesWidget(QWidget):
    def __init__(self, clean_csv_filename):
        super().__init__()
        self.clean_csv_filename = clean_csv_filename

        # Mise en page
        page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        page_layout.setSpacing(20)

        """
        Le premier widget permet à l'utilisateur de sélectionner
        les paramètres de calcul : 
            - la période sur laquelle faire l'analyse et
            - la ou les banque(s) sélectionnée(s)
        """
        parameters_layout = QHBoxLayout()
        parameters_layout.addWidget(QLabel("Période :"))
        # sélectionner la période en mois
        self.month_selection = QComboBox()
        one_to_eleven_strings = [str(i) for i in range(1, 12)]
        self.month_selection.insertItems(0, one_to_eleven_strings)
        parameters_layout.addWidget(self.month_selection)
        parameters_layout.addWidget(QLabel("mois"))
        # periode en années
        parameters_layout.addWidget(QLabel("et"))
        self.year_selection = QComboBox()
        zero_to_ten_strings = [str(i) for i in range(11)]
        self.year_selection.insertItems(0, zero_to_ten_strings)
        parameters_layout.addWidget(self.year_selection)
        parameters_layout.addWidget(QLabel("années"))

        # sélectionner la banque
        label = QLabel("Banque sélectionnée :")
        bank_choice = QComboBox()
        bank_choice.insertItem(0, "Toutes les banques")
        bank_choice.insertItem(1, "LCL")

        parameters_layout.addWidget(label)
        parameters_layout.addWidget(bank_choice)

        """
        Ajouter un bouton qui permet à l'utilisateur de lancer le calcul
        à partir des paramètres définis plus haut
        """
        launch_compute_button = QPushButton("Lancer les calculs")
        launch_compute_button.clicked.connect(self.lancer_calculs)

        """"
        Afficher la somme des dépenses sur la période sélectionnée
        """
        title = QLabel("Somme des dépenses sur la période sélectionnée:")
        title.setAlignment(Qt.AlignCenter)
        self.display_sum = QLabel("0")
        self.display_sum.setAlignment(Qt.AlignCenter)

        """
        Afficher le camembert des dépenses avec les catégories de dépenses et
        leur montant associé
        """
        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # ajouter les widgets et layouts à la mise en page
        page_layout.addLayout(parameters_layout)
        page_layout.addWidget(launch_compute_button)
        page_layout.addWidget(title)
        page_layout.addWidget(self.display_sum)
        page_layout.addWidget(self.chart_view)

    """
    Button slot
    """
    @Slot()
    def lancer_calculs(self):
        # sélectionner les transactions souhaitées par l'utilisateur
        source_of_truth_path = Path(self.clean_csv_filename)
        transactions = source_of_truth_path.read_text(encoding="utf-8-sig")
        # on split le fichier par transaction
        transactions = transactions.split(("\n"))
        # on retire la première ligne qui correspond aux colonnes
        transactions = transactions[1:]
        nb_month = int(self.month_selection.currentText())
        nb_year = int(self.year_selection.currentText())
        transactions_selectionnees = select_transactions.select_transactions(transactions,
                                                                             n_month=nb_month,
                                                                             n_year=nb_year)
        # calculer la somme des dépenses et l'afficher
        sum_expenses = expenses_statistics.compute_sum(
            transactions_selectionnees)
        self.display_sum.setNum(sum_expenses)

        # afficher le camembert des dépenses
        expenses = camembert.calculer_depenses_par_categories(
            transactions_selectionnees)
        series = QPieSeries()
        for categorie, montant in expenses.items():
            series.append(categorie, montant)
        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        self.chart_view.setChart(chart)
