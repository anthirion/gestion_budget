"""
Ce module a pour objectif de rassembler tous les scripts téléchargés sur lcl.fr
en un seul fichier csv qui rassemble et nettoie toutes les transactions
"""
from pathlib import Path

from Backend.clean_csv import clean_entry_file


def extract_unique_lines(raw_csv_directory_path):
    """
    A partir du dossier contenant tous les csv bruts, cette fonction
    retourne les lignes uniques à garder dans le csv final
    """
    # on définit l'ensemble qui contiendra les lignes uniques
    unique_lines = set()
    # on parcourt tous les csv contenus dans le répertoire fourni
    for csvfile in raw_csv_directory_path.glob('**/*.csv'):
        # on nettoie les transactions du fichier courant
        clean_lines = clean_entry_file(csvfile)
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


def create_source_of_truth(raw_csv_directory, source_of_truth_filename):
    raw_csv_directory_path = Path(raw_csv_directory)
    if raw_csv_directory_path.exists():
        # on retire les transactions qui apparaissent en double
        unique_lines = extract_unique_lines(
            raw_csv_directory_path)
        # on trie ensuite les transactions par date croissante
        unique_lines = list(unique_lines)
        unique_lines.sort(key=sort_by_transaction_date,
                          reverse=False)
        # on écrit les transactions obtenues dans la source de vérité
        with open(source_of_truth_filename, "w", encoding="utf-8-sig") as file:
            # la première ligne spécifie les noms des colonnes
            column_names = "Date,Montant,Type,Description\n"
            file.write(column_names)
            for line in unique_lines:
                file.write(line)
