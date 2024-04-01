"""
Ce module a pour objectif de rassembler tous les scripts téléchargés sur lcl.fr
en un seul fichier csv qui rassemble et nettoie toutes les transactions
"""

import clean_csv
import glob


def extract_unique_lines(raw_csv_directory):
    """
    A partir du dossier contenant tous les csv bruts
    retourne les lignes uniques à garder dans le csv final
    """
    # on définit l'ensemble qui contiendra les lignes uniques
    unique_lines = set()
    # on parcourt tous les csv contenus dans le répertoire fourni
    for csvfile in glob.glob(raw_csv_directory + "*.csv"):
        # on nettoie les transactions du fichier courant
        clean_lines = clean_csv.clean_entry_file(csvfile)
        # on ne garde que les lignes uniques
        unique_lines.update(clean_lines)
        clean_lines.clear()
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


def create_source_of_truth(source_of_truth_path, clean_csv_filename):
    if source_of_truth_path.exists():
        raw_csv_directory = "/home/thiran/projets_persos/gestion_budget/csv_files/raw_csv_files/"
        # on retire les transactions qui apparaissent en double
        unique_lines = extract_unique_lines(
            raw_csv_directory)
        # on trie ensuite les transactions par date croissante
        unique_lines = list(unique_lines)
        unique_lines.sort(key=sort_by_transaction_date,
                          reverse=False)
        # on écrit les transactions obtenues dans la source de vérité
        with open(clean_csv_filename, "w", encoding="utf-8-sig") as file:
            # la première ligne spécifie les noms des colonnes
            column_names = "Date,Montant,Type,Description\n"
            file.write(column_names)
            for line in unique_lines:
                file.write(line)
