from collections import namedtuple

from PySide6.QtWidgets import (
    QLabel, QWidget, QPushButton,
    QVBoxLayout
)
from PySide6.QtCore import Qt, Slot


import GUI.bar_chart as bar_chart

from Backend.transactions_statistics import compute_sum
from Backend.select_transactions import extract_expenses_revenus_savings
from Backend.select_transactions import select_transactions_of_several_months

from GUI.launch_compute import select_transactions
from GUI.parameters_layout import ParametersLayout

# namedtuple permettant d'enregistrer plusieurs paramètres
parameters_tuple = namedtuple("parameters_tuple",
                              ["title",
                               "list",
                               "default_text"]
                              )


class SeveralMonthsWidget(QWidget):
    """
    Cette classe construit le widget affichant les sommes des dépenses, revenus et
    de l'épargne sur plusieurs mois
    """

    def __init__(self):
        super().__init__()
        self.transactions_selectionnees = []
        self.depenses = []
        self.revenus = []
        self.epargne = []

        # Mise en page
        self.page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        self.page_layout.setSpacing(20)

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

        month_period_parameters = parameters_tuple(self.month_period_title,
                                                   self.month_period_list,
                                                   self.month_period_default_text,
                                                   )

        # sélectionner la periode en années
        zero_to_ten_strings = [str(i) for i in range(11)]
        self.year_period_title = "et"
        self.year_period_list = zero_to_ten_strings
        self.year_period_default_text = "0"

        year_period_parameters = parameters_tuple(self.year_period_title,
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
        Ajouter un bouton pour lancer les calculs une fois les paramètres saisis
        par l'utilisateur
        """
        launch_compute_button = QPushButton("Lancer les calculs")
        launch_compute_button.clicked.connect(self.lancer_calculs)
        self.page_layout.addWidget(launch_compute_button)

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
        source_of_truth_found, self.transactions_selectionnees = select_transactions(
            compute_parameters, self, select_transactions_of_several_months)

        if source_of_truth_found:
            # on ne sélectionne que les dépenses pour tracer les graphes
            self.depenses, self.revenus, self.epargne = extract_expenses_revenus_savings(
                self.transactions_selectionnees)

            # calculer la somme des dépenses et l'afficher
            sum_expenses = compute_sum(self.transactions_selectionnees)
            self.display_sum_expenses.setNum(sum_expenses)

            # afficher le diagramme en batons des dépenses mensuelles
            self.plot_barchart()
