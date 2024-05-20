from collections import namedtuple

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
)
from PySide6.QtCore import Qt, Slot

from GUI.parameters_layout import OneMonthParametersWidget
from GUI.sums_layout import SumsLayout
from GUI.chart_layouts import PieChartsLayout
from GUI.launch_compute import select_transactions
import GUI.bar_chart as bar_chart
from GUI.selection_widget import SelectionWidget
from GUI.one_month_view import OneMonthView

from Backend.transactions_statistics import compute_sum
from Backend.select_transactions import (
    select_transactions_by_card,
    select_transactions_by_bank_transfer,
    extract_expenses_revenus_savings,
    select_transactions_of_one_month,
    select_transactions_of_several_months
)

import global_variables as GV

# namedtuple permettant d'enregistrer quelques paramètres du layout de calculs
parameters_tuple = namedtuple("parameters_tuple",
                              ["title",
                               "list",
                               "default_text"]
                              )


class ExpensesWidget(QWidget):
    """
    Cette classe définit le widget affiché lorsque le sous-menu "Dépenses"
    est sélectionné.
    Il permet ensuite d'afficher une des 2 vues suivante:
        - une vue des dépenses sur un mois
        - une vue des dépenses sur plusieurs mois
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        # layout principal du widget courant
        expenses_layout = QVBoxLayout(self)
        expenses_layout.setSpacing(GV.horizontal_spacing)
        # widget affichant la vue sélectionnée (la vue d'un ou plusieurs mois)
        self.view_widget = QStackedWidget(self)

        """
        Widget permettant de sélectionner la vue souhaitée: soit la vue sur un
        mois, soit celle sur plusieurs mois
        """
        selection_widget = SelectionWidget(self)
        expenses_layout.addWidget(selection_widget)

        """
        Définition du widget affichant la vue sélectionnée (la vue d'un ou
        plusieurs mois)
        """
        one_month_view = OneMonthView(self, transaction_type="expenses")
        # several_months_view = SeveralMonthsView(self)
        self.view_widget.addWidget(one_month_view)
        # self.view_widget.addWidget(several_months_view)

        expenses_layout.addWidget(self.view_widget)
