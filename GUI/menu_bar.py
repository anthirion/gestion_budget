from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMenuBar, QFileDialog, QMessageBox
)

import global_variables
from Backend.create_unique_csv import create_source_of_truth
from GUI.source_of_truth import (
    save_source_of_truth
)


class MenuBar(QMenuBar):
    """
    Création d'une barre de menus avec deux menus: Fichier et Ouvrir.
    Le menu Fichier permettra de :
        - ouvrir une nouvelle fenetre
        - quitter l'application
    Le menu Ouvrir permettra de :
        - sélectionner le dossier contenant les fichiers csv de dépenses brutes
        - sélectionner le fichier "source de vérité" contenant les dépenses
            traitées
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.menu_bar = self.parent_window.menuBar()
        file_menu = self.menu_bar.addMenu("Fichier")
        open_menu = self.menu_bar.addMenu("Ouvrir")

        """
        Menu Fichier
        """
        # ouvrir une nouvelle fenetre
        new_window = QAction(
            "Ouvrir une nouvelle fenêtre", self.parent_window)
        file_menu.addAction(new_window)
        new_window.setShortcut("Ctrl+N")
        # quitter l'application
        exit = file_menu.addAction("Quitter", self.parent_window.close)
        exit.setShortcut("Ctrl+Q")

        """
        Menu Ouvrir
        """
        # sélectionner le dossier contenant les fichiers csv de dépenses brutes
        select_directory = \
            QAction("Créer une source de vérité à partir d'un dossier de \
                    dépenses brutes",
                    self.parent_window)
        open_menu.addAction(select_directory)
        select_directory.setShortcut("Ctrl+Shift+O")
        select_directory.triggered.connect(self.open_directory)

        # sélectionner le fichier "source de vérité" contenant les dépenses
        # traitées
        select_source_of_truth = QAction(
            "Sélectionner une source de vérité", self.parent_window)
        open_menu.addAction(select_source_of_truth)
        select_source_of_truth.setShortcut("Ctrl+O")
        select_source_of_truth.triggered.connect(self.open_source_of_truth)

    """
    Slots associés à la barre de menus
    """

    def open_directory(self):
        """
        Gère l'importation d'un dossier contenant les dépenses brutes
        Une fois le dossier sélectionné, calcule une source de vérité à partir
        des fichiers contenus dans le dossier
        """
        dialog_src = QFileDialog(self.parent_window)
        dialog_src.setFileMode(QFileDialog.Directory)
        if dialog_src.exec():
            directory_src = dialog_src.selectedFiles()[0]
            # demander à l'utilisateur de sélectionner le dossier destination
            # de la source de vérité
            # afficher un message de demande
            msgBox = QMessageBox(parent=dialog_src)
            msgBox.setText(
                "Veuillez sélectionner le dossier où enregistrer la source de\
                    vérité")
            msgBox.exec()
            dialog_dest = QFileDialog(dialog_src)
            dialog_dest.setFileMode(QFileDialog.Directory)
            if dialog_dest.exec():
                directory_dest = dialog_dest.selectedFiles()[0]
                source_of_truth_filename = directory_dest + \
                    "/source_of_truth.csv"
                # créer une source de vérité
                create_source_of_truth(directory_src, source_of_truth_filename)
                # afficher un message de validation
                validationmsgBox = QMessageBox(parent=dialog_dest)
                validationmsgBox.setText(
                    "La source de vérité a bien été créée")
                validationmsgBox.exec()
                # enregistrer la nouvelle source de vérité créée
                save_source_of_truth(source_of_truth_filename)
                # on met à jour la variable globale source_of_truth avec la
                # valeur correcte
                global_variables.source_of_truth = source_of_truth_filename

    def open_source_of_truth(self):
        """
        Gère l'importation d'un fichier de dépenses traité (source de vérité)
        """
        dialog = QFileDialog(parent=self.parent_window)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("CSV files (*.csv)")
        if dialog.exec():
            source_of_truth_path = dialog.selectedFiles()[0]
            save_source_of_truth(source_of_truth_path)
            # on met à jour la variable globale source_of_truth avec la valeur
            # correcte
            global_variables.source_of_truth = source_of_truth_path
