from collections import namedtuple

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
)
from PySide6.QtCore import Qt, Slot

from GUI.parameters_layout import ParametersLayout
from GUI.sums_layout import SumsLayout
from GUI.chart_layouts import PieChartsLayout
from GUI.launch_compute import select_transactions
import GUI.bar_chart as bar_chart

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
        """
        Définition d'un layout de la vue des dépenses avec
        2 composants: les boutons de sélection de la vue
        et la vue elle-même
        """
        expenses_layout = QVBoxLayout(self)
        expenses_layout.setSpacing(GV.horizontal_spacing)
        # sélection de la vue appropriée
        selection_layout = QHBoxLayout()
        selection_layout.setSpacing(GV.vertical_spacing)
        # boutons de sélection de la vue
        one_month_selection = QPushButton("Vue sur un mois")
        one_month_selection.clicked.connect(self.one_month_view_selected)
        several_months_selection = QPushButton("Vue sur plusieurs mois")
        several_months_selection.clicked.connect(
            self.several_months_view_selected)
        for btn in (one_month_selection, several_months_selection):
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setMinimumWidth(200)

        selection_layout.addWidget(one_month_selection)
        selection_layout.addWidget(several_months_selection)
        # afficher la sélection en haut et au centre
        selection_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter |
                                      Qt.AlignmentFlag.AlignTop)

        expenses_layout.addLayout(selection_layout)
        """
        Widget affichant la vue principale (la vue d'un ou plusieurs mois)
        """
        self.vue_widget = QStackedWidget(self)
        one_month_view = OneMonthView(self)
        several_months_view = SeveralMonthsView(self)
        self.vue_widget.addWidget(one_month_view)
        self.vue_widget.addWidget(several_months_view)

        expenses_layout.addWidget(self.vue_widget)

    """
    Button slots
    """
    @Slot()
    def one_month_view_selected(self):
        """
        Afficher la vue sur un mois
        """
        self.vue_widget.setCurrentIndex(0)

    @Slot()
    def several_months_view_selected(self):
        """
        Afficher la vue sur plusieurs mois
        """
        self.vue_widget.setCurrentIndex(1)


###############################################################################
# Vue des dépenses sur un seul mois
###############################################################################


class OneMonthView(QWidget):
    """
    Cette classe construit le widget affichant les dépenses mensuelles
    par carte et virement en fonction des catégories de dépenses, sous
    forme de 2 camemberts (un pour les dépenses par carte et un pour
    les dépenses par virement)
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        self.transactions_selectionnees = []
        self.depenses = []
        self.depenses_carte = []
        self.depenses_virement = []

        # Mise en page
        self.page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        self.page_layout.setSpacing(GV.vertical_spacing)

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

###############################################################################
# Vue des dépenses sur plusieurs mois
###############################################################################


class SeveralMonthsView(QWidget):
    """
    Cette classe construit le widget affichant les sommes des dépenses
    sur plusieurs mois sous forme de diagramme en bâtons
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        self.transactions_selectionnees = []
        self.depenses = []
        self.revenus = []
        self.epargne = []

        # Mise en page
        self.page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        self.page_layout.setSpacing(GV.vertical_spacing)

        """
        Le premier widget permet à l'utilisateur de sélectionner
        les paramètres de calcul:
            - la période sur laquelle faire l'analyse et
            - la ou les banque(s) sélectionnée(s)
        """
        # sélectionner la période en mois
        from_one_to_eleven_strings = [str(i) for i in range(1, 12)]
        self.month_period_title = "Période :"
        self.month_period_list = from_one_to_eleven_strings
        self.month_period_default_text = "5"

        month_period_parameters = \
            parameters_tuple(self.month_period_title,
                             self.month_period_list,
                             self.month_period_default_text,
                             )

        # sélectionner la periode en années
        zero_to_ten_strings = [str(i) for i in range(11)]
        self.year_period_title = "et"
        self.year_period_list = zero_to_ten_strings
        self.year_period_default_text = "0"

        year_period_parameters = \
            parameters_tuple(self.year_period_title,
                             self.year_period_list,
                             self.year_period_default_text,
                             )

        # définition du layout des paramètres
        parameters = ParametersLayout(month_period_parameters,
                                      year_period_parameters,
                                      additional_texts=("mois", "annee(s)")
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

        """"
        Afficher la somme des dépenses et des revenus sur la période
        sélectionnée
        """
        expenses_title = \
            QLabel("Somme des dépenses sur la période sélectionnée:")
        expenses_title.setAlignment(Qt.AlignCenter)
        self.display_sum_expenses = QLabel("0")
        self.display_sum_expenses.setAlignment(Qt.AlignCenter)

        """
        Afficher le diagramme en bâtons des dépenses par mois
        """
        self.bar_chart = QWidget()

        self.page_layout.addWidget(launch_compute_button)
        self.page_layout.addWidget(self.bar_chart)

    """
    Méthodes
    """

    def plot_barchart(self):
        # retirer l'ancien widget du layout
        self.page_layout.removeWidget(self.bar_chart)
        # mettre à jour le widget avec le bon diagramme
        self.bar_chart = bar_chart.BarChart(depenses=self.depenses,
                                            revenus=self.revenus,
                                            epargne=self.epargne).bar_canvas
        # afficher le nouveau widget
        self.page_layout.addWidget(self.bar_chart)

    """
    Button slot
    """
    @Slot()
    def lancer_calculs(self):
        """
        Cette méthode lance les calculs lors de l'appui sur le bouton
        à condition d'avoir la source de vérité
        En absence de source de vérité, afficher un message et ne rien faire
        """
        # sélection des transactions
        parameters = namedtuple("parameters",
                                ["month_choice",
                                 "year_choice"])
        compute_parameters = parameters(self.month_choice, self.year_choice)
        source_of_truth_found, self.transactions_selectionnees = \
            select_transactions(compute_parameters,
                                self,
                                select_transactions_of_several_months)

        if source_of_truth_found:
            # on ne sélectionne que les dépenses pour tracer les graphes
            self.depenses, self.revenus, self.epargne = \
                extract_expenses_revenus_savings(
                    self.transactions_selectionnees)

            # calculer la somme des dépenses et l'afficher
            sum_expenses = compute_sum(self.transactions_selectionnees)
            self.display_sum_expenses.setNum(sum_expenses)

            # afficher le diagramme en batons des dépenses mensuelles
            self.plot_barchart()
