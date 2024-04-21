from PySide6.QtCharts import (
    QBarCategoryAxis, QBarSeries, QBarSet, QChart,
    QValueAxis
)
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

import barplot_depenses


class BarChart(QWidget):
    """
    Cette classe calcule puis affiche un diagramme en bâtons des dépenses 
    et des revenus mensuels
    """

    def __init__(self, depenses, revenus):
        super().__init__()
        self.depenses = depenses
        self.revenus = revenus
        self.bar_canvas = QWidget()

        """
        Extraction des mois et sommes pour afficher le diagramme
        """
        mois, sommes_depenses_mensuelles = barplot_depenses.spending_barplot(
            self.depenses)
        mois, sommes_revenus_mensuels = barplot_depenses.spending_barplot(
            self.revenus)

        categories = {
            "Dépenses": sommes_depenses_mensuelles,
            "Revenus": sommes_revenus_mensuels
        }

        """
        Tracé du diagramme en bâtons
        """
        self.bar_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        bar_ax = self.bar_canvas.figure.subplots()

        step = np.arange(len(mois))  # the label locations
        width = 0.25  # the width of the bars
        multiplier = 0

        for category, transaction in categories.items():
            offset = width * multiplier
            rects = bar_ax.bar(step + offset, transaction,
                               width, label=category)
            bar_ax.bar_label(rects, padding=3)
            multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        bar_ax.set_ylabel('Montant (en euros)')
        bar_ax.set_title(
            'Sommes des dépenses et revenus par mois sur la période sélectionnée')
        bar_ax.set_xticks(step + width, mois)
        bar_ax.legend(loc='upper left', ncols=2)
