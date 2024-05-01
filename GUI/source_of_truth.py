from PySide6.QtWidgets import QMessageBox
import global_variables

save_file_path = global_variables.save_file


def get_source_of_truth(widget):
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
        # qui doit alors sélectionner la source de vérité
        QMessageBox.warning(widget, "Avertissement",
                            global_variables.source_of_truth_notfound_msg)
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
