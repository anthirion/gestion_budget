"""
L'objectif de ce module est de splitter les csv fournis par LCL afin d'avoir un csv par mois de dépenses
"""

import clean_csv
import sys


def get_month_year(line):
    """
    Récupère le mois et l'année à partir d'une ligne du fichier csv
    """
    date = line.split(",")[0]
    return (date.split("/")[1], date.split("/")[2])


def toString(month, year):
    """
    Convertit le numéro de mois et l'année en chaine de caractère
    Ex: 01/2022 -> janv 2022
    """
    # s'assurer que le mois et l'année sont bien des chaines de caractères
    month, year = str(month), str(year)
    month_number_toString = {"01": "janv",
                             "02": "fev",
                             "03": "mars",
                             "04": "avril",
                             "05": "mai",
                             "06": "juin",
                             "07": "juil",
                             "08": "aout",
                             "09": "sept",
                             "10": "oct",
                             "11": "nov",
                             "12": "dec",
                             }
    try:
        month_string = month_number_toString[month]
    except KeyError as e:
        print("Le numéro de mois est incorrect", e)
    return month_string + year + ".csv"


def split_csv_by_month(csv_lines):
    """
    Retourne un dictionnaire dont la clé est le nom du nouveau fichier à créer
    et la valeur le contenu du fichier
    """
    csv_content = {}
    # on lis la première ligne à part
    line = csv_lines[0]
    month, year = get_month_year(line)
    current_month = month
    filename = toString(month, year)
    csv_content[filename] = [line]
    for line in csv_lines[1:]:
        month, year = get_month_year(line)
        if month == current_month:
            csv_content[filename].append(line)
        else:
            # il faut écrire les lignes suivantes dans un nouveau fichier
            filename = toString(month, year)
            csv_content[filename] = [line]
            current_month = month
    return csv_content


def write_csv_content(csv_content):
    for filename, content in csv_content.items():
        filename = "../csv_files/clean_csv_files/" + filename
        with open(filename, "w", encoding="utf-8") as file:
            for line in content:
                file.write(line)


if __name__ == "__main__":
    try:
        raw_csv_filename = "../csv_files/raw_csv_files/" + sys.argv[1]
        clean_file_lines = clean_csv.clean_entry_file(raw_csv_filename)
        csv_content = split_csv_by_month(clean_file_lines)
        write_csv_content(csv_content)
    except IndexError as e:
        print("Nombre d'arguments fournis incorrect !")
        print("Vous devez fournir le nom du fichier csv à splitter")
        print("L'erreur est la suivante :", e)
