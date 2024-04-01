import create_unique_csv
import clean_csv
import select_transactions
import camembert
import barplot_depenses
from pathlib import Path


if __name__ == "__main__":
    """
    On rassemble et nettoie toutes les transactions fournies par LCL dans des fichiers csv
    dans un fichier csv unique qui sera notre source de vérité
    uniquement si nécessaire (préciser par l'utilisateur)
    """
    creer_source_de_verite = True
    clean_csv_filename = "/home/thiran/projets_persos/gestion_budget/csv_files/clean_csv_files/source_of_truth.csv"
    source_of_truth_path = Path(clean_csv_filename)
    if creer_source_de_verite:
        create_unique_csv.create_source_of_truth(
            source_of_truth_path, clean_csv_filename)
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
    # camembert.display_pie_chart(transactions_six_derniers_mois)
    """
    Afficher le diagramme en batons des dépenses des 6 derniers mois
    """
    transactions_carte_six_derniers_mois = select_transactions.select_transactions_by_card(
        transactions_six_derniers_mois)
    barplot_depenses.spending_barplot(transactions_carte_six_derniers_mois)
