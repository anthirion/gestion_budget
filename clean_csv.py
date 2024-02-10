"""
L'objectif de ce code est de nettoyer le csv fourni et de créer un nouveau csv propre.
Le nouveau fichier csv produit retirera les colonnes vides, "divers" et "0" qui n'apportent rien
On enlèvera aussi les caractères inutiles suivants:
    - "VIR.PERMANENT "
    - "VIREMENT "
    - "VIR "
    - "PRLV "
    - "CB " 
déjà indiqués dans un autre champ
On remplacera les points-virgules par des virgules pour respecter le format csv et les virgules par des points
"""

import sys
import re
# import copy
csv_filename = "../csv_files/" + sys.argv[1]

useless_parameters = ["VIR.PERMANENT ", "VIREMENT ", "VIR ", "PRLV ", "CB "]
clean_lines = []
# Expression régulière pour identifier les dates jj/mm/aa
pattern = r'\b\d{1,2}/\d{1,2}/\d{2}\b'

# reformater le fichier csv donné en entrée
with open(csv_filename, "r", encoding="utf-8") as csvfile:
    for line in csvfile:
        # on remplace les virgules par des points dans chaque champ pour avoir un csv propre
        line = line.replace(",", ".")
        # on retire les caractères inutiles
        for parameter in useless_parameters:
            line = line.replace(parameter, "")
        # on retire les dates
        line_without_dates = re.sub(pattern, '', line)
        fields = line_without_dates.split(";")
        # on retire les deux derniers champs inutiles et les champs vides
        clean_fields = [field for field in fields[:-2] if field]
        clean_line = ",".join(clean_fields)
        # ajouter un retour à la ligne
        clean_line += "\n"
        clean_lines.append(clean_line)

# réécrire proprement le csv dans un autre fichier
clean_csv_filename = "../csv_files/clean.csv"

with open(clean_csv_filename, "w", encoding="utf-8") as clean_csv_file:
    for clean_line in clean_lines:
        clean_csv_file.write(clean_line)
