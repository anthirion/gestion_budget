"""
L'objectif de ce module est de construire un camembert des dépenses du mois en fonction des catégories
de dépenses. Il prend en entrée une liste des transactions à traiter.
"""
from collections import defaultdict
import copy
import GlobalVariables


def calculer_depenses_par_categories(transactions, condenser=False):
    """
    @parameter transactions : liste des transactions à traiter
    retourne un dictionnaire dont la clé correspond à une catégorie de dépense
    et la valeur correspondante est la somme des montants dépensés dans cette catégorie
    si condenser vaut False, le dictionnaire contient l'ensemble des dépenses
    sinon le dictionnaire regroupera certaines dépenses dans une catégorie "Autre" 
    """
    depenses = defaultdict(int)
    for transaction in transactions:
        try:
            _, montant, type_transaction, description = transaction.split(",")
            depenses[description] += -float(montant)
        except ValueError as e:
            # dans le cas où le sequence unpacking ne marche pas
            print(type(e), e)
            # transaction[:-1] pour retirer le saut de ligne lors du print
            print("La transaction suivante est incorrecte: ", transaction[:-1])
            print("Si c'est la dernière ligne, c'est ok ;) \n")

    """ 
    Pour éviter que les valeurs du dictionnaire soient illisibles sur un 
    camembert, on classe toutes les catégories dont le montant est inférieur
    à 2% de la somme des dépenses dans une catégorie "Autre"
    uniquement si condenser est True
    """
    if condenser is True:
        somme_depenses = sum(montant for montant in depenses.values())
        # limite sous laquelle on retire la catégorie et on classe la dépense dans "Autre"
        limite = GlobalVariables.pourcentage_cat_autres*somme_depenses
        # on crée un nouveau dictionnaire de dépenses condensé qui regroupe les valeurs sous la limite
        # dans une catégorie "Autre" pour ne pas toucher au dictionnaire créé précédemment
        # une shallow copie suffit car les clés et valeurs sont des types immuables
        depenses_condensees = copy.copy(depenses)
        # on crée la catégorie "Autre" dans le dictionnaire nouvellement créé
        depenses_condensees["Autre"] = 0
        for categorie, montant in depenses.items():
            if montant < limite:
                depenses_condensees["Autre"] += montant
                # on supprime la clé du dictionnaire correspondante
                del depenses_condensees[categorie]

    return (depenses if condenser is False else depenses_condensees)
