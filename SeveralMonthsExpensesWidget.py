from PySide6.QtWidgets import (
    QLabel, QWidget, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtCharts import (
    QChart, QBarCategoryAxis, QBarSeries, QBarSet,
    QChartView, QChart
)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPainter

from pathlib import Path
import transactions_statistics
from select_transactions import select_transactions_of_one_month
import barplot_depenses
import CommonWidgets


class SeveralMonthsExpensesWidget(QWidget):
    def __init__(self, clean_csv_filename):
        super().__init__()
        self.clean_csv_filename = clean_csv_filename
        self.transactions_selectionnees = []

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
        from_one_to_eleven_strings = [str(i) for i in range(1, 12)]
        self.month_selection.insertItems(0, from_one_to_eleven_strings)
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
        choice_bank_widget = CommonWidgets.ChoiceBankWidget()
        label = choice_bank_widget.get_label()
        bank_choice = choice_bank_widget.get_bank_choice_combobox()
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
        Afficher le diagramme en bâtons des dépenses par mois
        """
        self.barchart_view = QChartView()
        self.barchart_view.setRenderHint(QPainter.Antialiasing)

        page_layout.addLayout(parameters_layout)
        page_layout.addWidget(launch_compute_button)
        page_layout.addWidget(self.barchart_view)

    def plot_barchart(self):
        """
        Cette méthode calcule puis affiche un diagramme en bâtons des dépenses 
        mensuelles
        """
        mois, sommes_depenses_mensuelles = barplot_depenses.spending_barplot(
            self.transactions_selectionnees)
        barchart = QChart()
        series = QBarSeries()
        # affichage des mois sur l'axe des abscisses
        axis_x = QBarCategoryAxis()
        axis_x.append(mois)
        barchart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        # affichage des dépenses mensuelles
        somme_depenses = QBarSet("Somme des dépenses mensuelles")
        somme_depenses.append(sommes_depenses_mensuelles)
        series.append(somme_depenses)
        barchart.addSeries(series)
        barchart.setTitle("Dépenses mensuelles")
        # barchart.setAnimationOptions(QChart.SeriesAnimations)
        barchart.legend().setVisible(True)
        self.barchart_view.setChart(barchart)

    """
    Button slot
    """
    @Slot()
    def lancer_calculs(self):
        """
        Cette méthode lance les calculs lors de l'appui sur le bouton
        """
        # sélectionner les transactions souhaitées par l'utilisateur
        source_of_truth_path = Path(self.clean_csv_filename)
        transactions = source_of_truth_path.read_text(encoding="utf-8-sig")
        # on split le fichier par transaction
        transactions = transactions.split(("\n"))
        # on retire la première ligne qui correspond aux colonnes
        transactions = transactions[1:]
        nb_month = int(self.month_selection.currentText())
        nb_year = int(self.year_selection.currentText())
        self.transactions_selectionnees = select_transactions_of_one_month(transactions,
                                                                           n_month=nb_month,
                                                                           n_year=nb_year)
        # calculer la somme des dépenses et l'afficher
        sum_expenses = transactions_statistics.compute_sum(
            self.transactions_selectionnees)
        self.display_sum.setNum(sum_expenses)

        # afficher le diagramme en batons des dépenses mensuelles
        self.plot_barchart()
