from PySide6.QtCharts import (
    QBarCategoryAxis, QBarSeries, QBarSet, QChart,
    QChartView, QValueAxis
)
from PySide6 import QtGui
from PySide6.QtCore import Qt

import barplot_depenses


class BarChart(QChart):
    """
    Cette classe calcule puis affiche un diagramme en bâtons des dépenses 
    et des revenus mensuels
    """

    def __init__(self, depenses, revenus):
        super().__init__()
        self.bar_chart = QChart()
        self.depenses = depenses
        self.revenus = revenus

        mois, sommes_depenses_mensuelles = barplot_depenses.spending_barplot(
            self.depenses)
        mois, sommes_revenus_mensuels = barplot_depenses.spending_barplot(
            self.revenus)
        # définir les 2 catégories sur le diagramme en batons
        expenses = QBarSet("Dépenses")
        revenus = QBarSet("Revenus")
        expenses.append(sommes_depenses_mensuelles)
        revenus.append(sommes_revenus_mensuels)

        # définir les valeurs
        series = QBarSeries()
        series.append(expenses)
        series.append(revenus)

        # ajout des series au graphe et quelques configurations
        self.bar_chart.addSeries(series)
        self.bar_chart.setTitle(
            "Dépenses et revenus mensuels sur la période sélectionnée")
        self.bar_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.bar_chart.legend().setVisible(True)
        self.bar_chart.legend().setAlignment(Qt.AlignBottom)

        # définir l'axe des abscisses sur lequel on affiche les mois
        axis_x = QBarCategoryAxis()
        axis_x.append(mois)
        self.bar_chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        # définir l'axe des ordonnées sur lequel on affiche les montants
        axis_y = QValueAxis()
        axis_y.setRange(0, 10_000)
        self.bar_chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
