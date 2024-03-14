"""
Ce module a pour objectif de rassembler tous les scripts téléchargés sur lcl.fr
en un seul fichier csv qui rassemble toutes les transactions
"""

import clean_csv
import glob


def extract_unique_lines(raw_csv_directory):
    """
    A partir du dossier contenant tous les csv bruts
    retourne les lignes uniques à garder dans le csv final
    """
    # on définit l'ensemble qui contiendra l'ensemble des lignes uniques
    unique_lines = set()
    # on parcoure tous les csv du chemin fourni
    for csvfile in glob.glob(raw_csv_directory + "*.csv"):
        clean_lines = clean_csv.clean_entry_file(csvfile)
        unique_lines.update(clean_lines)
        clean_lines.clear()
    return unique_lines


def sort_by_transaction_date(line):
    try:
        day, month, year = line.split(",")[0].split("/")
        return (year, month, day)
    except ValueError as ve:
        print(type(ve), ve)


if __name__ == "__main__":
    raw_csv_directory = "/home/thiran/projets_persos/gestion_budget/csv_files/raw_csv_files/"
    unique_lines = extract_unique_lines(raw_csv_directory)
    # on trie ensuite les lignes par date de transaction
    unique_lines = list(unique_lines)
    unique_lines.sort(key=sort_by_transaction_date)
    clean_csv_filename = "/home/thiran/projets_persos/gestion_budget/csv_files/clean_csv_files/source_of_truth.csv"
    # on écrit les lignes dans le fichier ci-dessus
    with open(clean_csv_filename, "w", encoding="utf-8") as file:
        for line in unique_lines:
            file.write(line)
