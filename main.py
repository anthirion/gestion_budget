import create_unique_csv
import clean_csv
import select_transactions
import camembert
import barplot_depenses
from pathlib import Path
import argparse


if __name__ == "__main__":
    """
    On récupére les arguments que l'utilisateur fournis via la ligne de commande
    pour les traiter plus tard
    """
    # parser = argparse.ArgumentParser()
    # # on crée l'argument qui indique s'il est nécessaire de créer la source de vérité ou non
    # parser.add_argument(
    #     "--creer_source_de_verite", help="indique s'il est nécessaire de créer la source de vérité",
    #     type=bool, default=False)
    # # on crée les arguments mois et année fournis par l'utilisateur à travers la ligne de commande
    # parser.add_argument(
    #     "--mois", help="le nombre de mois à analyser", type=int, default=6)
    # parser.add_argument(
    #     "--annee", help="le nombre d'années à analyser", type=int, default=0)
    # # on récupère tous les arguments fournis par l'utilisateur
    # args = parser.parse_args()
    creer_source_de_verite = True
    """
    On rassemble et nettoie toutes les transactions fournies par LCL dans des fichiers csv
    dans un fichier csv unique qui sera notre source de vérité
    uniquement si nécessaire (préciser par l'utilisateur)
    """
    clean_csv_filename = "/home/thiran/projets_persos/gestion_budget/csv_files/clean_csv_files/source_of_truth.csv"
    source_of_truth_path = Path(clean_csv_filename)
    if creer_source_de_verite is True and source_of_truth_path.exists():
        raw_csv_directory = "/home/thiran/projets_persos/gestion_budget/csv_files/raw_csv_files/"
        # on retire les transactions qui apparaissent en double
        unique_lines = create_unique_csv.extract_unique_lines(
            raw_csv_directory)
        # on trie ensuite les transactions par date croissante
        unique_lines = list(unique_lines)
        unique_lines.sort(key=create_unique_csv.sort_by_transaction_date,
                          reverse=False)
        # on écrit les transactions obtenues dans la source de vérité
        with open(clean_csv_filename, "w", encoding="utf-8-sig") as file:
            # la première ligne spécifie les noms des colonnes
            column_names = "Date,Montant,Type,Description\n"
            file.write(column_names)
            for line in unique_lines:
                file.write(line)
    """
    On sélectionne les transactions de la période souhaitée par l'utilisateur
    """
    transactions = source_of_truth_path.read_text(encoding="utf-8-sig")
    # on split le fichier par transaction
    transactions = transactions.split(("\n"))
    # on retire la première ligne qui correspond aux colonnes
    transactions = transactions[1:]
    transactions_six_derniers_mois = select_transactions.select_transactions(transactions,
                                                                             n_month=6,
                                                                             n_year=0)
    """
    Afficher le camembert des transactions correspondantes à la période souhaitée
    """
    # camembert.display_pie_chart(transactions_dernier_mois)
    """
    Afficher le diagramme en batons des dépenses des 6 derniers mois
    """
    barplot_depenses.spending_barplot(transactions_six_derniers_mois)
