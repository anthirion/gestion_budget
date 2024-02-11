"""
L'objectif de ce code est de nettoyer le csv fourni et de créer un nouveau csv propre.
Le nouveau fichier csv produit retirera les colonnes vides, "divers" et "0" qui n'apportent rien
On enlèvera aussi quelques caractères inutiles comme:
    - "VIR.PERMANENT "
    - "VIREMENT "
    - "VIR "
    - "PRLV "
    - "CB " 
déjà indiqués dans un autre champ
On remplacera enfin les points-virgules par des virgules pour respecter le format csv et les virgules par des points
"""

import sys
import re

csv_filename = "../csv_files/" + sys.argv[1]

useless_parameters = ["VIR.PERMANENT ", "VIREMENT ", "VIR ", "PRLV ", "CB "]
# Expression régulière pour identifier les dates jj/mm/aa
pattern = r'\b\d{1,2}/\d{1,2}/\d{2}\b'

# on ajoute le moyen de paiement pour la transaction "ASSURANCE MOYEN DE PAIEMENT"


def ajouter_moyen_paiement(line):
    new_line = line
    if "ASSURANCE MOYEN DE PAIEMENT" in line:
        champs = line.split(",")
        # description correspond ici à "ASSURANCE MOYEN DE PAIEMENT"
        # infos correspond aux autres champs
        infos, description = champs[:-1], champs[-1]
        new_line = ",".join(infos) + ", Virement, " + description
    return new_line

# traite la ligne en entier en retirant les paramètres inutiles, les dates dans la description
# et remplace les virgules par des points


def line_cleaning(line):
    # on remplace les virgules par des points dans chaque champ pour avoir un csv propre
    line = line.replace(",", ".")
    # on retire les caractères inutiles
    for parameter in useless_parameters:
        line = line.replace(parameter, "")
    # on retire les dates
    line = re.sub(pattern, '', line)
    return line

# retourne une ligne propre en nettoyant chaque champ séparé par un ;


def fields_cleaning(fields):
    # on retire les deux derniers champs inutiles et les champs vides
    clean_fields = [field.strip() for field in fields[:-2] if field]
    clean_line = ",".join(clean_fields)
    # ajouter un retour à la ligne
    clean_line += "\n"
    return clean_line


# reformater le fichier csv donné en entrée
clean_lines = []
with open(csv_filename, "r", encoding="utf-8") as csvfile:
    for line in csvfile:
        new_line = line_cleaning(line)
        # extraire les champs séparés par des ;
        fields = new_line.split(";")
        line_with_clean_fields = fields_cleaning(fields)
        clean_line = ajouter_moyen_paiement(line_with_clean_fields)
        clean_lines.append(clean_line)

# réécrire proprement le csv dans un autre fichier
# reprendre la période du budget
periode = csv_filename.split("/")[-1].split("_")[1:]
# utiliser la période pour nommer le nouveau fichier csv propre
clean_csv_filename = "../csv_files/cleancsv_" + "_".join(periode)

with open(clean_csv_filename, "w", encoding="utf-8") as clean_csv_file:
    # indiquer en première ligne les noms des colonnes
    column_names = "Date, Montant, Type, Description\n"
    clean_csv_file.write(column_names)
    # ecrire dans le nouveau csv les lignes écrites proprement
    for clean_line in clean_lines:
        clean_csv_file.write(clean_line)
