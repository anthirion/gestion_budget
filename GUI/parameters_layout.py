from PySide6.QtWidgets import (
    QLabel, QHBoxLayout, QComboBox, QWidget
)


class OneMonthParametersWidget(QWidget):
    """
    Cette classe définit le widget des paramètres de calcul, affiché dans
    la vue sur un seul mois
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        """
        Définition des paramètres utiles pour la sélection du mois
        et de l'année
        """
        month_selection_title = "Mois sélectionné :"
        month_selection_list = [str(i) for i in range(1, 13)]
        month_selection_default_text = "11"

        year_selection_title = "/"
        year_selection_list = [str(i) for i in range(2020, 2031)]
        year_selection_default_text = "2023"

        self.parameters_layout = QHBoxLayout()
        """
        Définition du widget de sélection du mois
        """
        month_selection_label = QLabel(month_selection_title)
        month_selection_combobox = QComboBox()
        for selection_item in month_selection_list:
            month_selection_combobox.addItem(selection_item)
        month_selection_combobox.setCurrentText(month_selection_default_text)

        self.parameters_layout.addWidget(month_selection_label)
        self.parameters_layout.addWidget(month_selection_combobox)

        # récupérer le mois sélectionné via la combobox pour les calculs
        # ultérieurs
        self.selected_month = month_selection_combobox.currentText()

        """
        Définition du widget de sélection de l'année
        """
        year_selection_label = QLabel(year_selection_title)
        year_selection_combobox = QComboBox()
        for selection_item in year_selection_list:
            year_selection_combobox.addItem(selection_item)
        year_selection_combobox.setCurrentText(year_selection_default_text)

        self.parameters_layout.addWidget(year_selection_label)
        self.parameters_layout.addWidget(year_selection_combobox)

        # récupérer l'année sélectionnée via la combobox pour les calculs
        # ultérieurs
        self.selected_year = year_selection_combobox.currentText()

        """
        Définition du widget permettant de sélectioner la banque
        """
        # ajout d'un peu d'espace avant le widget de sélection de la banque
        # pour aérer
        self.parameters_layout.insertSpacing(4, 300)
        bank_label = QLabel("Banque sélectionnée :")
        bank_combobox = QComboBox()
        bank_combobox.addItem("Toutes les banques")
        bank_combobox.addItem("LCL")

        self.parameters_layout.addWidget(bank_label)
        self.parameters_layout.addWidget(bank_combobox)
