"""
L'objectif de ce module est de nettoyer le csv fourni et de créer un nouveau csv propre.
Le nouveau fichier csv produit retirera les colonnes vides, "divers" et "0" qui n'apportent rien
On enlèvera aussi quelques caractères inutiles comme:
    - "VIR.PERMANENT "
    - "VIREMENT "
    - "VIR "
    - "PRLV "
    - "CB " 
déjà indiqués dans un autre champ
On renommera certaines catégories pour les rendre plus explicites:
    - "AMAZON PAYMENTS" -> "AMAZON"
    - "AMAZON EU SARL" -> "AMAZON"
    - "SNCF INTERNET" -> "SNCF"
    - "DRI*NVIDIA" -> "NVIDIA"
    - "FRANPRIX 1029" -> "FRANPRIX"
    - "DECAT 1994" -> "DECATHLON"
On remplacera enfin les points-virgules par des virgules pour respecter le format csv et les virgules par des points
"""

import sys
import re

# global variables
useless_parameters = ["VIR.PERMANENT ", "VIREMENT ", "VIR ", "PRLV ", "CB "]
# liste de transactions à supprimer du csv car non-pertinentes
transactions_to_delete = ["TOTAL OPTION SYSTEM' EPARGNE"]
# dictionnaire indiquant les transactions à remplacer (clés) par
# la clé correspondante
transactions_to_replace = {
    "AMAZON PAYMENTS": "AMAZON",
    "AMAZON EU SARL": "AMAZON",
    "SNCF INTERNET": "SNCF",
    "DRI*NVIDIA": "NVIDIA",
    "FRANPRIX 1029": "FRANPRIX",
    "DECAT 1994": "DECATHLON",
}
# Expression régulière pour identifier les dates jj/mm/aa
pattern = r'\b\d{1,2}/\d{1,2}/\d{2}\b'


def delete_line(line):
    """
    Returns True if line contains a parameter in transactions_to_delete element
    or is not a transaction (the number of fields is less than 7)
    If true, the line should be deleted
    """
    if len(line.split(";")) < 7:
        return True
    for pattern in transactions_to_delete:
        if pattern in line:
            return True
    return False


def ajouter_moyen_paiement(line):
    """
    on ajoute le moyen de paiement Virement pour la transaction ASSURANCE MOYEN DE PAIEMENT
    """
    new_line = line
    if "ASSURANCE MOYEN DE PAIEMENT" in line:
        champs = line.split(",")
        # description correspond ici à "ASSURANCE MOYEN DE PAIEMENT"
        # infos correspond aux autres champs
        *infos, description = champs
        new_line = ",".join(infos) + ", Virement, " + description
    return new_line


def line_cleaning(line):
    """
    traite la ligne en entier en retirant les paramètres inutiles, les dates dans la description,
    renomme certaines transactions pas claires et remplace les virgules par des points
    """
    # on remplace les virgules par des points dans chaque champ pour avoir un csv propre
    line = line.replace(",", ".")
    # on retire les caractères inutiles
    for parameter in useless_parameters:
        line = line.replace(parameter, "")
    # on renomme les transactions au nom pas clair
    for old_name, new_name in transactions_to_replace.items():
        line = line.replace(old_name, new_name)
    # on retire les dates
    line = re.sub(pattern, '', line)
    return line


def fields_cleaning(fields):
    """
    retourne une ligne propre en nettoyant chaque champ séparé par un ;
    et on ajoute le moyen de paiement Carte pour les transactions au montant positif (crédits)
    """
    # on retire les deux derniers champs inutiles et les champs vides
    clean_fields = [field.strip() for field in fields[:-2] if field]
    # ajouter le moyen de paiement Carte pour les crédits
    if len(clean_fields) < 4:
        try:
            montant = float(clean_fields[-2])
            if montant > 0:
                # ajouter le moyen de paiement Carte
                clean_fields.insert(-2, "Carte")
        except ValueError as e:
            print("Problème: le montant n'est pas entier : ", montant)
            print("L'erreur est la suivante :", e)

    clean_line = ",".join(clean_fields)
    clean_line += "\n"
    return clean_line


def clean_entry_file(csv_filename):
    clean_lines = []
    with open(csv_filename, "r", encoding="utf-8") as csvfile:
        for line in csvfile:
            if delete_line(line) is False:
                new_line = line_cleaning(line)
                # extraire les champs séparés par des ;
                fields = new_line.split(";")
                line_with_clean_fields = fields_cleaning(fields)
                clean_line = ajouter_moyen_paiement(line_with_clean_fields)
                clean_lines.append(clean_line)
    return clean_lines


def get_new_filename(csv_filename):
    # reprendre la période du budget
    periode = csv_filename.split("/")[-1].split("_")[1:]
    # utiliser la période pour nommer le nouveau fichier csv propre
    clean_csv_filename = "../csv_files/clean_csv_files/" + "_".join(periode)
    return clean_csv_filename


def write_new_file(clean_csv_filename, clean_lines):
    with open(clean_csv_filename, "w", encoding="utf-8") as clean_csv_file:
        # indiquer en première ligne les noms des colonnes
        column_names = "Date,Montant,Type,Description\n"
        clean_csv_file.write(column_names)
        # ecrire dans le nouveau csv les lignes écrites proprement
        for clean_line in clean_lines:
            clean_csv_file.write(clean_line)


if __name__ == "__main__":
    try:
        csv_filename = "../csv_files/raw_csv_files/" + sys.argv[1]
        clean_lines = clean_entry_file(csv_filename)
        clean_csv_filename = get_new_filename(csv_filename)
        write_new_file(clean_csv_filename, clean_lines)
    except IndexError as e:
        print("Nombre d'arguments fournis incorrect !")
        print("Vous devez fournir le nom du fichier csv à nettoyer")
        print("L'erreur est la suivante :", e)
