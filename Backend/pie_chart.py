"""
L'objectif de ce module est de construire un camembert des dépenses du mois en
fonction des catégories de dépenses. Il prend en entrée une liste des
transactions à traiter.
"""
from collections import defaultdict
import copy
import global_variables as GV


def split_transactions_by_categories(transactions, condenser=False):
    """
    @parameter {list} transactions : liste des transactions à traiter
    Cette fonction est capable de traiter n'importe quel type d'opération:
    dépenses, revenus ou épargne.
    Retourne un dictionnaire dont la clé correspond à une catégorie
    d'opérations et la valeur correspondante est la somme des montants
    appartenant à cette catégorie.
    Si condenser vaut False, le dictionnaire contient l'ensemble des
    opérations, sinon le dictionnaire regroupera certaines opérations dans
    une catégorie "Autre"
    """
    operations = defaultdict(int)
    for transaction in transactions:
        _, amount, _, description = transaction.split(",")[:4]
        operations[description] += float(amount)

    """
    Pour éviter que les valeurs du dictionnaire soient illisibles sur un
    camembert, on classe toutes les catégories dont le montant est inférieur
    à 2% de la somme des dépenses dans une catégorie "Autre"
    **uniquement si condenser est True**
    """
    if condenser is True:
        sum_operations = sum(amount for amount in operations.values())
        # limite sous laquelle on retire la catégorie et on classe la dépense
        # dans "Autre"
        limite = GV.pourcentage_cat_autres * sum_operations
        # on crée un nouveau dictionnaire de dépenses condensé qui regroupe
        # les valeurs sous la limite dans une catégorie "Autre" pour ne pas
        # toucher au dictionnaire créé précédemment une shallow copie suffit
        # car les clés et valeurs sont des types immuables
        condensed_operations = copy.copy(operations)
        # on crée la catégorie "Autre" dans le dictionnaire nouvellement créé
        condensed_operations["Autre"] = 0
        for categorie, amount in operations.items():
            if amount < limite:
                condensed_operations["Autre"] += amount
                # on supprime la catégorie incluse dans Autre
                del condensed_operations[categorie]

    return (operations if condenser is False else condensed_operations)
