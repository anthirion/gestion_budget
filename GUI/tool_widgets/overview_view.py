from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox
)
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import Slot

from GUI.tool_widgets.parameters_widget import OverviewSubMenuParametersWidget
from GUI.source_of_truth import (
    get_source_of_truth,
    get_transactions,
)
from GUI.tool_widgets.bar_chart_widget import BarChartWidget
from GUI.tool_widgets.sums_widget import OverviewSumWidget

from Backend.transactions_statistics import compute_sum
from Backend.select_transactions import (
    extract_expenses_revenus_savings,
    select_several_months_transactions,
)

import global_variables as GV


class OverviewWidget(QWidget):
    """
    Cette classe construit le widget affichant la vue de synthèse à la
    sélection du sous-menu correspondant dans le menu latéral.
    Ce widget affiche un aggrégat des dépenses, revenus et de l'épargne sur
    plusieurs mois sous la forme d'un diagramme en bâtons.
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        self.selected_operations = []
        self.expenses, self.revenus, self.savings = [], [], []

        # Mise en page
        self.page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        self.page_layout.setSpacing(GV.vertical_spacing)

        """
        Le premier widget permet à l'utilisateur de sélectionner
        les paramètres de calcul:
            - la période sur laquelle faire l'analyse (en mois et années) et
            - la ou les banque(s) sélectionnée(s)
        Ce widget est différent de celui utilisé par la vue sur un mois.
        """
        self.parameters_widget = OverviewSubMenuParametersWidget(self)
        self.page_layout.addWidget(self.parameters_widget)

        """
        Ajouter un bouton pour lancer les calculs une fois les paramètres
        saisis par l'utilisateur
        """
        launch_compute_button = QPushButton("Lancer les calculs", self)
        launch_compute_button.clicked.connect(self.lancer_calculs)
        self.page_layout.addWidget(launch_compute_button)

        """"
        Afficher la somme des dépenses, des revenus et de l'épargne sur
        la période sélectionnée
        """
        self.sums = OverviewSumWidget(self)
        self.page_layout.addWidget(self.sums)

        """
        Afficher le diagramme en bâtons des dépenses par mois
        """
        self.bar_canvas = FigureCanvas(Figure(figsize=(6, 8)))
        self.bar_axes = self.bar_canvas.figure.subplots()

        self.page_layout.addWidget(launch_compute_button)
        self.page_layout.addWidget(self.bar_canvas)

    """
    Méthodes
    """

    def plot_barchart(self):
        # effacer les anciens axes pour éviter le chevauchement
        # des anciens et nouveaux axes
        self.bar_axes.clear()
        # calculer le nouveau diagramme en batons
        BarChartWidget(self)
        # afficher le nouveau diagramme en batons
        self.bar_canvas.draw()

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
        # recherche de la source de vérité
        GV.source_of_truth = get_source_of_truth(self)
        if GV.source_of_truth:
            transactions = get_transactions()
            nb_month, nb_year = self.parameters_widget.get_period()
            self.selected_operations = \
                select_several_months_transactions(transactions,
                                                   n_month=nb_month,
                                                   n_year=nb_year)
            if not self.selected_operations:
                # pas de transaction sélectionnée
                # afficher un message d'avertissement à l'utilisateur
                QMessageBox.warning(self, "Avertissement",
                                    GV.no_transaction_found_msg)

            self.expenses, self.revenus, self.savings = \
                extract_expenses_revenus_savings(self.selected_operations)

            # calculer la somme des dépenses, revenus et de l'épargne et les
            # afficher
            expenses_sum = compute_sum(self.expenses)
            revenus_sum = compute_sum(self.revenus)
            savings_sum = compute_sum(self.savings)
            self.sums.setSums(expenses_sum, revenus_sum, savings_sum)

            # afficher le diagramme en batons des dépenses mensuelles
            self.plot_barchart()
