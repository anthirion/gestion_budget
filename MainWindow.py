from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar, QCheckBox,
    QFileDialog, QHBoxLayout, QVBoxLayout
)
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from PySide6.QtCharts import QChartView, QPieSeries, QChart

from pathlib import Path
from MonthExpensesWidget import MonthExpensesWidget


class MainWindow(QMainWindow):
    def __init__(self, widget):
        super().__init__()
        self.setWindowTitle("Mon super logiciel de visualisation des dépenses")

        """
        Création d'une barre de menus avec un seul menu: Fichier
        Le menu permettra de :
            - sélectionner le dossier contenant les fichiers csv de dépenses brutes
            - sélectionner le fichier "source de vérité" contenant les dépenses traitées
            - quitter l'application
        """
        # création de la barre de menus avec un seul menu Fichier
        menu = self.menuBar()
        file_menu = menu.addMenu("Fichier")
        # création des actions dans le menu fichier
        # action de sélectionner le dossier contenant les fichiers csv de dépenses brutes
        # select_directory = QAction(
        #     "Sélectionner un dossier des dépenses brutes")
        # select_directory.setStatusTip("Opening directory")
        # select_directory.triggered.connect(self.open_directory)
        # # action de sélectionner le fichier "source de vérité" contenant les dépenses traitées
        # select_source_of_truth = QAction(
        #     "Sélectionner un fichier des dépenses")
        # select_source_of_truth.setStatusTip("Opening source of truth file")
        # select_source_of_truth.triggered.connect(self.open_source_of_truth)
        # action de quitter l'application
        exit = file_menu.addAction("Exit", self.close)
        exit.setShortcut("Ctrl+Q")

        """
        Fonction qui gère l'importation d'un dossier de dépenses brutes
        """

        # def open_directory(self):
        #     dialog = QFileDialog(self)
        #     dialog.setFileMode(QFileDialog.Directory)
        #     dialog.exec()

        # def open_directory(self):
        #     dialog = QFileDialog(self)
        #     dialog.setFileMode(QFileDialog.Directory)
        #     dialog.exec()

        """
        Fonction qui gère l'importation d'un fichier de dépenses traité (source de vérité)
        """
        self.setCentralWidget(widget)


if __name__ == "__main__":
    app = QApplication()
    expenses_widget = MonthExpensesWidget()
    window = MainWindow(expenses_widget)
    window.show()
    app.exec()
