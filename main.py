import create_unique_csv
import clean_csv
import select_transactions
import camembert
from pathlib import Path
import argparse


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
    # on split le fichier par transaction
    transactions = transactions.split(("\n"))
    # on retire la première ligne qui correspond aux colonnes
    transactions = transactions[1:]
    # on récupère les arguments mois et année fournis par l'utilisateur à travers la ligne de commande
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mois", help="le nombre de mois à analyser", type=int, default=1)
    parser.add_argument(
        "--annee", help="le nombre d'années à analyser", type=int, default=0)
    args = parser.parse_args()
    transactions_dernier_mois = select_transactions.select_transactions(transactions,
                                                                        n_month=args.mois,
                                                                        n_year=args.annee)
    """
    Afficher le camembert sur les transactions souhaitées
    """
    camembert.display_pie_chart(transactions_dernier_mois)
