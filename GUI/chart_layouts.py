from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QCheckBox,
    QLayout
)
from PySide6.QtGui import QPainter
from PySide6 import QtCharts
import global_variables as GV
from PySide6.QtCore import Slot
from GUI.pie_chart import ExpensesPieChart


class PieChartsLayout(QLayout):
    """
    Cette classe définit le layout correspondant aux 2 camemberts:
        - camembert des dépenses mensuelles par carte
        - camembert des dépenses mensuelles par virement
    """

    def __init__(self, one_month_widget):
        super().__init__()

        self.charts_layout = QHBoxLayout()

        # camembert des dépenses par carte
        self.card_expenses_chart_ = \
            ChartLayout(GV.card_chart_title,
                        one_month_widget,
                        card_chart=True,
                        )
        self.card_expenses_chart_layout_ = \
            self.card_expenses_chart_.chart_layout

        self.card_expenses_checkbox = self.card_expenses_chart_.checkbox

        # camembert des dépenses par virement
        self.bank_transfer_expenses_chart_ = \
            ChartLayout(GV.bank_transfer_chart_title,
                        one_month_widget,
                        card_chart=False,
                        )
        self.bank_transfer_expenses_chart_layout_ = \
            self.bank_transfer_expenses_chart_.chart_layout
        self.bank_transfer_expenses_checkbox = \
            self.bank_transfer_expenses_chart_.checkbox

        # ajouter les 2 layouts au layout principal
        self.charts_layout.addLayout(self.card_expenses_chart_layout_)
        self.charts_layout.addLayout(self.bank_transfer_expenses_chart_layout_)

    """
    Méthodes
    """

    def update_pie_charts(self, common_condenser_value):
        """
        Cette méthode calcule puis affiche les 2 camemberts
        """
        self.card_expenses_chart_.update_pie_chart(common_condenser_value)
        self.bank_transfer_expenses_chart_.update_pie_chart(
            common_condenser_value)


class ChartLayout(QLayout):
    """
    Cette classe définit le layout correspondant à un camembert de dépenses
    Soit le camembert représentant les dépenses par carte soit par virement
    """

    def __init__(self, title, one_month_widget, card_chart):
        super().__init__()
        self.title_ = title
        self.transactions_ = []
        # le booleen card_chart indique si notre graphe représente les
        # dépenses par carte ou par virement (True -> par carte;
        # False -> par virement)
        self.card_chart_ = card_chart
        self.one_month_widget_ = one_month_widget

        self.chart_layout = QVBoxLayout()

        # définir le widget correspondant au graphe
        self.chart_view_ = QtCharts.QChartView()
        self.chart_view_.setRenderHint(QPainter.Antialiasing)
        # définir le widget correspondant à la checkbox
        self.checkbox = QCheckBox("Afficher la catégorie Autres")
        self.checkbox.toggled.connect(self.checkbox_enclenchee)

        # ajouter les widgets précédents au layout
        self.chart_layout.addWidget(self.checkbox)

        self.chart_layout.addWidget(self.chart_view_)

    """
    Méthodes
    """

    def get_transactions(self):
        if self.card_chart_ is True:
            self.transactions_ = self.one_month_widget_.transactions_card
        else:
            self.transactions_ = \
                self.one_month_widget_.transactions_bank_transfer
        return self.transactions_

    # force la mise à jour des transactions à partir de celles calculées
    # par le lauch compute button
    transactions = property(get_transactions)

    def update_pie_chart(self, condenser_value):
        """
        Cette méthode calcule puis affiche le camembert des dépenses
        """
        # il est important de ne pas ajouter d'underscore à self.transactions
        # pour forcer l'utilisation du getter
        updated_chart = ExpensesPieChart(
            self.transactions, condenser_value=condenser_value).pie_chart
        updated_chart.setTitle(self.title_)
        self.chart_view_.setChart(updated_chart)

    """
    Checkbox slot
    """

    @Slot()
    def checkbox_enclenchee(self, checked):
        condenser_local = True if checked else False
        self.update_pie_chart(condenser_value=condenser_local)
