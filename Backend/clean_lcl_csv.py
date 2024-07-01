"""
L'objectif de ce module est de nettoyer un csv fourni par LCL et de retourner
les lignes "propres" avec la fonction clean_entry_file.
Le procédé de nettoyage se déroule comme suit:
- Retire les colonnes vides, "divers" et "0" qui n'apportent rien.
- Enlever les caractères inutiles suivants:
    - "VIR.PERMANENT "
    - "VIREMENT "
    - "VIR "
    - "PRLV "
    - "CB "
    déjà indiqués dans un autre champ
- Renommer les catégories suivantes pour les rendre plus explicites:
    - "AMAZON PAYMENTS" -> "AMAZON"
    - "AMAZON EU SARL" -> "AMAZON"
    - "SNCF INTERNET" -> "SNCF"
    - "DRI*NVIDIA" -> "NVIDIA"
    - "FRANPRIX 1029" -> "FRANPRIX"
    - "DECAT 1994" -> "DECATHLON"
- Remplacer les points-virgules par des virgules pour respecter le format csv
et les virgules par des points
"""
import re

###############################################################################
# Variables globales relatives à ce fichier
###############################################################################

useless_parameters = ["VIR.PERMANENT ", "VIREMENT ", "VIR ", "PRLV ", "CB "]
# liste de transactions à supprimer du csv car non-pertinentes
transactions_to_delete = ["TOTAL OPTION SYSTEM' EPARGNE"]
# dictionnaire indiquant les descriptions à modifier; la clé indique l'ancienne
# description à modifier et la valeur indique la nouvelle description
descriptions_to_replace = {
    "AMAZON PAYMENTS": "AMAZON",
    "AMAZON EU SARL": "AMAZON",
    "SNCF INTERNET": "SNCF",
    "DRI*NVIDIA": "NVIDIA",
    "FRANPRIX 1029": "FRANPRIX",
    "DECAT 1994": "DECATHLON",
    "SEPA VERSPIEREN": "ABONNEMENT BOULANGER",
}
# Expression régulière pour identifier les dates jj/mm/aa
pattern = r'\b\d{1,2}/\d{1,2}/\d{2}\b'


###############################################################################
# Exceptions relatives à ce fichier
###############################################################################


class LineError(Exception):
    """
    Cette exception est levée lors d'un problème de type, plus précisément
    lorsque la ligne passée en paramètre n'est pas une chaine de caractères.
    Elle est similaire à l'exception built-in AttributeError à la différence
    qu'elle affiche la ligne en cause
    """

    def __init__(self, line):
        error_msg = f"La ligne {line} n'est pas une chaine de caractères"
        raise AttributeError(error_msg)

###############################################################################
# Fonctions
###############################################################################


def delete_line(line):
    """
    Renvoie True si la ligne contient un paramètre dans la liste
    transactions_to_delete ou n'est pas une transaction (le nombre
    de champs est inférieur à 7).
    Si la valeur renvoyée est vrai, la ligne doit être supprimée.
    """
    try:
        if len(line.split(";")) < 7:
            return True
        for pattern in transactions_to_delete:
            if pattern in line:
                return True
    except AttributeError:
        # la ligne passée en paramètre n'est pas une str
        raise LineError(line)
    return False


def add_payment_type(line):
    """
    Ajoute le moyen de paiement Virement pour la transaction ASSURANCE
    MOYEN DE PAIEMENT
    """
    try:
        new_line = line
        if "ASSURANCE MOYEN DE PAIEMENT" in line:
            fields = line.split(",")
            # description correspond ici à "ASSURANCE MOYEN DE PAIEMENT"
            # infos correspond aux autres champs
            *infos, description = fields
            new_line = ",".join(infos) + ", Virement, " + description
    except AttributeError:
        # la ligne passée en paramètre n'est pas une str
        raise LineError(line)
    except ValueError:
        # le sequence unpacking n'a pas marché
        error_msg = f"La ligne {line} ne contient pas les bons champs"
        raise ValueError(error_msg)
    return new_line


def line_cleaning(line):
    """
    Traite une ligne en retirant les paramètres inutiles, les dates
    dans la description, renomme certaines transactions pas claires et remplace
    les virgules par des points
    """
    try:
        # on remplace les virgules par des points dans chaque champ pour avoir
        # un csv propre
        line = line.replace(",", ".")
        # on retire les caractères inutiles
        for parameter in useless_parameters:
            line = line.replace(parameter, "")
        # on renomme les transactions au nom pas clair
        for old_name, new_name in descriptions_to_replace.items():
            line = line.replace(old_name, new_name)
        # on retire les dates
        line = re.sub(pattern, '', line)
    except AttributeError:
        # la ligne passée en paramètre n'est pas une str
        raise LineError(line)
    return line


def fields_cleaning(fields):
    """
    Retourne une ligne propre en nettoyant chaque champ séparé par un ;
    et en ajoutant le moyen de paiement Carte pour les transactions au montant
    positif (crédits)
    """
    clean_line = ""
    try:
        # on retire les deux derniers champs inutiles et les champs vides
        clean_fields = [field.strip() for field in fields[:-2] if field]
        # ajouter le moyen de paiement Carte pour les crédits
        if len(clean_fields) < 4:
            amount = float(clean_fields[-2])
            if amount > 0:
                # ajouter le moyen de paiement Carte
                clean_fields.insert(-1, "Carte")

        clean_line = ",".join(clean_fields)
        # ajout d'un champ supplémentaire indiquant la banque
        clean_line += ",LCL"
        clean_line += "\n"
    except ValueError:
        error_msg = f"Le montant n'est pas entier : {amount}"
        raise ValueError(error_msg)
        # print("L'erreur est la suivante :", e)
    except TypeError:
        error_msg = "Les champs passés en paramètre ne sont pas sous forme de \
                        liste"
        raise TypeError(error_msg)
    return clean_line


def clean_entry_file(csv_filename):
    """
    Nettoie les lignes du fichier donné en entrée
    et retourne la liste des lignes propres
    """
    clean_lines = []
    try:
        with open(csv_filename, "r", encoding="utf-8-sig") as csvfile:
            for line in csvfile:
                if delete_line(line) is False:
                    new_line = line_cleaning(line)
                    # extraire les champs séparés par des ;
                    fields = new_line.split(";")
                    line_with_clean_fields = fields_cleaning(fields)
                    clean_line = add_payment_type(line_with_clean_fields)
                    clean_lines.append(clean_line)
    except FileNotFoundError:
        error_msg = f"Le fichier {csv_filename} n'a pas été trouvé. \n \
                    Assurez-vous que le nom du fichier est correct."
        raise FileNotFoundError(error_msg)
    return clean_lines
