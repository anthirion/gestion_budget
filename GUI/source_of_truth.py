"""
Ce module implémente toutes les fonctions utiles à la gestion de la source de
vérité par l'interface graphique GUI
"""


from PySide6.QtWidgets import QMessageBox
import global_variables as GV
from pathlib import Path

save_file = GV.save_file


def get_transactions():
    """
    Cette fonction récupère les transactions inscrites dans la source de vérité
    @return transactions de la source de vérité
    """
    # sélection des transactions
    source_of_truth_path = Path(GV.source_of_truth)
    # sélectionner les transactions souhaitées par l'utilisateur
    transactions = source_of_truth_path.read_text(encoding="utf-8-sig")
    # on split le fichier par transaction
    transactions = transactions.split(("\n"))
    # on retire la première ligne qui correspond aux colonnes
    # et la dernière transaction qui est vide
    return transactions[1:-1]


def check_save_file_exists(filename):
    """
    Vérifie que le fichier spécifié pour enregistrer la source
    de vérité existe
    Sinon, le créer avec un contenu vide
    """
    path = Path(filename)
    if not path.exists():
        open(filename, mode="x", encoding="utf-8-sig")


def get_source_of_truth(widget):
    """
    @parameter {QWidget} widget: widget où afficher le message d'erreur si la
        source de vérité n'est pas trouvée
    Cette fonction va récupérer la source de vérité dans le fichier enregistré
    dans le fichier de sauvegarde
    """
    # lire le contenu du fichier de sauvegarde et récupérer la valeur de la
    # variable source_of_truth qui indique le chemin de la source de vérité
    check_save_file_exists(save_file)
    with open(save_file, "r") as sauv_file:
        lines = sauv_file.readlines()
    found = False
    for line in lines:
        if "source_of_truth_file" in line:
            found = True
            _, file_path = line.split('=')
            return file_path.strip()

    if found is False:
        # la source de vérité n'a pas été trouvée, remonter une erreur à
        # l'utilisateur qui doit alors sélectionner la source de vérité
        QMessageBox.warning(widget, "Avertissement",
                            GV.source_of_truth_notfound_msg)
        return ""


def save_source_of_truth(source_of_truth_path):
    """
    Retirer la variable source_of_truth_file incorrecte du fichier sauv_file
    si elle existe
    """
    check_save_file_exists(save_file)
    with open(save_file, "r") as sauv_file:
        lines = sauv_file.readlines()
    with open(save_file, "w") as sauv_file:
        for line in lines:
            if "source_of_truth_file" not in line:
                sauv_file.write(line)
        # écrire dans le fichier la valeur correcte du chemin de la source de
        # vérité
        sauv_file.write(f"source_of_truth_file = {source_of_truth_path}")
