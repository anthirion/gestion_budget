from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt, Slot

from GUI.tool_widgets.parameters_widget import SynthesisSubMenuParametersWidget
from GUI.source_of_truth import get_source_of_truth
from GUI.tool_widgets.bar_chart_widget import BarChartWidget

from Backend.transactions_statistics import compute_sum
from Backend.select_transactions import (
    extract_expenses_revenus_savings,
    select_transactions_of_several_months,
)

import global_variables as GV


class OverviewWidget(QWidget):
    """
    Cette classe construit le widget affichant la vue de sytnhèse à la
    sélection du sous-menu correspondant dans le menu latéral.
    Ce widget affiche un aggrégat des dépenses, revenus et de l'épargne sur
    plusieurs mois sous la forme d'un diagramme en bâtons.
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        self.selected_operations = []
        self.transactions, self.transactions_card = [], []
        self.transactions_bank_transfer = []
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
        self.parameters_widget = SynthesisSubMenuParametersWidget(self)
        self.page_layout.addWidget(self.parameters_widget)

        """
        Ajouter un bouton pour lancer les calculs une fois les paramètres
        saisis par l'utilisateur
        """
        launch_compute_button = QPushButton("Lancer les calculs", self)
        launch_compute_button.clicked.connect(self.lancer_calculs)
        self.page_layout.addWidget(launch_compute_button)

        """"
        Afficher la somme des dépenses et des revenus sur la période
        sélectionnée
        """
        expenses_title = \
            QLabel("Somme des dépenses sur la période sélectionnée:", self)
        expenses_title.setAlignment(Qt.AlignCenter)
        self.display_sum_expenses = QLabel("0", self)
        self.display_sum_expenses.setAlignment(Qt.AlignCenter)

        """
        Afficher le diagramme en bâtons des dépenses par mois
        """
        self.bar_chart = QWidget(self)

        self.page_layout.addWidget(launch_compute_button)
        self.page_layout.addWidget(self.bar_chart)

    """
    Méthodes
    """

    def plot_barchart(self):
        # retirer l'ancien graphe pour en dessiner un nouveau
        self.page_layout.removeWidget(self.bar_chart)
        # mettre à jour le widget avec le bon diagramme
        self.bar_chart = BarChartWidget(self).bar_canvas
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
        # recherche de la source de vérité
        GV.source_of_truth = get_source_of_truth(self)
        if GV.source_of_truth:
            # sélection des transactions
            source_of_truth_path = Path(GV.source_of_truth)
            # sélectionner les transactions souhaitées par l'utilisateur
            transactions = source_of_truth_path.read_text(encoding="utf-8-sig")
            # on split le fichier par transaction
            transactions = transactions.split(("\n"))
            # on retire la première ligne qui correspond aux colonnes
            # et la dernière transaction qui est vide
            transactions = transactions[1:-1]
            nb_month, nb_year = self.parameters_widget.get_period()
            self.selected_operations = \
                select_transactions_of_several_months(transactions,
                                                      n_month=nb_month,
                                                      n_year=nb_year)
            if not self.selected_operations:
                # pas de transaction sélectionnée
                # afficher un message d'avertissement à l'utilisateur
                QMessageBox.warning(self, "Avertissement",
                                    GV.no_transaction_found_msg)

            self.expenses, self.revenus, self.savings = \
                extract_expenses_revenus_savings(self.selected_operations)

            # calculer la somme des dépenses et l'afficher
            sum_expenses = compute_sum(self.selected_operations)
            self.display_sum_expenses.setNum(sum_expenses)

            # afficher le diagramme en batons des dépenses mensuelles
            self.plot_barchart()
