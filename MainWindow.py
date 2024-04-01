from PySide6.QtWidgets import (
    QMainWindow, QApplication, QFileDialog
)
from PySide6.QtGui import QAction

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
        menu = self.menuBar()
        file_menu = menu.addMenu("Fichier")

        # action de sélectionner le dossier contenant les fichiers csv de dépenses brutes
        select_directory = QAction(
            "Ouvrir un dossier des dépenses brutes", self)
        file_menu.addAction(select_directory)
        select_directory.triggered.connect(self.open_directory)

        # action de sélectionner le fichier "source de vérité" contenant les dépenses traitées
        select_source_of_truth = QAction(
            "Sélectionner un fichier des dépenses", self)
        file_menu.addAction(select_source_of_truth)
        select_source_of_truth.triggered.connect(self.open_source_of_truth)

        # action de quitter l'application
        exit = file_menu.addAction("Exit", self.close)
        exit.setShortcut("Ctrl+Q")

        # centralise le widget passé en paramètre
        self.setCentralWidget(widget)

    """
    Slots associés à la barre de menus
    """

    def open_directory(self):
        """
        Gère l'importation d'un dossier contenant les dépenses brutes
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.exec()

    def open_source_of_truth(self):
        """
        Gère l'importation d'un fichier de dépenses traité (source de vérité)
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter(tr("Images (*.png *.xpm *.jpg)"))
        dialog.exec()


if __name__ == "__main__":
    app = QApplication()
    expenses_widget = MonthExpensesWidget()
    window = MainWindow(expenses_widget)
    window.show()
    app.exec()
