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

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)

        main_layout = QGridLayout(self)

        card_title = "Somme des dépenses par carte :"
        bank_transfer_title = "Somme des dépenses par virement :"

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
