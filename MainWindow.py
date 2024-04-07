from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QTabWidget, QFileDialog
)
from PySide6.QtGui import QAction

from OneMonthExpensesWidget import OneMonthExpensesWidget
from SeveralMonthsExpensesWidget import SeveralMonthsExpensesWidget


class MainWindow(QMainWindow):

    def __init__(self, widget_depenses_one_month, widget_depenses_several_months):
        super().__init__()
        self.setWindowTitle("Mon super logiciel de visualisation des dépenses")

        """
        Création d'une barre de menus avec un deux menus: Fichier et ouvrir
        Le menu Fichier permettra de :
            - ouvrir une nouvelle fenetre
            - quitter l'application
        Le menu Ouvrir permettra de :
            - sélectionner le dossier contenant les fichiers csv de dépenses brutes
            - sélectionner le fichier "source de vérité" contenant les dépenses traitées
        """
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Fichier")
        open_menu = menubar.addMenu("Ouvrir")

        """
        Menu Fichier
        """
        # ouvrir une nouvelle fenetre
        new_window = QAction("Ouvrir une nouvelle fenêtre", self)
        file_menu.addAction(new_window)
        new_window.setShortcut("Ctrl+N")
        # quitter l'application
        exit = file_menu.addAction("Quitter", self.close)
        exit.setShortcut("Ctrl+Q")

        """
        Menu Ouvrir
        """
        # sélectionner le dossier contenant les fichiers csv de dépenses brutes
        select_directory = QAction(
            "Ouvrir un dossier des dépenses brutes", self)
        open_menu.addAction(select_directory)
        select_directory.setShortcut("Ctrl+Shift+O")
        select_directory.triggered.connect(self.open_directory)

        # sélectionner le fichier "source de vérité" contenant les dépenses traitées
        select_source_of_truth = QAction(
            "Sélectionner un fichier des dépenses", self)
        open_menu.addAction(select_source_of_truth)
        select_source_of_truth.setShortcut("Ctrl+O")
        select_source_of_truth.triggered.connect(self.open_source_of_truth)

        """
        Création de plusieurs tabs:
            - dépenses
            - revenus
            - épargne
        """
        tabs = QTabWidget()
        tabs.addTab(widget_depenses_one_month, "Dépenses sur un mois")
        tabs.addTab(widget_depenses_several_months,
                    "Dépenses sur plusieurs mois")
        self.setCentralWidget(tabs)

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
        dialog.setNameFilter("CSV files (*.csv)")
        dialog.exec()


if __name__ == "__main__":
    clean_csv_filename = "/home/thiran/projets_persos/gestion_budget/csv_files/clean_csv_files/source_of_truth.csv"
    app = QApplication([])
    depenses_sur_un_mois = OneMonthExpensesWidget(clean_csv_filename)
    depenses_sur_plusieurs_mois = SeveralMonthsExpensesWidget(
        clean_csv_filename)
    window = MainWindow(depenses_sur_un_mois, depenses_sur_plusieurs_mois)
    window.show()
    app.exec()
