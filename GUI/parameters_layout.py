from PySide6.QtWidgets import (
    QLabel, QLayout, QComboBox, QHBoxLayout,
    QWidget
)

# Variables globales
card_chart_title = "Dépenses par carte"
bank_transfer_chart_title = "Dépenses par virement"


class ParameterSelection(QLayout):
    """
    Cette classe définit un layout permettant de sélectionner un paramètre (mois, année, autre)
    Cette classe est une classe ABSTRAITE
    """

    def __init__(self, title, selection_list, default_text):
        super().__init__()

        self.parameter_selection_layout = QHBoxLayout()
        # définition du titre et d'une liste déroulante
        # pour la sélection d'un paramètre
        title_widget = QLabel(title)
        self.parameter_selection = QComboBox()
        self.parameter_selection.insertItems(0, selection_list)
        self.parameter_selection.setCurrentText(default_text)

        # ajout des widgets précédents au layout
        self.parameter_selection_layout.addWidget(title_widget)
        self.parameter_selection_layout.addWidget(self.parameter_selection)


class ChoiceBankWidget(QWidget):
    def __init__(self):
        self.label = QLabel("Banque sélectionnée :")
        self.bank_choice_combobox = QComboBox()
        self.bank_choice_combobox.insertItem(0, "Toutes les banques")
        self.bank_choice_combobox.insertItem(1, "LCL")


class ParametersLayout(QLayout):
    """
    Cette classe définit un layout permettant à l'utilisateur de saisir
    les paramètres du calcul
    """

    def __init__(self, month_selection_parameters, year_selection_parameters):
        super().__init__()

        self.parameters_layout = QHBoxLayout()
        # définir le widget de sélection de la période en mois
        month_selection_title = month_selection_parameters.title
        month_selection_list = month_selection_parameters.list
        month_selection_default_text = month_selection_parameters.default_text
        month_selection = ParameterSelection(month_selection_title,
                                             month_selection_list,
                                             month_selection_default_text)
        self.month_selection_box = month_selection.parameter_selection
        month_selection_layout = month_selection.parameter_selection_layout
        self.parameters_layout.addLayout(month_selection_layout)

        # définir le widget de sélection de la période en année
        year_selection_title = year_selection_parameters.title
        year_selection_list = year_selection_parameters.list
        year_selection_default_text = year_selection_parameters.default_text
        year_selection = ParameterSelection(year_selection_title,
                                            year_selection_list,
                                            year_selection_default_text)
        self.year_selection_box = year_selection.parameter_selection
        year_selection_layout = year_selection.parameter_selection_layout
        self.parameters_layout.addLayout(year_selection_layout)

        # sélectionner la banque
        choice_bank_widget = ChoiceBankWidget()
        label = choice_bank_widget.label
        bank_choice = choice_bank_widget.bank_choice_combobox
        self.parameters_layout.addWidget(label)
        self.parameters_layout.addWidget(bank_choice)
