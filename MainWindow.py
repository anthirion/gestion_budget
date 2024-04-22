from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QFileDialog, QMessageBox
)
from PySide6.QtGui import QAction
import GlobalVariables
from create_unique_csv import create_source_of_truth


save_file_path = GlobalVariables.save_file


class MainWindow(QMainWindow):

    def __init__(self, widget_one_month, widget_several_months):
        try:
            super().__init__()
            self.setWindowTitle(
                "Mon super logiciel de visualisation des dépenses")

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
                "Créer une source de vérité à partir d'un dossier de dépenses brutes", self)
            open_menu.addAction(select_directory)
            select_directory.setShortcut("Ctrl+Shift+O")
            select_directory.triggered.connect(self.open_directory)

            # sélectionner le fichier "source de vérité" contenant les dépenses traitées
            select_source_of_truth = QAction(
                "Sélectionner un fichier de dépenses", self)
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
            tabs.addTab(widget_one_month, "Dépenses sur un mois")
            tabs.addTab(widget_several_months,
                        "Statistiques sur plusieurs mois")
            # placer les onglets sur la gauche
            tabs.setTabPosition(QTabWidget.West)
            self.setCentralWidget(tabs)

        except Exception as e:
            critical_error = QMessageBox.critical(parent=self)
            critical_error.setText(e)
            critical_error.exec()

    """
    Slots associés à la barre de menus
    """

    def open_directory(self):
        """
        Gère l'importation d'un dossier contenant les dépenses brutes
        Une fois le dossier sélectionné, calcule une source de vérité à partir
        des fichiers contenus dans le dossier
        """
        dialog_src = QFileDialog(self)
        dialog_src.setFileMode(QFileDialog.Directory)
        if dialog_src.exec():
            directory_src = dialog_src.selectedFiles()[0]
            # demander à l'utilisateur de sélectionner le dossier destination
            # de la source de vérité
            # afficher un message de demande
            msgBox = QMessageBox(parent=dialog_src)
            msgBox.setText(
                "Veuillez sélectionner le dossier où enregistrer la source de vérité")
            msgBox.exec()
            dialog_dest = QFileDialog(dialog_src)
            dialog_dest.setFileMode(QFileDialog.Directory)
            if dialog_dest.exec():
                directory_dest = dialog_dest.selectedFiles()[0]
                source_of_truth_filename = directory_dest + "/source_of_truth.csv"
                # créer une source de vérité
                create_source_of_truth(directory_src, source_of_truth_filename)
                # afficher un message de validation
                validationmsgBox = QMessageBox(parent=dialog_dest)
                validationmsgBox.setText(
                    "La source de vérité a bien été créée")
                validationmsgBox.exec()
                # enregistrer la nouvelle source de vérité créée
                save_source_of_truth(source_of_truth_filename)
                # on met à jour la variable globale source_of_truth avec la valeur correcte
                GlobalVariables.source_of_truth = source_of_truth_filename

    def open_source_of_truth(self):
        """
        Gère l'importation d'un fichier de dépenses traité (source de vérité)
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("CSV files (*.csv)")
        if dialog.exec():
            source_of_truth_path = dialog.selectedFiles()[0]
            save_source_of_truth(source_of_truth_path)
            # on met à jour la variable globale source_of_truth avec la valeur correcte
            GlobalVariables.source_of_truth = source_of_truth_path


def get_source_of_truth():
    """
    Cette fonction va récupérer la source de vérité dans le fichier enregistré
    dans le fichier de sauvegarde
    """
    # lire le contenu du fichier de sauvegarde et récupérer la valeur de la variable
    # source_of_truth qui indique le chemin de la source de vérité
    with open(save_file_path, "r") as sauv_file:
        lines = sauv_file.readlines()
    found = False
    for line in lines:
        if "source_of_truth_file" in line:
            found = True
            _, file_path = line.split('=')
            return file_path.strip()

    if found is False:
        # la source de vérité n'a pas été trouvée, remonter une erreur à l'utilisateur
        # qui doit alors la sélectionner
        print(GlobalVariables.source_of_truth_notfound_msg)
        return ""


def save_source_of_truth(source_of_truth_path):
    # retirer la variable source_of_truth_file incorrecte du fichier sauv_file si elle existe
    with open(save_file_path, "r") as sauv_file:
        lines = sauv_file.readlines()
    with open(save_file_path, "w") as sauv_file:
        for line in lines:
            if "source_of_truth_file" not in line:
                sauv_file.write(line)
        # écrire dans le fichier la valeur correcte du chemin de la source de vérité
        sauv_file.write(f"source_of_truth_file = {source_of_truth_path}")
