"""
Ce module a pour objectif de rassembler tous les scripts téléchargés sur lcl.fr
en un seul fichier csv qui rassemble et nettoie toutes les transactions
"""
from pathlib import Path

from Backend.clean_csv import clean_entry_file


###############################################################################
# Exceptions relatives à ce fichier
###############################################################################
class BadDirectoryError(Exception):
    """
    Cette exception se déclenche lorsque le dossier passé en paramètre
    n'existe pas OU n'est pas un dossier
    """

    def __init__(self, bad_directory_path):
        error_msg = f"Le dossier {str(bad_directory_path)} n'existe pas ou \
                        n'est pas un dossier"
        raise FileNotFoundError(error_msg)

###############################################################################
# Fonctions
###############################################################################


def extract_unique_lines(raw_csv_directory_path):
    """
    A partir du dossier contenant tous les csv bruts, cette fonction
    retourne les lignes uniques à garder dans la source de vérité
    """
    # on définit l'ensemble qui contiendra les lignes uniques
    unique_lines = set()
    if (raw_csv_directory_path.exists() and
            raw_csv_directory_path.is_dir()):
        # on parcourt tous les csv contenus dans le répertoire fourni
        for csvfile in raw_csv_directory_path.glob('**/*.csv'):
            # on nettoie les transactions du fichier courant
            clean_lines = clean_entry_file(csvfile)
            # on ne garde que les lignes uniques
            unique_lines.update(clean_lines)
            clean_lines.clear()
    else:
        raise BadDirectoryError(raw_csv_directory_path)
    return unique_lines


def sort_by_transaction_date(line):
    """
    On définit ici la manière de trier les transactions:
    on les trie par date
    """
    try:
        day, month, year = line.split(",")[0].split("/")
        return (year, month, day)
    except ValueError as ve:
        print(type(ve), ve)


def create_source_of_truth(raw_csv_directory, source_of_truth_filename):
    """
    @parameter {str} raw_csv_directory: répertoire contenant les fichiers
        de transactions bruts à utiliser pour créer la source de vérité
    @parameter {str} source_of_truth_filename: le nom à donner à la source
        de vérité créée
    Cette fonction construit une source de vérité de transactions bancaires
    à partir de fichiers csv bruts stockés dans un dossier
    """
    raw_csv_directory_path = Path(raw_csv_directory)
    if (raw_csv_directory_path.exists() and
            raw_csv_directory_path.is_dir()):
        # on retire les transactions qui apparaissent en double
        unique_lines = extract_unique_lines(
            raw_csv_directory_path)
        # on trie ensuite les transactions par date croissante
        unique_lines = list(unique_lines)
        unique_lines.sort(key=sort_by_transaction_date,
                          reverse=False)
        try:
            # on écrit les transactions obtenues dans la source de vérité
            with open(source_of_truth_filename, "w", encoding="utf-8-sig") as\
                    file:
                # la première ligne spécifie les noms des colonnes
                column_names = "Date,Amount,Type,Description\n"
                file.write(column_names)
                for line in unique_lines:
                    file.write(line)
        except FileNotFoundError:
            error_msg = f"Le fichier {source_of_truth_filename} n'a pas été\
                            trouvé"
            raise FileNotFoundError(error_msg)
    else:
        raise BadDirectoryError(raw_csv_directory_path)
