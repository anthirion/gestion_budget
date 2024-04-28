from PySide6.QtWidgets import (
    QLabel, QWidget, QComboBox
)


class ChoiceBankWidget(QWidget):
    def __init__(self):
        self.label = QLabel("Banque sélectionnée :")
        self.bank_choice_combobox = QComboBox()
        self.bank_choice_combobox.insertItem(0, "Toutes les banques")
        self.bank_choice_combobox.insertItem(1, "LCL")
