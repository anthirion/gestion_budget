from Backend.pie_chart import split_transactions_by_categories
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QCheckBox,
    QLayout
)
from PySide6.QtGui import QPainter
from PySide6 import QtCharts
import global_variables as GV
from PySide6.QtCore import Slot


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
            PieChartWidget(GV.card_chart_title,
                           one_month_widget,
                           card_chart=True,
                           )
        self.card_expenses_chart_layout_ = \
            self.card_expenses_chart_.chart_layout

        self.card_expenses_checkbox = self.card_expenses_chart_.checkbox

        # camembert des dépenses par virement
        self.bank_transfer_expenses_chart_ = \
            PieChartWidget(GV.bank_transfer_chart_title,
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


class PieChartWidget(QLayout):
    """
    Cette classe définit un widget contenant:
        - un camembert de dépenses (dépenses par carte ou par virement)
        - une checkbox pour afficher la catégorie "Autre" sur le camembert
    La vue des dépenses contiendra 2 exemplaires de ce widget (1 pour les
    dépenses par carte et 1 pour les dépenses par virement)
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
    # par le launch compute button
    transactions = property(get_transactions)

    def update_pie_chart(self, condenser_value):
        """
        Cette méthode calcule puis affiche le camembert des dépenses
        """
        # il est important de ne PAS ajouter d'underscore à self.transactions
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


class ExpensesPieChart(QtCharts.QChart):
    """
    Cette classe calcule le camembert des dépenses passées en paramètre dans
    le constructeur
    """

    def __init__(self, transactions, condenser_value):
        """
        @parameter transactions: transactions à afficher
        @parameter condenser_value: indique s'il faut afficher la catégorie
            Autre ou non
        """
        super().__init__()
        self.transactions = transactions

        self.pie_chart = QtCharts.QChart()
        series = QtCharts.QPieSeries()

        expenses = split_transactions_by_categories(self.transactions,
                                                    condenser=condenser_value)

        # afficher les valeurs sur le camembert
        slices = []
        for categorie, amount in expenses.items():
            pie_slice = QtCharts.QPieSlice("", amount)
            label = f"<p align='center'> {categorie} <br> \
                {round(pie_slice.value(), 2)} €</p>"
            pie_slice.setLabel(label)
            slices.append(pie_slice)
            series.append(pie_slice)

        # modifier l'affichage des labels en fonction de leur pourcentage
        # for pie_slice in slices:
        #     if pie_slice.percentage() > \
        #                               GV.pourcentage_affichage_label_pie_chart:
        #         # si le montant est suffisamment grand pour être affiché
        #         # correctement dans le camembert on l'affiche à l'intérieur
        #         # et en blanc pour être lisible
        #         pie_slice.setLabelPosition(
        #             QtCharts.QPieSlice.LabelInsideHorizontal)
        #         pie_slice.setLabelColor(QtGui.QColor("white"))
        #     else:
        #         # si le montant est trop petit pour être affiché
        #         # correctement dans le camembert
        #         # on préfère l'afficher à l'extérieur et en noir
        #         pie_slice.setLabelPosition(
        #             QtCharts.QPieSlice.LabelOutside)
        #         pie_slice.setLabelColor(QtGui.QColor("black"))

        # afficher les labels sur le camembert
        series.setLabelsVisible(True)

        # mettre à jour le graphe
        self.pie_chart.addSeries(series)
        # masquer la légende
        self.pie_chart.legend().hide()
