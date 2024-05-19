from collections import namedtuple

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
)
from PySide6.QtCore import Slot

from GUI.parameters_layout import ParametersLayout
from GUI.sums_layout import SumsLayout
from GUI.chart_layouts import PieChartsLayout
from GUI.launch_compute import select_transactions

from Backend.transactions_statistics import compute_sum
from Backend.select_transactions import (
    select_transactions_by_card,
    select_transactions_by_bank_transfer,
    extract_expenses_revenus_savings
)
from Backend.select_transactions import select_transactions_of_one_month

# namedtuple permettant d'enregistrer plusieurs paramètres
parameters_tuple = namedtuple("parameters_tuple",
                              ["title",
                               "list",
                               "default_text"]
                              )


class OneMonthWidget(QWidget):
    """
    Cette classe construit le widget affichant les dépenses mensuelles
    par carte et virement en fonction des catégories de dépenses
    """

    def __init__(self):
        super().__init__()
        self.transactions_selectionnees = []
        self.depenses = []
        self.depenses_carte = []
        self.depenses_virement = []

        # Mise en page
        self.page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        self.page_layout.setSpacing(20)

        """
        Ce widget permet à l'utilisateur de sélectionner
        les paramètres de calcul:
            - le mois sur lequel faire l'analyse et
            - la ou les banque(s) sélectionnée(s)
        """
        # sélection du mois
        from_one_to_twelve_strings = [str(i) for i in range(1, 13)]
        self.month_selection_title = "Mois sélectionné :"
        self.month_selection_list = from_one_to_twelve_strings
        self.month_selection_default_text = "11"

        month_selection_parameters = \
            parameters_tuple(self.month_selection_title,
                             self.month_selection_list,
                             self.month_selection_default_text,
                             )
        # sélection de l'année
        from_2023_to_2026 = [str(i) for i in range(2020, 2031)]
        self.year_selection_title = "/"
        self.year_selection_list = from_2023_to_2026
        self.year_selection_default_text = "2023"
        year_selection_parameters = \
            parameters_tuple(self.year_selection_title,
                             self.year_selection_list,
                             self.year_selection_default_text,
                             )
        # définition du layout des paramètres
        parameters = ParametersLayout(month_selection_parameters,
                                      year_selection_parameters,
                                      )
        # récupérer les différents attributs nécessaires du layout paramètres
        parameters_layout = parameters.parameters_layout
        self.month_choice = parameters.month_selection_box
        self.year_choice = parameters.year_selection_box
        # ajouter le layout des paramètres au layout principal de la fenetre
        self.page_layout.addLayout(parameters_layout)

        """
        Ajouter un bouton pour lancer les calculs une fois les paramètres
        saisis par l'utilisateur
        """
        launch_compute_button = QPushButton("Lancer les calculs")
        launch_compute_button.clicked.connect(self.lancer_calculs)
        self.page_layout.addWidget(launch_compute_button)

        """
        Ajouter un layout affichant les sommes des dépenses mensuelles
        par carte et par virement
        """
        sums = SumsLayout()
        self.sum_card_expenses_label = sums.card_expenses_label
        self.sum_bank_transfer_expenses_label = \
            sums.bank_transfer_expenses_label
        sums_layout = sums.sums_layout
        self.page_layout.addLayout(sums_layout)

        """
        Afficher un camembert des dépenses par carte avec les catégories de
        dépenses et leur montant associé et un camembert des dépenses
        par virement
        """
        self.pie_charts = PieChartsLayout(self)
        self.pie_charts_layout = self.pie_charts.charts_layout
        self.card_expenses_checkbox = self.pie_charts.card_expenses_checkbox
        self.bank_transfer_expenses_checkbox = \
            self.pie_charts.bank_transfer_expenses_checkbox

        # ajouter le layout des camemberts au layout principal de la fenetre
        self.page_layout.addLayout(self.pie_charts_layout)

    """
    Slot du bouton de lancement des calculs
    """

    @Slot()
    def lancer_calculs(self):
        """
        Cette méthode lance les calculs lors de l'appui sur le bouton
        à condition d'avoir la source de vérité.
        En absence de source de vérité, afficher un message et ne rien faire
        """
        # sélection des transactions
        period_selection = namedtuple("period_selection",
                                      ["month_choice",
                                       "year_choice"])
        period_parameters = period_selection(self.month_choice,
                                             self.year_choice)
        source_of_truth_found, self.transactions_selectionnees = \
            select_transactions(period_parameters, self,
                                select_transactions_of_one_month)

        if source_of_truth_found:
            # on ne sélectionne que les dépenses pour tracer les graphes
            self.depenses, _, _ = extract_expenses_revenus_savings(
                self.transactions_selectionnees)
            # on extrait les transactions par carte
            self.depenses_carte = select_transactions_by_card(self.depenses)
            # on extrait les transactions par virement
            self.depenses_virement = select_transactions_by_bank_transfer(
                self.depenses)

            # calculer la somme des dépenses par carte et l'afficher
            sum_card_expenses = compute_sum(self.depenses_carte)
            sum_bank_transfer_expenses = compute_sum(self.depenses_virement)
            self.sum_card_expenses_label.setNum(sum_card_expenses)
            self.sum_bank_transfer_expenses_label.setNum(
                sum_bank_transfer_expenses)

            # décocher les checkbox associées à chaque graphe
            for checkbox in (self.card_expenses_checkbox,
                             self.bank_transfer_expenses_checkbox):
                checkbox.setChecked(False)

            # mettre à jour les camemberts de dépenses par carte et virement
            self.pie_charts.update_pie_charts(common_condenser_value=False)
