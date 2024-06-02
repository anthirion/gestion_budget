from PySide6.QtWidgets import (
    QLabel, QWidget, QGridLayout
)
from PySide6.QtCore import Qt


class SumsWidget(QWidget):
    """
    Cette classe affiche les sommes des dépenses sur le mois sélectionné:
        - la somme des dépenses par carte
        - la somme des dépenses par virement
    """

    def __init__(self, parent_widget, transaction_type):
        """
        @parameter {str} transaction_type: indique si le widget correspond
            aux dépenses, revenus ou à l'épargne. Le type de transaction
            impacte le titre à afficher
        """
        super().__init__(parent=parent_widget)

        main_layout = QGridLayout(self)

        # adapter les titres en fonction du type de transaction
        match transaction_type:
            case "expenses":
                card_title = "Somme des dépenses par carte :"
                bank_transfer_title = "Somme des dépenses par virement :"
            case "revenus":
                card_title = "Somme des revenus par carte :"
                bank_transfer_title = "Somme des revenus par virement :"
            case "savings":
                card_title = "Somme de l'épargne par carte :"
                bank_transfer_title = "Somme de l'épargne par virement :"
            case _:
                raise ValueError(
                    "Le type de transaction fourni est incorrect")

        # dépenses par carte
        main_layout.addWidget(QLabel(card_title, self), 0, 0, Qt.AlignCenter)
        self.sum_card_spending = QLabel("0", self)
        main_layout.addWidget(self.sum_card_spending, 1, 0, Qt.AlignCenter)
        # self.expenses_label.setAlignment(Qt.AlignCenter)

        # dépenses par virement
        main_layout.addWidget(QLabel(bank_transfer_title, self),
                              0, 1, Qt.AlignCenter)
        self.sum_bank_transfer_spending = QLabel("0", self)
        main_layout.addWidget(
            self.sum_bank_transfer_spending, 1, 1, Qt.AlignCenter)

    def setSums(self, card_sum, bank_transfer_sum):
        """
        @parameter {float} card_sum: sommes des transactions par carte
        @parameter {float} card_bank_transfer: sommes des transactions par
            virement
        Cette méthode écrit les sommes des dépenses, revenus ou de l'épargne
        calculées lorsque l'utilisateur lance les calculs
        """
        self.sum_card_spending.setNum(card_sum)
        self.sum_bank_transfer_spending.setNum(bank_transfer_sum)
