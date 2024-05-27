from Backend.pie_chart import split_transactions_by_categories
from PySide6.QtWidgets import (
    QVBoxLayout, QCheckBox, QWidget
)
from PySide6.QtGui import QPainter
from PySide6 import QtCharts
from PySide6.QtCore import Slot


class PieChartWidget(QWidget):
    """
    Cette classe définit un widget contenant:
        - un camembert de dépenses (dépenses par carte ou par virement)
        - une checkbox pour afficher la catégorie "Autre" sur le camembert
    La vue des dépenses contiendra 2 exemplaires de ce widget (1 pour les
    dépenses par carte et 1 pour les dépenses par virement)
    """

    def __init__(self, parent_widget, chart_title):
        super().__init__(parent=parent_widget)
        self.parent_widget_ = parent_widget
        self.chart_title_ = chart_title
        self.transactions_ = []

        self.chart_layout = QVBoxLayout(self)

        self.checkbox = QCheckBox("Afficher la catégorie Autres", self)
        self.checkbox.toggled.connect(self.checkbox_enclenchee)

        self.pie_chart = QtCharts.QChartView(self)
        self.pie_chart.setRenderHint(QPainter.Antialiasing)

        # ajouter les widgets précédents au layout
        self.chart_layout.addWidget(self.checkbox)
        self.chart_layout.addWidget(self.pie_chart)

    """
    Méthodes
    """

    def update_pie_chart(self, transactions, condenser_value):
        """
        Cette méthode calcule puis affiche le camembert des dépenses
        @parameter transactions: transactions à afficher
        @parameter condenser_value: indique s'il faut afficher la catégorie
            Autre ou non
        """
        self.transactions_ = transactions
        updated_chart = QtCharts.QChart()
        series = QtCharts.QPieSeries()

        expenses = split_transactions_by_categories(self.transactions_,
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
        updated_chart.addSeries(series)
        # masquer la légende
        updated_chart.legend().hide()

        # mettre à jour le graphe initial
        self.pie_chart.setChart(updated_chart)

    """
    Checkbox slot
    """

    @Slot()
    def checkbox_enclenchee(self, checked):
        condenser_local = True if checked else False
        self.update_pie_chart(self.transactions_,
                              condenser_value=condenser_local)
