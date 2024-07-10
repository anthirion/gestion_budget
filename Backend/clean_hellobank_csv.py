"""
L'objectif de ce module est de nettoyer un csv fourni par Fortuneo et de
retourner les lignes "propres" avec la fonction clean_entry_file.
Le procédé de nettoyage se déroule comme suit:
1. Remplacer ; par , ET , par .
2. Retirer les champs vides et le 3ème champ
3. Récupérer le montant et le mettre en 2ème position
4. Type de transaction: virement si champ vide et remplacer "PAIEMENT CB"
    par "Carte"
5. Description :
    - toutes les descriptions par carte sont de la forme :
        "FACTURE CARTE DU XXXXX [info] CARTE YYYYY"
        où XXXXX et YYYYY sont des suites de chiffres
        -> récupérer uniquement l'info
"""
import re

# dictionnaire indiquant les descriptions à modifier; la clé indique l'ancienne
# description à modifier et la valeur indique la nouvelle description
descriptions_to_replace = {
    "SNCF INTERNET PARIS 10": "SNCF",
}
# liste des types de transactions décrivant une transaction par virement
bank_transfer_types = ["VIREMENT",
                       "VIREMENT INTERNE",
                       "VIREMENT INSTANTANE RECU",
                       ]
# liste indiquant les chaines de caractères permettant de distinguer les
# descriptions des transactions par virement
valid_bank_transfer_descriptions = ["/FRM", "/DE", "/MOTIF",
                                    "VIRT CPTE A CPTE EMIS",
                                    "VERSEMENT PRIME HELLO BANK"]


def clean_transaction_type(transaction_field):
    """
    Remplace le type "PAIEMENT CB" par "Carte"
    et indique "Virement" si le champ est vide
    """
    new_transaction_type = ""
    transaction_field = transaction_field.strip()
    if not transaction_field or transaction_field in bank_transfer_types:
        new_transaction_type = "Virement"
    elif transaction_field == "PAIEMENT CB":
        new_transaction_type = "Carte"
    else:
        print("ERREUR: le type de transaction suivant est inattendu :",
              transaction_field)
    return new_transaction_type


def is_valid_bank_transfer_description(description_field):
    """
    Vérifie que la description contient /DE ou /MOTIF, au moins un des 2
    """
    for description in valid_bank_transfer_descriptions:
        if description in description_field:
            return True
    return False


def clean_description(description_field):
    """
    Nettoie le champ description fourni en entrée avec les règles données
    ci-dessus
    Le champ d'entrée est forcément soit un champ de paiement par carte ou
    de virement
    """
    new_description = ""
    description_field = description_field.strip()
    # traiter les transactions par carte
    # récupérer la description se situant entre la date et le mot CARTE
    description_pattern = r"FACTURE CARTE DU \d+ (.+?) CARTE \w+"
    match = re.search(description_pattern, description_field)
    if match:
        new_description = match.group(1)
    # traiter les transactions par virement
    # récupérer le motif de la transaction apparaissant après /MOTIF
    reason_pattern = r"/MOTIF ([^/]+)"
    reason_match = re.search(reason_pattern, description_field)
    reason_info = reason_match.group(1).strip() if reason_match else ""
    if reason_info == "":
        reason_info = "NO DESCRIPTION"
    new_description = reason_info
    return new_description


def clean_line(line):
    try:
        new_line = ""
        description = ""
        line = line.replace(",", ".")
        line = line.replace(";", ",")
        transaction_type = ""
        fields = line.split(",")
        fields = [field.strip() for field in fields]
        # le nombre d'éléments n'est pas constant :
        # il est possible que la description contienne plusieurs
        # champs dans le cas d'une transaction par virement
        date, transaction_type, _, *description_fields, amount = fields
        transaction_type = clean_transaction_type(transaction_type)
        if transaction_type == "Virement":
            # parmi les champs de description, récupérer le seul champ
            # qui nous intéresse (contenant un élément de la liste
            # valid_bank_transfer_descriptions)
            for des in description_fields:
                if is_valid_bank_transfer_description(des):
                    description = des
                    break
            # vérifier que le champ description est correct dans le cas
            # d'un virement
            assert is_valid_bank_transfer_description(description)
        else:
            # la transaction est faite par carte
            description = description_fields[0]
        # vérifier que le champ description est correct dans tous les cas
        assert (isinstance(description, str) and len(description) > 0)
    except AssertionError:
        print("Problème à la ligne: ", line)

    # nettoyer le champ description
    cleaned_description = clean_description(description)
    new_line = ",".join(
        [date, amount, transaction_type, cleaned_description])
    # ajout d'un champ supplémentaire indiquant la banque
    new_line += ",Hello Bank"
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
