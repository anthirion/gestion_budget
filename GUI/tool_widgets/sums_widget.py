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

        # définition des paramètres
        card_title = "Somme des dépenses par carte :"
        bank_transfer_title = "Somme des dépenses par virement :"

        # dépenses par carte
        main_layout.addWidget(QLabel(card_title), 0, 0, Qt.AlignCenter)
        self.sum_card_spending = QLabel("0")
        main_layout.addWidget(self.sum_card_spending, 1, 0, Qt.AlignCenter)
        # self.expenses_label.setAlignment(Qt.AlignCenter)

        # dépenses par virement
        main_layout.addWidget(QLabel(bank_transfer_title),
                              0, 1, Qt.AlignCenter)
        self.sum_bank_transfer_spending = QLabel("0")
        main_layout.addWidget(
            self.sum_bank_transfer_spending, 1, 1, Qt.AlignCenter)


# class SumsLayout(QLayout):
#     def __init__(self):
#         """"
#         Cette classe définit deux layouts affichant des sommes de dépenses sur le mois sélectionné:
#             - la somme des dépenses par carte
#             - la somme des dépenses par virement

#         """
#         super().__init__()

#         self.sums_layout = QHBoxLayout()

#         # ajout d'un widget affichant la somme des dépenses par carte
#         card_title = "Somme des dépenses par carte sur le mois sélectionné:"
#         card_sum = SumLayout(card_title)
#         self.card_expenses_label = card_sum.expenses_label
#         card_sum_layout = card_sum.sum_layout
#         # ajout d'un widget affichant la somme des dépenses par virement

#         # définition du titre et label pour les dépenses par virement
#         bank_transfer_title = "Somme des dépenses par virement sur le mois sélectionné:"
#         bank_transfer_sum = SumLayout(bank_transfer_title)
#         self.bank_transfer_expenses_label = bank_transfer_sum.expenses_label
#         bank_transfer_sum_layout = bank_transfer_sum.sum_layout

#         # ajout des widgets de sommes au layout
#         self.sums_layout.addLayout(card_sum_layout)
#         self.sums_layout.addLayout(bank_transfer_sum_layout)
