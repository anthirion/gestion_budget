import create_unique_csv
import clean_csv
import select_transactions
import camembert
from pathlib import Path


if __name__ == "__main__":
    raw_csv_directory = "/home/thiran/projets_persos/gestion_budget/csv_files/raw_csv_files/"
    """
    On rassemble et nettoie toutes les transactions dans un fichier csv unique
    qui sera notre source de vérité
    """
    # on retire les transactions qui apparaissent en double
    unique_lines = create_unique_csv.extract_unique_lines(raw_csv_directory)
    # on trie ensuite les transactions par date croissante
    unique_lines = list(unique_lines)
    unique_lines.sort(key=create_unique_csv.sort_by_transaction_date,
                      reverse=False)
    # on écrit les transactions obtenues dans la source de vérité
    clean_csv_filename = "/home/thiran/projets_persos/gestion_budget/csv_files/clean_csv_files/source_of_truth.csv"
    with open(clean_csv_filename, "w", encoding="utf-8") as file:
        # la première ligne spécifie les noms des colonnes
        column_names = "Date,Montant,Type,Description\n"
        file.write(column_names)
        for line in unique_lines:
            file.write(line)
    """
    On sélectionne les transactions du dernier mois (mois de mars 2023)
    """
    source_of_truth_path = Path(clean_csv_filename)
    transactions = source_of_truth_path.read_text(encoding="utf-8")
    # on retire la première ligne qui correspond aux colonnes
    begin_index = transactions.find("\n")
    assert isinstance(begin_index, int)
    transactions_dernier_mois = select_transactions.select_transactions(transactions[begin_index:],
                                                                        month=1,
                                                                        year=0)
    print(transactions_dernier_mois)
