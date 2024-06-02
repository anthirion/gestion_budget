from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton
)
from PySide6.QtGui import QIcon
from GUI.resources import (
    expenses_icon,
    list_icon,
    money_icon,
    stocks_icon,
    overview_icon,
)
from PySide6.QtCore import Qt, Slot

###############################################################################
# On associe un index à chaque sous-menu
###############################################################################

expenses_widget_index = 1
revenus_widget_index = 2
assets_widget_index = 3
overview_widget_index = 4
transactions_widget_index = 5

###############################################################################
# Classe principale du module
###############################################################################


class SideMenu(QWidget):
    """
    Cette classe définit le menu latéral à partir duquel l'utilisateur
    choisit ce qu'il souhaite visualiser.
    Le menu latéral contient plusieurs sous-menus:
        - Sous-menu Dépenses qui affiche une vue des dépenses par mois
        - Sous-menu Revenus qui affiche une vue des revenus par mois
        - Sous-menu Patrimoine qui affiche une vue de l'épargne par mois
        - Sous-menu Transactions qui permet de voir les transactions et de les
            modifier
        - Sous-menu Synthèse qui affiche les dépenses, revenus et épargne sur
        plusieurs mois, aggrégés en un seul diagramme en bâtons
    Il est prévu de rendre ce menu intéractif (avoir une version repliée du
    menu et une version complète)
    """

    def __init__(self, parent_widget):
        super().__init__(parent_widget)
        # ce widget sert à afficher la bonne vue en fonction du sous-menu
        # sélectionné depuis le menu latéral
        self.parent_main_widget = parent_widget.main_widget

        side_menu_layout = QVBoxLayout(self)

        """
        Définition des sous-menus
        """
        expenses_sub_menu = QPushButton(icon=QIcon(expenses_icon),
                                        text="\t Dépenses")
        expenses_sub_menu.clicked.connect(self.expenses_selected)

        revenus_sub_menu = QPushButton(icon=QIcon(money_icon),
                                       text="\t Revenus")
        revenus_sub_menu.clicked.connect(self.revenus_selected)

        assets_sub_menu = QPushButton(icon=QIcon(stocks_icon),
                                      text="\t Patrimoine")
        assets_sub_menu.clicked.connect(self.assets_selected)

        transactions_sub_menu = QPushButton(icon=QIcon(list_icon),
                                            text="\t Transactions")
        transactions_sub_menu.clicked.connect(self.transactions_selected)
        overview_sub_menu = QPushButton(icon=QIcon(overview_icon),
                                        text="\t Synthèse")
        overview_sub_menu.clicked.connect(self.overview_selected)

        # définir chaque bouton "auto-exclusive" pour ne pas que 2 sous-menus
        # soient sélectionnés en même temps
        # et rendre chaque bouton "checkable" pour que l'utilisateur sache quel
        # sous-menu est sélectionné
        sub_menus = [expenses_sub_menu, revenus_sub_menu,
                     assets_sub_menu, transactions_sub_menu,
                     overview_sub_menu]

        for sub_menu in sub_menus:
            sub_menu.setAutoExclusive(True)
            sub_menu.setCheckable(True)

        # ATTENTION: l'ordre est important !!!!
        side_menu_layout.addWidget(expenses_sub_menu)
        side_menu_layout.addWidget(revenus_sub_menu)
        side_menu_layout.addWidget(assets_sub_menu)
        side_menu_layout.addWidget(overview_sub_menu)
        side_menu_layout.addWidget(transactions_sub_menu)

        # aligner le menu en haut à gauche
        side_menu_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # fixer une taille maximale en largeur pour ne pas que les sous-menus
        # paraissent trop étirés horizontalement
        # self.setMaximumWidth(300)

    """
    Buttons Slots
    """
    @Slot()
    def expenses_selected(self):
        """
        Lorsque le sous-menu dépenses est sélectionné, afficher la vue des
        dépenses
        """
        self.parent_main_widget.setCurrentIndex(expenses_widget_index)

    @Slot()
    def revenus_selected(self):
        """
        Lorsque le sous-menu revenus est sélectionné, afficher la vue des
        revenus
        """
        self.parent_main_widget.setCurrentIndex(revenus_widget_index)

    @Slot()
    def assets_selected(self):
        """
        Lorsque le sous-menu patrimoine est sélectionné, afficher la vue du
        patrimoine
        """
        self.parent_main_widget.setCurrentIndex(assets_widget_index)

    @Slot()
    def transactions_selected(self):
        """
        Lorsque le sous-menu transactions est sélectionné, afficher la vue des
        transactions
        """
        self.parent_main_widget.setCurrentIndex(transactions_widget_index)

    @Slot()
    def overview_selected(self):
        """
        Lorsque le sous-menu Synthèse est sélectionné, afficher la vue des
        de la sytnhèse
        """
        self.parent_main_widget.setCurrentIndex(overview_widget_index)
