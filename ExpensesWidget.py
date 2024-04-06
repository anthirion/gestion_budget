from PySide6.QtWidgets import (
    QLabel, QWidget, QComboBox,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from PySide6.QtCharts import QChartView, QPieSeries, QChart

from pathlib import Path
import expenses_statistics
import select_transactions
import camembert


class ExpensesWidget(QWidget):
    def __init__(self, clean_csv_filename):
        super().__init__()
        self.clean_csv_filename = clean_csv_filename
        """
        Données à utiliser: transactions du dernier mois
        """
        source_of_truth_path = Path(self.clean_csv_filename)
        transactions = source_of_truth_path.read_text(encoding="utf-8-sig")
        # on split le fichier par transaction
        transactions = transactions.split(("\n"))
        # on retire la première ligne qui correspond aux colonnes
        transactions = transactions[1:]
        transactions_selectionnees = select_transactions.select_transactions(transactions,
                                                                             n_month=1,
                                                                             n_year=0)
        """
        Création de l'interface des dépenses contenant:
            - la somme des dépenses
            - un camembert représentant les catégories de dépenses et leur montant
        """
        page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        page_layout.setSpacing(20)
        # définir le widget qui permet à l'utilisateur de sélectionner
        # les paramètres : la période sur laquelle faire l'analyse et
        # la ou les banque(s) sélectionnée(s)

        parameters_layout = QHBoxLayout()
        parameters_layout.addWidget(QLabel("Période :"))
        # sélectionner la période
        # periode en mois
        month_selection = QComboBox()
        one_to_eleven_strings = [str(i) for i in range(1, 12)]
        month_selection.insertItems(0, one_to_eleven_strings)
        parameters_layout.addWidget(month_selection)
        parameters_layout.addWidget(QLabel("mois"))
        # periode en années
        parameters_layout.addWidget(QLabel("et"))
        year_selection = QComboBox()
        one_to_eleven_strings = [str(i) for i in range(1, 12)]
        year_selection.insertItems(0, one_to_eleven_strings)
        parameters_layout.addWidget(year_selection)
        parameters_layout.addWidget(QLabel("années"))

        # sélectionner la banque
        label = QLabel("Banque sélectionnée :")
        bank_choice = QComboBox()
        bank_choice.insertItem(0, "Toutes les banques")
        bank_choice.insertItem(1, "LCL")
        parameters_layout.addWidget(label)
        parameters_layout.addWidget(bank_choice)

        # définir le widget affichant à la somme des dépenses du mois
        title = QLabel("Somme des dépenses de la période sélectionnée:")
        title.setAlignment(Qt.AlignCenter)
        display_sum = QLabel()
        display_sum.setAlignment(Qt.AlignCenter)
        sum_expenses = expenses_statistics.compute_sum(
            transactions_selectionnees)
        display_sum.setNum(sum_expenses)

        # définir le widget correspondant au camembert des dépenses du mois passé
        chart_view = QChartView()
        chart_view.setRenderHint(QPainter.Antialiasing)

        expenses = camembert.calculer_depenses_par_categories(
            transactions_selectionnees)
        series = QPieSeries()
        for categorie, montant in expenses.items():
            series.append(categorie, montant)
        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        chart_view.setChart(chart)

        # ajouter les widgets et layout à la page
        page_layout.addLayout(parameters_layout)
        page_layout.addWidget(title)
        page_layout.addWidget(display_sum)
        page_layout.addWidget(chart_view)
