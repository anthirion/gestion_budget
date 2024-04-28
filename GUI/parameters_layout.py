from PySide6.QtWidgets import (
    QLabel, QLayout, QComboBox, QHBoxLayout,
)

from GUI.choice_bank_widget import ChoiceBankWidget

# Variables globales
card_chart_title = "Dépenses par carte"
bank_transfer_chart_title = "Dépenses par virement"


class ParametersLayout(QLayout):
    """
    Ce widget permet à l'utilisateur de sélectionner
    les paramètres de calcul : 
        - le mois sur lequel faire l'analyse et
        - la ou les banque(s) sélectionnée(s)
    """

    def __init__(self, month_selection_list, month_selection_default_text,
                 year_selection_list, year_selection_default_text):
        super().__init__()

        self.parameters_layout = QHBoxLayout()
        self.parameters_layout.addWidget(QLabel("Mois sélectionné :"))
        # sélectionner la période en mois
        self.month_selection = QComboBox()
        self.month_selection.insertItems(0, month_selection_list)
        self.month_selection.setCurrentText(month_selection_default_text)
        self.parameters_layout.addWidget(self.month_selection)
        # periode en années
        self.parameters_layout.addWidget(QLabel("/"))
        self.year_selection = QComboBox()
        self.year_selection.insertItems(0, year_selection_list)
        self.year_selection.setCurrentText(year_selection_default_text)
        self.parameters_layout.addWidget(self.year_selection)

        # sélectionner la banque
        choice_bank_widget = ChoiceBankWidget()
        label = choice_bank_widget.label
        bank_choice = choice_bank_widget.bank_choice_combobox
        self.parameters_layout.addWidget(label)
        self.parameters_layout.addWidget(bank_choice)
