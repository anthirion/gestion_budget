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
# csv_filename = "../csv_files/" + sys.argv[1]
csv_filename = "../csv_files/budget_nov23_fev24.csv"

useless_characters = ["VIR.PERMANENT ", "VIREMENT ", "VIR ", "PRLV ", "CB "]
clean_lines = []

with open(csv_filename, "r", encoding="utf-8") as csvfile:
    for line in csvfile:
        fields = line.split(";")
        # nettoyer chaque champ
        # retirer les champs vides et inutiles ainsi que les caractères inutiles
        clean_fields = []
        for field in fields:
            if field:
                for character in useless_characters:
                    clean_field = field[:-2].replace(character, "")
                # remplacer les virgules par des points dans chaque champ
                clean_field = clean_field.replace(",", ".")
                clean_fields.append(clean_field)
        clean_line = ",".join(clean_fields)
        clean_lines.append(clean_line)

clean_csv_filename = "../csv_files/clean.csv"

with open(clean_csv_filename, "w", encoding="utf-8") as clean_csv_file:
    for clean_line in clean_lines:
        clean_csv_file.write(clean_line)
