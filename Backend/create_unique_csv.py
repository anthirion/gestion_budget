"""
Ce module a pour objectif de rassembler tous les scripts téléchargés sur lcl.fr
en un seul fichier csv qui rassemble et nettoie toutes les transactions
"""
from pathlib import Path

import Backend.clean_lcl_csv
import Backend.clean_fortuneo_csv

import global_variables as GV

# dictionnaire définissant à partir de la banque quelle fonction de nettoyage
# utiliser
clean_function = {"LCL": Backend.clean_lcl_csv.clean_entry_file,
                  "Fortuneo": Backend.clean_fortuneo_csv.clean_entry_file,
                  }


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


def extract_unique_lines(raw_csv_dir_path):
    """
    @parameter {Path} raw_csv_dir_path: dossier contenant les csv bruts de
        toutes les banques
    @return unique_lines: lignes nettoyées et sans doublon
    A partir du dossier contenant les csv bruts de toutes les banques,
    cette fonction récupère de manière récursive les csv et retourne
    les lignes uniques à garder dans la source de vérité
    """
    # on définit l'ensemble qui contiendra les lignes uniques
    unique_lines = set()
    if (raw_csv_dir_path.exists() and raw_csv_dir_path.is_dir()):
        for bank in GV.banks:
            bank_dir_path = raw_csv_dir_path / Path(bank)
            if (bank_dir_path.exists() and bank_dir_path.is_dir()):
                clean_fct = clean_function[bank]
                # on parcourt tous les csv contenus dans les sous-répertoires
                for csvfile in bank_dir_path.glob('**/*.csv'):
                    # on nettoie les transactions du fichier courant
                    clean_lines = clean_fct(csvfile)
                    # on ne garde que les lignes uniques
                    unique_lines.update(clean_lines)
                    clean_lines.clear()
            else:
                raise BadDirectoryError(bank_dir_path)
    else:
        raise BadDirectoryError(raw_csv_dir_path)
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


def create_source_of_truth(raw_csv_dir, source_of_truth_filename):
    """
    @parameter {str} raw_csv_dir: répertoire contenant les fichiers
        de transactions bruts à utiliser pour créer la source de vérité
    @parameter {str} source_of_truth_filename: le nom à donner à la source
        de vérité créée
    Cette fonction construit une source de vérité de transactions bancaires
    à partir de fichiers csv bruts stockés dans un dossier
    """
    raw_csv_dir_path = Path(raw_csv_dir)
    if (raw_csv_dir_path.exists() and
            raw_csv_dir_path.is_dir()):
        # on retire les transactions qui apparaissent en double
        unique_lines = extract_unique_lines(raw_csv_dir_path)
        # on trie ensuite les transactions par date croissante
        unique_lines = list(unique_lines)
        unique_lines.sort(key=sort_by_transaction_date,
                          reverse=False)
        try:
            # on écrit les transactions obtenues dans la source de vérité
            with open(source_of_truth_filename, "w", encoding="utf-8-sig") as\
                    file:
                # la première ligne spécifie les noms des colonnes
                column_names = "Date,Amount,Type,Description,Bank\n"
                file.write(column_names)
                for line in unique_lines:
                    file.write(line)
        except FileNotFoundError:
            error_msg = f"Le fichier {source_of_truth_filename} n'a pas été\
                            trouvé"
            raise FileNotFoundError(error_msg)
    else:
        raise BadDirectoryError(raw_csv_dir_path)


# if __name__ == "__main__":
#     base_path = "/home/thiran/projets_persos/gestion_budget/csv_files/"
#     raw_csv_dir = base_path + "raw_csv_files/"
#     dest_file = base_path + "source_of_truth.csv"
#     create_source_of_truth(raw_csv_dir, dest_file)
