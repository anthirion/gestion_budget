from PySide6.QtWidgets import (
    QLabel, QLayout, QHBoxLayout, QVBoxLayout
)
from PySide6.QtCore import Qt


class SumsLayout(QLayout):
    def __init__(self):
        """"
        Afficher la somme des dépenses par carte et par virement
        sur le mois sélectionné
        """
        super().__init__()

        self.sums_layout = QHBoxLayout()
        card_sum_layout = QVBoxLayout()
        # définition du titre et label pour les dépenses par carte
        card_title = QLabel(
            "Somme des dépenses par carte sur le mois sélectionné:")
        card_title.setAlignment(Qt.AlignCenter)
        self.sum_card_expenses_label = QLabel()
        self.sum_card_expenses_label.setAlignment(Qt.AlignCenter)
        card_sum_layout.addWidget(card_title)
        card_sum_layout.addWidget(self.sum_card_expenses_label)

        bank_transfer_sum_layout = QVBoxLayout()
        # définition du titre et label pour les dépenses par virement
        bank_transfer_title = QLabel(
            "Somme des dépenses par virement sur le mois sélectionné:")
        bank_transfer_title.setAlignment(Qt.AlignCenter)
        self.sum_bank_transfer_expenses_label = QLabel()
        self.sum_bank_transfer_expenses_label.setAlignment(Qt.AlignCenter)
        bank_transfer_sum_layout.addWidget(bank_transfer_title)
        bank_transfer_sum_layout.addWidget(
            self.sum_bank_transfer_expenses_label)

        # affichage des widgets précédemment définis
        self.sums_layout.addLayout(card_sum_layout)
        self.sums_layout.addLayout(bank_transfer_sum_layout)
