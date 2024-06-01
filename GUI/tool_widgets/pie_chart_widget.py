from Backend.pie_chart import split_transactions_by_categories
from PySide6.QtWidgets import (
    QGridLayout, QVBoxLayout, QHBoxLayout,
    QCheckBox, QWidget, QSlider, QLabel
)
from PySide6.QtGui import QPainter
from PySide6 import QtCharts
from PySide6.QtCore import Slot, Qt

import global_variables as GV


class PieChartWidget(QWidget):
    """
    Cette classe définit un widget contenant:
        - un camembert de dépenses (dépenses par carte ou par virement)
        - une checkbox pour afficher la catégorie "Autre" sur le camembert
        - un slider pour paramétrer la valeur seuil utiliser pour la catégorie
            "Autre"
    La vue des dépenses contiendra 2 exemplaires de ce widget (1 pour les
    dépenses par carte et 1 pour les dépenses par virement)
    """

    def __init__(self, parent_widget, chart_title):
        super().__init__(parent=parent_widget)
        self.parent_widget_ = parent_widget
        self.chart_title_ = chart_title
        self.transactions_ = []

        self.main_layout = QVBoxLayout(self)
        tools_layout = QHBoxLayout()

        self.checkbox = QCheckBox("Afficher la catégorie Autres", self)
        self.checkbox.toggled.connect(self.checkbox_enclenchee)

        self.slider = CustomSlider(self)
        # par défaut ne pas afficher le slider tant que la checkbox n'est pas
        # cochée
        self.slider.setVisible(False)

        self.pie_chart = QtCharts.QChartView(self)
        self.pie_chart.setRenderHint(QPainter.Antialiasing)

        # ajouter les widgets précédents au layout
        tools_layout.addWidget(self.checkbox)
        tools_layout.addWidget(self.slider)
        self.main_layout.addLayout(tools_layout)
        self.main_layout.addWidget(self.pie_chart)

    """
    Méthodes
    """

    def setCheckboxToFalse(self):
        """
        Cette méthode décoche la checkbox
        """
        self.checkbox.setChecked(False)

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

    @Slot()
    def checkbox_enclenchee(self, checked):
        # afficher le slider uniquement si la checkbox est cochée
        self.slider.setVisible(checked)
        condenser_local = True if checked else False
        self.update_pie_chart(self.transactions_,
                              condenser_value=condenser_local)


class CustomSlider(QWidget):
    """
    Cette classe définit un slider qui permet de changer la valeur seuil
    de la catégorie Autre
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        self.parent_widget = parent_widget
        layout = QGridLayout(self)

        slider_min_value, slider_max_value = 0, 100
        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        # ATTENTION: les valeurs des sliders sont des entiers !!!
        # la valeur du slider est un pourcentage entre 0 et 100
        self.slider.setRange(slider_min_value, slider_max_value)
        self.slider.setSingleStep(10)
        # par défaut, afficher la valeur globale du fichier global_variables
        self.slider.setSliderPosition(GV.pourcentage_cat_autres * 100)
        self.slider.valueChanged.connect(self.slider_value_changed)
        self.slider.sliderReleased.connect(self.slider_released)

        # labels indiquant les limites de valeur possibles: 0 et 100
        min_label = QLabel(str(slider_min_value), self)
        max_label = QLabel(str(slider_max_value), self)
        max_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        # label indiquant la valeur actuelle sélectionnée par l'utilisateur
        self.value_label = QLabel(str(self.slider.value()), self)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.slider, 1, 0, 1, 7)
        layout.addWidget(min_label, 2, 0)
        layout.addWidget(self.value_label, 2, 3)
        layout.addWidget(max_label, 2, 6)

    @Slot()
    def slider_released(self):
        # récupérer la valeur indiquée par l'utilisateur via le slider
        value = self.slider.sliderPosition()
        GV.pourcentage_cat_autres = value / 100
        parent_wg = self.parent_widget
        parent_wg.update_pie_chart(parent_wg.transactions_,
                                   parent_wg.checkbox.isChecked())

    @Slot()
    def slider_value_changed(self):
        self.value_label.setNum(self.slider.value())
