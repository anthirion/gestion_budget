from GUI.one_month_widget import OneMonthWidget
from GUI.several_months_widget import SeveralMonthsWidget
from GUI.menu_bar import MenuBar

from PySide6.QtWidgets import (
    QMainWindow, QTabWidget
)


class MainWindow(QMainWindow):

    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle(
                "Mon super logiciel de visualisation des dépenses")

            self.widget_one_month = OneMonthWidget()
            self.widget_several_months = SeveralMonthsWidget()

            # barre de menus
            MenuBar(parent=self)

            """
            Création de plusieurs tabs:
                - dépenses
                - revenus
                - épargne
            """
            tabs = QTabWidget()
            tabs.addTab(self.widget_one_month, "Dépenses sur un mois")
            tabs.addTab(self.widget_several_months,
                        "Statistiques sur plusieurs mois")
            # placer les onglets sur la gauche
            tabs.setTabPosition(QTabWidget.West)
            self.setCentralWidget(tabs)

        except Exception as e:
            # QMessageBox.critical(self, "Critical error", e)
            print(type(e), e)
