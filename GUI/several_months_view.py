from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt, Slot

from GUI.parameters_layout import SeveralMonthsParametersWidget
from GUI.source_of_truth import get_source_of_truth
from GUI.bar_chart import BarChart

from Backend.transactions_statistics import compute_sum
from Backend.select_transactions import (
    extract_expenses_revenus_savings,
    select_transactions_of_several_months,
)

import global_variables as GV


class SeveralMonthsView(QWidget):
    """
    Cette classe construit le widget affichant la vue sur plusieurs mois des
    dépenses, revenus ou de l'épargne, tout agrégé sur un diagramme en bâtons
    """

    def __init__(self, parent_widget, transaction_type):
        super().__init__(parent=parent_widget)
        self.transaction_type = transaction_type
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
        """
        parameters_widget = SeveralMonthsParametersWidget(self)
        # récupérer les différents attributs du layout paramètres nécessaires
        # aux calculs ultérieurs
        self.month_choice = parameters_widget.month_selection_combobox
        self.year_choice = parameters_widget.year_selection_combobox
        # ajouter le layout des paramètres au layout principal de la fenetre
        self.page_layout.addWidget(parameters_widget)

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
        self.bar_chart = BarChart(depenses=self.expenses,
                                  revenus=self.revenus,
                                  epargne=self.savings).bar_canvas
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
            nb_month = int(self.month_choice.currentText())
            nb_year = int(self.year_choice.currentText())
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

        # sélection des transactions
        # parameters = namedtuple("parameters",
        #                         ["month_choice",
        #                          "year_choice"])
        # compute_parameters = parameters(self.month_choice, self.year_choice)
        # source_of_truth_found, self.transactions_selectionnees = \
        #     select_transactions(compute_parameters,
        #                         self,
        #                         select_transactions_of_several_months)

        # if source_of_truth_found:
        #     # on ne sélectionne que les dépenses pour tracer les graphes
        #     self.depenses, self.revenus, self.epargne = \
        #         extract_expenses_revenus_savings(
        #             self.transactions_selectionnees)
