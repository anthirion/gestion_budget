from GUI.tool_widgets.sub_menu_widget import SubMenuWidget
from GUI.menu_bar import MenuBar

from PySide6.QtWidgets import (
    QMainWindow, QHBoxLayout, QWidget, QLabel,
    QStackedWidget
)
from PySide6.QtCore import Qt
from GUI.side_menu import SideMenu


class MainWindow(QMainWindow):
    """
    Cette classe définit la fenêtre principale de l'app
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("VisuDépenses")

        # affichage de la barre de menus
        MenuBar(parent=self)

        app_widget = QWidget(self)
        app_layout = QHBoxLayout(app_widget)

        """
        Définition du widget principal (à côté du menu latéral)
        Ce widget superpose plusieurs widgets:
            - widget d'accueil (home_widget) qui s'affiche au démarrage
                de l'app
            - les widgets correspondant aux sous-menus
        """
        # widget principal
        self.main_widget = QStackedWidget(app_widget)

        # widget d'accueil
        home_widget = \
            QLabel("Bienvenue sur l'app de visualisation de budget !\n\
                    Sélectionner un menu à gauche pour commencer !")
        home_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # widget du sous-menu des dépenses
        expenses_widget = SubMenuWidget(self.main_widget,
                                        sub_menu="expenses")
        # widget du sous-menu des revenus
        revenus_widget = SubMenuWidget(self.main_widget,
                                       sub_menu="revenus")
        # widget du sous-menu patrimoine
        savings_widget = SubMenuWidget(self.main_widget,
                                       sub_menu="savings")
        # widget du sous-menu des transactions
        transactions_widget = \
            QLabel("Bienvenue sur la vue des transactions")
        transactions_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ATTENTION: l'ordre est important !!!!
        self.main_widget.addWidget(home_widget)
        self.main_widget.addWidget(expenses_widget)
        self.main_widget.addWidget(revenus_widget)
        self.main_widget.addWidget(savings_widget)
        self.main_widget.addWidget(transactions_widget)

        """
        Création d'un menu latéral avec plusieurs sous-menus:
            - Dépenses
            - Revenus
            - Patrimoine
            - Transactions
        """
        side_menu_widget = SideMenu(self)

        # disposition des widgets précédemment définis
        app_layout.addWidget(side_menu_widget)
        app_layout.addWidget(self.main_widget)

        self.setCentralWidget(app_widget)
