from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
)
from PySide6.QtGui import QIcon
import GUI.resources
from PySide6.QtCore import Qt, Slot


class SideMenu(QWidget):
    """
    Cette classe définit le menu latéral à partir duquel l'utilisateur
    choisit ce qu'il souhaite visualiser.
    Le menu latéral contient plusieurs sous-menus:
        - Sous-menu dépenses qui affiche une vue des dépenses par mois et
            sur plusieurs mois
        - Sous-menu revenus qui affiche une vue des revenus par mois et
            sur plusieurs mois
        - Sous-menu patrimoine qui affiche une vue de l'épargne par mois et
            sur plusieurs mois
        - Sous-menu édition qui permet de voir les transactions et les modifier
    Il est prévu de rendre ce menu intéractif (avoir une version repliée du
    menu et une version complète)
    """

    def __init__(self, parent_widget):
        super().__init__(parent_widget)
        side_menu_layout = QVBoxLayout(self)

        # définition des sous-menus
        # définir chaque bouton "auto-exclusive" pour ne pas que 2 sous-menus
        # soient sélectionnés en même temps
        expenses_sub_menu = QPushButton(icon=QIcon(":/icons/expenses.svg"),
                                        text="\t Dépenses")
        expenses_sub_menu.setAutoExclusive(True)
        expenses_sub_menu.setCheckable(True)

        revenus_sub_menu = QPushButton(icon=QIcon(":/icons/money.svg"),
                                       text="\t Revenus")
        revenus_sub_menu.setAutoExclusive(True)
        revenus_sub_menu.setCheckable(True)

        assets_sub_menu = QPushButton(icon=QIcon(":/icons/stocks.svg"),
                                      text="\t Patrimoine")
        assets_sub_menu.setAutoExclusive(True)
        assets_sub_menu.setCheckable(True)

        transactions_sub_menu = QPushButton(icon=QIcon(":/icons/list.svg"),
                                            text="\t Transactions")
        transactions_sub_menu.setAutoExclusive(True)
        transactions_sub_menu.setCheckable(True)

        side_menu_layout.addWidget(expenses_sub_menu)
        side_menu_layout.addWidget(revenus_sub_menu)
        side_menu_layout.addWidget(assets_sub_menu)
        side_menu_layout.addWidget(transactions_sub_menu)

        # aligner le menu en haut à gauche
        side_menu_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # fixer une taille maximale en largeur pour ne pas que les sous-menus
        # paraissent trop étirés horizontalement
        self.setMaximumWidth(300)
