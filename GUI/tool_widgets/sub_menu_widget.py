from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
)
from PySide6.QtCore import Slot

from GUI.tool_widgets.parameters_widget import SubMenuParametersWidget
from GUI.tool_widgets.sums_widget import SumsWidget
from GUI.tool_widgets.pie_chart_widget import PieChartWidget
from GUI.source_of_truth import get_source_of_truth

from Backend.transactions_statistics import compute_sum
from Backend.select_transactions import (
    select_transactions_by_card,
    select_transactions_by_bank_transfer,
    extract_expenses_revenus_savings,
    select_transactions_of_one_month,
)

import global_variables as GV


class SubMenuWidget(QWidget):
    """
    Cette classe construit le widget affiché à la sélection des sous-menus
    dépenses, revenus ou épargne, sélectionnés depuis le menu latéral.
    Ce widget affiche la vue sur un seul mois des transactions, les
    transactions pouvant être des dépenses, revenus ou de l'épargne en
    fonction du sous-menu sélectionné depuis le menu latéral.
    Les transactions mensuelles sont affichées sous forme de 2 camemberts
    (un pour les transactions par carte et un pour les transactions par
    virement). Ces camemberts regroupent les transactions par catégorie.
    """

    def __init__(self, parent_widget, transaction_type):
        """
        @parameter {str} transaction_type: indique si la vue à afficher
            concerne les dépenses, les revenus ou l'épargne
        Cette classe construit le widget contenant:
            - un widget de sélection des paramètres (période de calcul
                et banque)
            - un bouton permettant de lancer les calculs
            - les sommes des dépenses mensuelles par carte et par virement
            - des camemberts représentant les dépenses mensuelles par carte
                et par virement, rangées par catégories de dépenses
                (alimentation, assurance, etc)
        """
        super().__init__(parent=parent_widget)
        self.transaction_type = transaction_type
        self.selected_operations = []
        self.transactions, self.card_transactions = [], []
        self.bank_transfer_transactions = []
        self.expenses, self.revenus, self.savings = [], [], []

        # Mise en page
        self.page_layout = QVBoxLayout(self)
        # ajouter un espace entre les éléments du layout
        self.page_layout.setSpacing(GV.vertical_spacing)

        """
        Le premier widget permet à l'utilisateur de sélectionner
        les paramètres de calcul:
            - le mois et l'année sur lesquels faire l'analyse et
            - la ou les banque(s) sélectionnée(s)
        Ce widget est différent de celui utilisé par la vue sur plusieurs mois.
        """
        self.parameters_widget = SubMenuParametersWidget(self)
        self.page_layout.addWidget(self.parameters_widget)

        """
        Ajouter un bouton pour lancer les calculs une fois les paramètres
        saisis par l'utilisateur
        """
        launch_compute_button = QPushButton("Lancer les calculs", self)
        launch_compute_button.clicked.connect(self.lancer_calculs)
        self.page_layout.addWidget(launch_compute_button)

        """
        Ajouter un layout affichant les sommes des dépenses mensuelles
        par carte et par virement
        """
        self.sums_widget = SumsWidget(self, self.transaction_type)
        self.page_layout.addWidget(self.sums_widget)

        """
        Afficher un camembert des dépenses par carte avec les catégories de
        dépenses et leur montant associé ainsi qu'un camembert des dépenses
        par virement
        """
        pies_layout = QHBoxLayout()
        self.pie_card = PieChartWidget(self,
                                       GV.card_chart_title)

        self.pie_bank_transfer = \
            PieChartWidget(self,
                           GV.bank_transfer_chart_title)

        # ajouter le layout des camemberts au layout principal de la fenetre
        pies_layout.addWidget(self.pie_card)
        pies_layout.addWidget(self.pie_bank_transfer)
        self.page_layout.addLayout(pies_layout)

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
                select_transactions_of_one_month(transactions,
                                                 n_month=nb_month,
                                                 n_year=nb_year)
            if not self.selected_operations:
                # pas de transaction sélectionnée
                # afficher un message d'avertissement à l'utilisateur
                QMessageBox.warning(self, "Avertissement",
                                    GV.no_transaction_found_msg)

            self.expenses, self.revenus, self.savings = \
                extract_expenses_revenus_savings(self.selected_operations)

            match self.transaction_type:
                case "expenses":
                    # les camemberts à afficher sont ceux des dépenses
                    self.transactions = self.expenses
                case "revenus":
                    # les camemberts à afficher sont ceux des revenus
                    self.transactions = self.revenus
                case "savings":
                    # les camemberts à afficher sont ceux de l'épargne
                    self.transactions = self.savings
                case _:
                    raise ValueError(
                        "Le type de transaction fourni est incorrect")

            # on extrait les transactions par carte
            self.card_transactions = \
                select_transactions_by_card(self.transactions)
            # on extrait les transactions par virement
            self.bank_transfer_transactions = \
                select_transactions_by_bank_transfer(self.transactions)

            # calculer la somme des transactions par carte et par virement
            # et les afficher dans le widget SumsWidget
            sum_card = compute_sum(self.card_transactions)
            sum_bank_transfer = compute_sum(self.bank_transfer_transactions)
            self.sums_widget.setSums(sum_card, sum_bank_transfer)

            # décocher les checkbox associées à chaque graphe
            for pie in (self.pie_card, self.pie_bank_transfer):
                pie.setCheckboxToFalse()

            # mettre à jour les camemberts de dépenses par carte et virement
            self.pie_card.update_pie_chart(self.card_transactions,
                                           condenser_value=False)
            self.pie_bank_transfer\
                .update_pie_chart(self.bank_transfer_transactions,
                                  condenser_value=False)
