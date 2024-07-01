"""
L'objectif de ce module est de nettoyer un csv fourni par Fortuneo et de
retourner les lignes "propres" avec la fonction clean_entry_file.
Le procédé de nettoyage se déroule comme suit:
1. Remplacer ; par , ET , par .
2. Retirer les champs vides et le 2ème champ qui est identique au 1er
3. Récupérer le montant et le mettre en 2ème position
4. Type: en fonction du premier mot de la description (attention à la
description "Banque prime ouverture)
5. Description:
    - retirer le type (VIR et CARTE) et le mot suivant
    - retirer le numéro du PEA
"""

# dictionnaire indiquant les descriptions à modifier; la clé indique l'ancienne
# description à modifier et la valeur indique la nouvelle description
descriptions_to_replace = {
    "SNCF INTERNET PARIS 10": "SNCF",
}


def clean_description(description_field):
    """
    Nettoie le champ description fourni en entrée avec les règles données
    ci-dessus
    """
    cleaned_description = ""
    description_field = description_field.strip()
    # si le virement concerne le PEA, écrire simplement PEA
    if "PEA" in description_field:
        cleaned_description = "PEA"
    elif "SALAIRE" in description_field:
        cleaned_description = "SALAIRE"
    else:
        # retirer VIR ou CARTE et le mot ou la date qui suit
        description_words = description_field.split()
        if len(description_words) > 2:
            cleaned_description = " ".join(description_words[2:])
    # renommer certaines descriptions peu claires
    # ATTENTION faire correspondre aux descriptions de LCL
    for key in descriptions_to_replace.keys():
        if key in description_field:
            cleaned_description = descriptions_to_replace[key]
    return cleaned_description


def clean_line(line):
    """
    Nettoie la ligne en :
    - remplaçant ; par , et , par .
    - retirant les champs inutiles (2ème champ et champs vides)
    - déplacer le montant en 2ème position
    - ajoutant le type de transaction
    - nettoyant le champ description
    """
    new_line = ""
    line = line.replace(",", ".")
    line = line.replace(";", ",")
    transaction_type = ""
    infos = line.split(",")
    infos = [info.strip() for info in infos]
    # le nombre d'éléments n'est pas constant:
    # si le débit est non-nul, pas de champ crédit
    date, _, description, amount = infos[:4]
    if not amount:
        # le champ debit est vide
        amount = infos[4]
    # ajouter le type de transaction
    # le 1er mot de la description indique le type de transaction
    # sauf dans le cas où la description est "BANQUE PRIME OUVERTURE"
    if description.startswith("CARTE"):
        transaction_type = "Carte"
    else:
        # dans le cas où la description commence par VIR ou est "BANQUE
        # PRIME OUVERTURE"
        transaction_type = "Virement"
    # nettoyer le champ description
    cleaned_description = clean_description(description)
    new_line = ",".join(
        [date, amount, transaction_type, cleaned_description])
    # ajout d'un champ supplémentaire indiquant la banque
    new_line += ",Fortuneo"
    # ajouter un retour à la ligne
    new_line += "\n"
    return new_line


def clean_entry_file(csv_filename):
    clean_lines = []
    line_nb = 1
    try:
        with open(csv_filename, "r", encoding="utf-8-sig") as csvfile:
            for line in csvfile:
                # ignorer la première ligne
                if line_nb == 1:
                    line_nb += 1
                    continue
                new_line = clean_line(line)
                clean_lines.append(new_line)
    except FileNotFoundError:
        error_msg = f"Le fichier {csv_filename} n'a pas été trouvé. \n \
                    Assurez-vous que le nom du fichier est correct."
        raise FileNotFoundError(error_msg)
    return clean_lines


if __name__ == "__main__":
    base_path = "/home/thiran/projets_persos/gestion_budget/csv_files/raw_csv_files/"
    entry_file = base_path + "Fortuneo/transactions_test.csv"
    output_file = base_path + "source_of_truth.csv"
    clean_lines = clean_entry_file(entry_file)
    with open(output_file, "w", encoding="utf-8-sig") as f:
        for line in clean_lines:
            f.write(line)
