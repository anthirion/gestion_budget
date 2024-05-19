from GUI.one_month_widget import OneMonthWidget
from GUI.several_months_widget import SeveralMonthsWidget
from GUI.menu_bar import MenuBar

from PySide6.QtWidgets import (
    QMainWindow, QLabel, QHBoxLayout, QWidget
)
from PySide6.QtCore import Qt
from GUI.side_menu import SideMenu


class MainWindow(QMainWindow):
    """
    Cette classe définit la fenêtre principale de l'app
    """

    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle("VisuDépenses")

            # self.widget_one_month = OneMonthWidget()
            # self.widget_several_months = SeveralMonthsWidget()

            # barre de menus
            MenuBar(parent=self)

            main_widget = QWidget(self)
            page_layout = QHBoxLayout(main_widget)

            """
            Création d'un menu latéral avec plusieurs sous-menus:
                - Dépenses
                - Revenus
                - Patrimoine
                - Transactions
            """
            side_menu_widget = SideMenu(self)
            page_layout.addWidget(side_menu_widget)

            """
            Création de plusieurs tabs:
                - dépenses
                - revenus
                - épargne
            """
            # tabs = QTabWidget()
            # tabs.addTab(self.widget_one_month, "Dépenses sur un mois")
            # tabs.addTab(self.widget_several_months,
            #             "Statistiques sur plusieurs mois")
            # self.setCentralWidget(tabs)

            label = QLabel("Bienvenue sur ma super app")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            page_layout.addWidget(label)

            self.setCentralWidget(main_widget)

        except Exception as e:
            # QMessageBox.critical(self, "Critical error", e)
            print(type(e), e)
