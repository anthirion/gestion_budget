from PySide6.QtWidgets import (
    QLabel, QLayout, QHBoxLayout, QVBoxLayout
)
from PySide6.QtCore import Qt


class SumLayout(QLayout):
    """
    Cette classe définit un layout affichant la somme de dépenses sur le mois sélectionné
    Le type de la somme (par carte ou virement) est défini par le titre passé au constructeur 
    """

    def __init__(self, layout_title):
        super().__init__()
        self.title = layout_title

        # définition du titre et label pour les dépenses
        self.sum_layout = QVBoxLayout()
        title = QLabel(self.title)
        title.setAlignment(Qt.AlignCenter)
        self.expenses_label = QLabel()
        self.expenses_label.setAlignment(Qt.AlignCenter)

        # ajout des widgets précédents au layout
        self.sum_layout.addWidget(title)
        self.sum_layout.addWidget(self.expenses_label)


class SumsLayout(QLayout):
    def __init__(self):
        """"
        Cette classe définit deux layouts affichant des sommes de dépenses sur le mois sélectionné:
            - la somme des dépenses par carte
            - la somme des dépenses par virement

        """
        super().__init__()

        self.sums_layout = QHBoxLayout()

        # ajout d'un widget affichant la somme des dépenses par carte
        card_title = "Somme des dépenses par carte sur le mois sélectionné:"
        card_sum = SumLayout(card_title)
        self.card_expenses_label = card_sum.expenses_label
        card_sum_layout = card_sum.sum_layout
        # ajout d'un widget affichant la somme des dépenses par virement

        # définition du titre et label pour les dépenses par virement
        bank_transfer_title = "Somme des dépenses par virement sur le mois sélectionné:"
        bank_transfer_sum = SumLayout(bank_transfer_title)
        self.bank_transfer_expenses_label = bank_transfer_sum.expenses_label
        bank_transfer_sum_layout = bank_transfer_sum.sum_layout

        # ajout des widgets de sommes au layout
        self.sums_layout.addLayout(card_sum_layout)
        self.sums_layout.addLayout(bank_transfer_sum_layout)
