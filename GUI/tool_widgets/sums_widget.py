from PySide6.QtWidgets import (
    QLabel, QWidget, QGridLayout
)
from PySide6.QtCore import Qt


class SubMenuSumsWidget(QWidget):
    """
    Cette classe affiche les sommes des dépenses, revenus ou transactions (en
    fonction du sous-menu sélectionné) du mois sélectionné sur la vue des
    sous-menus dépenses, revenus et épargne. Il affiche 2 types de sommes :
        - la somme des transactions (dépenses, revenus ou épargne) par carte
        - la somme des transactions (dépenses, revenus ou épargne) par virement
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
        main_layout.addWidget(QLabel(card_title, self), 1, 1,
                              Qt.AlignmentFlag.AlignCenter)
        self.sum_card_spending = QLabel("0", self)
        main_layout.addWidget(self.sum_card_spending, 2, 1,
                              Qt.AlignmentFlag.AlignCenter)

        # dépenses par virement
        main_layout.addWidget(QLabel(bank_transfer_title, self),
                              1, 2, Qt.AlignmentFlag.AlignCenter)
        self.sum_bank_transfer_spending = QLabel("0", self)
        main_layout.addWidget(
            self.sum_bank_transfer_spending, 2, 2,
            Qt.AlignmentFlag.AlignCenter)

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


class OverviewSumWidget(QWidget):
    """
    Cette classe affiche les sommes des dépenses, revenus et épargne de
    plusieurs mois. Ces sommes sont affichées dans le sous-menu Synthèse.
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        main_layout = QGridLayout(self)

        expenses_title = "Somme des dépenses sur la période :"
        revenus_title = "Somme des revenus sur la période :"
        savings_title = "Somme de l'épargne sur la période :"

        # dépenses
        main_layout.addWidget(QLabel(expenses_title, self), 1, 1,
                              Qt.AlignmentFlag.AlignCenter)
        self.expenses_sum = QLabel("0", self)
        main_layout.addWidget(self.expenses_sum, 2, 1,
                              Qt.AlignmentFlag.AlignCenter)

        # revenus
        main_layout.addWidget(QLabel(revenus_title, self), 1, 2,
                              Qt.AlignmentFlag.AlignCenter)
        self.revenus_sum = QLabel("0", self)
        main_layout.addWidget(self.revenus_sum, 2, 2,
                              Qt.AlignmentFlag.AlignCenter)

        # épargne
        main_layout.addWidget(QLabel(savings_title, self), 1, 3,
                              Qt.AlignmentFlag.AlignCenter)
        self.savings_sum = QLabel("0", self)
        main_layout.addWidget(self.savings_sum, 2, 3,
                              Qt.AlignmentFlag.AlignCenter)

    def setSums(self, expenses_sum, revenus_sum, savings_sum):
        """
        @parameter {float} expenses_sum: sommes des dépenses
        @parameter {float} revenus_sum: sommes des revenus
        @parameter {float} savings_sum: sommes de l'épargne
        Cette méthode écrit les sommes des dépenses, revenus et de l'épargne
        dans les labels définis ci-dessus
        """
        self.expenses_sum.setNum(expenses_sum)
        self.revenus_sum.setNum(revenus_sum)
        self.savings_sum.setNum(savings_sum)
