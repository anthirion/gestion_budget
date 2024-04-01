from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar, QCheckBox,
    QFileDialog, QHBoxLayout, QVBoxLayout,
    QWidget
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from PySide6.QtCharts import QChartView, QPieSeries, QChart

from pathlib import Path
import expenses_statistics
import select_transactions
import camembert


class MonthExpensesWidget(QWidget):
    def __init__(self):
        super().__init__()
        """
        Données à utiliser: transactions du dernier mois
        """
        clean_csv_filename = "/home/thiran/projets_persos/gestion_budget/csv_files/clean_csv_files/source_of_truth.csv"
        source_of_truth_path = Path(clean_csv_filename)
        transactions = source_of_truth_path.read_text(encoding="utf-8-sig")
        # on split le fichier par transaction
        transactions = transactions.split(("\n"))
        # on retire la première ligne qui correspond aux colonnes
        transactions = transactions[1:]
        transactions_dernier_mois = select_transactions.select_transactions(transactions,
                                                                            n_month=1,
                                                                            n_year=0)

        """
        Création de l'interface des dépenses du mois passé contenant:
            - la somme des dépenses du mois passé
            - un camembert représentant les catégories de dépenses et leur montant
        """
        page_layout = QVBoxLayout(self)
        # définir le widget correspondant à la somme des dépenses du mois
        sum_layout = QVBoxLayout(self)
        title = QLabel("Somme des dépenses du mois passé:")
        title.setAlignment(Qt.AlignCenter)
        display_sum = QLabel()
        display_sum.setAlignment(Qt.AlignCenter)
        sum_expenses = expenses_statistics.compute_sum(
            transactions_dernier_mois)
        display_sum.setNum(sum_expenses)
        sum_layout.addWidget(title)
        sum_layout.addWidget(display_sum)

        # définir le widget correspondant au camembert des dépenses du mois passé
        chart_view = QChartView()
        chart_view.setRenderHint(QPainter.Antialiasing)

        expenses = camembert.calculer_depenses_par_categories(
            transactions_dernier_mois)
        series = QPieSeries()
        for categorie, montant in expenses.items():
            series.append(categorie, montant)
        chart = QChart()
        chart.addSeries(series)
        chart.legend().setAlignment(Qt.AlignLeft)
        chart_view.setChart(chart)
        # rassembler les widgets en un layout
        page_layout.addLayout(sum_layout)
        page_layout.addWidget(chart_view)
