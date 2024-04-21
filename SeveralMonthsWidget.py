from PySide6.QtWidgets import (
    QLabel, QWidget, QComboBox, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtCharts import QChartView
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPainter

from pathlib import Path
import transactions_statistics
from select_transactions import (
    select_transactions_of_several_months,
    extract_expenses_revenus
)
import CommonWidgets
import BarChart


class SeveralMonthsWidget(QWidget):
    def __init__(self, clean_csv_filename):
        super().__init__()
        self.clean_csv_filename = clean_csv_filename
        self.transactions_selectionnees = []
        self.depenses = []
        self.revenus = []

        # Mise en page
        self.page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        self.page_layout.setSpacing(20)

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
        # définir la période par défaut à 5 mois
        self.month_selection.setCurrentText("5")
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
        Afficher la somme des dépenses et des revenus sur la période sélectionnée
        """
        expenses_title = QLabel(
            "Somme des dépenses sur la période sélectionnée:")
        expenses_title.setAlignment(Qt.AlignCenter)
        self.display_sum_expenses = QLabel("0")
        self.display_sum_expenses.setAlignment(Qt.AlignCenter)

        """
        Afficher le diagramme en bâtons des dépenses par mois
        """
        self.bar_chart = QWidget()

        self.page_layout.addLayout(parameters_layout)
        self.page_layout.addWidget(launch_compute_button)

    """
    Méthodes
    """

    def plot_barchart(self):
        self.bar_chart = BarChart.BarChart(depenses=self.depenses,
                                           revenus=self.revenus).bar_canvas
        self.page_layout.addWidget(self.bar_chart)

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
        # et la dernière transaction qui est vide
        transactions = transactions[1:-1]
        nb_month = int(self.month_selection.currentText())
        nb_year = int(self.year_selection.currentText())
        self.transactions_selectionnees = select_transactions_of_several_months(transactions,
                                                                                n_month=nb_month,
                                                                                n_year=nb_year)
        if not self.transactions_selectionnees:
            # pas de transaction sélectionnée
            # afficher un message à l'utilisateur
            print("ATTENTION: pas de transaction sélectionnée !")

        # on ne sélectionne que les dépenses pour tracer les graphes
        self.depenses, self.revenus = extract_expenses_revenus(
            self.transactions_selectionnees)
        # calculer la somme des dépenses et l'afficher
        sum_expenses = transactions_statistics.compute_sum(
            self.transactions_selectionnees)
        self.display_sum_expenses.setNum(sum_expenses)

        # afficher le diagramme en batons des dépenses mensuelles
        self.plot_barchart()
