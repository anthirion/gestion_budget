from PySide6.QtWidgets import (
    QMainWindow, QApplication, QFileDialog,
    QTabWidget
)
from PySide6.QtGui import QAction

from ExpensesWidget import ExpensesWidget
from RevenuesWidget import RevenuesWidget


class MainWindow(QMainWindow):

    def __init__(self, widget_depenses, widget_revenus):
        super().__init__()
        self.setWindowTitle("Mon super logiciel de visualisation des dépenses")

        """
        Création d'une barre de menus avec un seul menu Fichier
        Le menu permettra de :
            - sélectionner le dossier contenant les fichiers csv de dépenses brutes
            - sélectionner le fichier "source de vérité" contenant les dépenses traitées
            - quitter l'application
        """
        menu = self.menuBar()
        file_menu = menu.addMenu("Fichier")
        open_menu = menu.addMenu("Ouvrir")

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

        # ouvrir une nouvelle fenetre
        new_window = QAction("Ouvrir une nouvelle fenêtre", self)
        file_menu.addAction(new_window)
        new_window.setShortcut("Ctrl+N")
        # quitter l'application
        exit = file_menu.addAction("Quitter", self.close)
        exit.setShortcut("Ctrl+Q")

        """
        Création de plusieurs tabs:
            - dépenses
            - revenus
            - épargne
        """
        tabs = QTabWidget()
        tabs.addTab(widget_depenses, "Dépenses")
        tabs.addTab(widget_revenus, "Revenus")
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
    app = QApplication()
    expenses_widget = ExpensesWidget(clean_csv_filename)
    revenues_widget = RevenuesWidget()
    window = MainWindow(expenses_widget, revenues_widget)
    window.show()
    app.exec()
