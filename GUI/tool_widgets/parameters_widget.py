from PySide6.QtWidgets import (
    QLabel, QHBoxLayout, QComboBox, QWidget
)
from PySide6.QtCore import Qt
from datetime import datetime

import global_variables as GV


class SubMenuParametersWidget(QWidget):
    """
    Cette classe définit le widget des paramètres de calcul, affiché dans
    la vue sur un seul mois, à savoir:
        - la période à analyser (mois/année)
        - la banque d'où les transactions sont tirées
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        parameters_layout = QHBoxLayout(self)

        """
        Widget permettant de sélectioner le mois
        """
        # les mois et année par défaut sont les mois et année actuels
        now = datetime.now()
        current_month = now.month
        current_year = now.year

        month_selection_list = [str(i) for i in range(1, 13)]
        month_selection_default_text = str(current_month)

        month_selection_label = QLabel("Période sélectionnée:", self)
        self.month_selection_combobox = QComboBox(self)
        for selection_item in month_selection_list:
            self.month_selection_combobox.addItem(selection_item)
        self.month_selection_combobox.setCurrentText(
            month_selection_default_text)

        parameters_layout.addWidget(month_selection_label)
        parameters_layout.addWidget(self.month_selection_combobox)

        """
        Widget permettant de sélectioner l'année
        """
        year_selection_list = [str(i) for i in range(2020, 2031)]
        year_selection_default_text = str(current_year)

        year_selection_label = QLabel("/", self)
        self.year_selection_combobox = QComboBox(self)
        for selection_item in year_selection_list:
            self.year_selection_combobox.addItem(selection_item)
        self.year_selection_combobox.setCurrentText(
            year_selection_default_text)

        parameters_layout.addWidget(year_selection_label)
        parameters_layout.addWidget(self.year_selection_combobox)

        """
        Widget permettant de sélectioner la banque
        """
        # ajout d'un peu d'espace avant le widget de sélection de la banque
        # pour aérer
        parameters_layout.insertSpacing(4, GV.widgets_spacing)
        choice_bank_widget = ChoiceBankWidget(self)
        parameters_layout.addWidget(choice_bank_widget,
                                    Qt.AlignmentFlag.AlignRight)

        # fixer une taille maximale à tous les widgets définis pour ne pas
        # qu'ils soient trop étirés
        for widget in [month_selection_label, self.month_selection_combobox,
                       year_selection_label, self.year_selection_combobox]:
            widget.setMaximumWidth(GV.max_widget_width)

    def get_period(self):
        """
        Cette méthode permet de récupérer la période (mois/année)
        choisie par l'utilisateur à travers les combobox
        """
        month_choice = int(self.month_selection_combobox.currentText())
        year_choice = int(self.year_selection_combobox.currentText())
        return (month_choice, year_choice)


class OverviewSubMenuParametersWidget(QWidget):
    """
    Cette classe définit le widget des paramètres de calcul, affiché dans
    la vue sur plusieurs mois
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        parameters_layout = QHBoxLayout(self)

        """
        Widget permettant de sélectioner le nombre de mois à analyser
        """
        month_selection_list = [str(i) for i in range(1, 12)]
        month_selection_default_text = "5"

        month_selection_label = QLabel("Période :", self)
        self.month_selection_combobox = QComboBox(self)
        for selection_item in month_selection_list:
            self.month_selection_combobox.addItem(selection_item)
        self.month_selection_combobox.setCurrentText(
            month_selection_default_text)
        month_additional_label = QLabel("mois et", self)

        parameters_layout.addWidget(month_selection_label)
        parameters_layout.addWidget(self.month_selection_combobox)
        parameters_layout.addWidget(month_additional_label)

        """
        Widget permettant de sélectioner le nombre d'années à analyser
        """
        year_selection_list = [str(i) for i in range(0, 10)]
        year_selection_default_text = "0"

        self.year_selection_combobox = QComboBox(self)
        for selection_item in year_selection_list:
            self.year_selection_combobox.addItem(selection_item)
        self.year_selection_combobox.setCurrentText(
            year_selection_default_text)
        year_additional_label = QLabel("annees", self)

        parameters_layout.addWidget(self.year_selection_combobox)
        parameters_layout.addWidget(year_additional_label)

        # fixer une taille maximale à tous les widgets définis pour ne pas
        # qu'ils soient trop étirés
        for widget in [month_selection_label, self.month_selection_combobox,
                       year_additional_label, self.year_selection_combobox]:
            widget.setMaximumWidth(GV.max_widget_width)

        """
        Définition du widget permettant de sélectionner la banque
        """
        # ajout d'un peu d'espace avant le widget de sélection de la banque
        # pour aérer
        parameters_layout.insertSpacing(5, GV.widgets_spacing)
        choice_bank_widget = ChoiceBankWidget(self)
        parameters_layout.addWidget(choice_bank_widget,
                                    Qt.AlignmentFlag.AlignRight)

    def get_period(self):
        """
        Cette méthode permet de récupérer la période (mois/année)
        choisie par l'utilisateur à travers les combobox
        """
        month_choice = int(self.month_selection_combobox.currentText())
        year_choice = int(self.year_selection_combobox.currentText())
        return (month_choice, year_choice)


class ChoiceBankWidget(QWidget):
    """
    Cette classe définit le widget permettant la sélection de la banque
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        layout = QHBoxLayout(self)
        label = QLabel("Banque sélectionnée :", self)
        bank_choice_combobox = QComboBox(self)
        bank_choice_combobox.addItem("Toutes les banques")
        bank_choice_combobox.addItem("LCL")
        layout.addWidget(label)
        layout.addWidget(bank_choice_combobox)

        # fixer une taille maximale à tous les widgets définis pour ne pas
        # qu'ils soient trop étirés
        label.setMaximumWidth(150)
        bank_choice_combobox.setMaximumWidth(300)
