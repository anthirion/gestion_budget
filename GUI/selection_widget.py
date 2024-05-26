from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt, Slot

import global_variables as GV


class ViewSelectionWidget(QWidget):
    """
    Cette classe définit le widget permettant de choisir entre la vue sur un
    mois et la vue sur plusieurs mois.
    Ce widget est composé de 2 boutons seulement:
        - un bouton pour sélectionner la vue sur un mois
        - un bouton pour sélectionner la vue sur plusieurs mois
    Ce widget s'affiche en haut de chaque sous-menu
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        # widget affichant la vue sélectionnée (la vue d'un ou plusieurs mois)
        self.view_widget = parent_widget.view_widget

        selection_layout = QHBoxLayout(self)
        selection_layout.setSpacing(GV.vertical_spacing)
        # boutons de sélection de la vue
        one_month_selection = QPushButton("Vue sur un mois")
        one_month_selection.clicked.connect(self.one_month_view_selected)
        several_months_selection = QPushButton("Vue sur plusieurs mois")
        several_months_selection.clicked.connect(
            self.several_months_view_selected)
        for btn in (one_month_selection, several_months_selection):
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.setMinimumWidth(200)

        selection_layout.addWidget(one_month_selection)
        selection_layout.addWidget(several_months_selection)
        # afficher la sélection en haut et au centre
        selection_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter |
                                      Qt.AlignmentFlag.AlignTop)

    """
    Button slots
    """
    @Slot()
    def one_month_view_selected(self):
        """
        Afficher la vue sur un mois
        """
        self.view_widget.setCurrentIndex(0)

    @Slot()
    def several_months_view_selected(self):
        """
        Afficher la vue sur plusieurs mois
        """
        self.view_widget.setCurrentIndex(1)
