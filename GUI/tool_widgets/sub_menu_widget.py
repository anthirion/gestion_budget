from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QStackedWidget, QLabel
)
from GUI.views.selection_widget import ViewSelectionWidget
from GUI.views.one_month_view import OneMonthView
from GUI.views.several_months_view import SeveralMonthsView

from PySide6.QtCore import Qt

import global_variables as GV


class SubMenuWidget(QWidget):
    """
    Cette classe définit le widget affiché à la sélection d'un sous-menu
    sélectionné depuis le menu latéral.
    Ce sous-menu permet d'afficher une des 2 vues suivantes:
        - une vue des dépenses sur un mois
        - une vue des dépenses sur plusieurs mois
    """

    def __init__(self, parent_widget, sub_menu):
        """
        @parameter {str} sub_menu: le sous-menu sélectionné à partir du menu
            latéral
        Il y a quatre sous-menus possibles:
            - Dépenses
            - Revenus
            - Patrimoine
            - Transactions
        """
        super().__init__(parent=parent_widget)

        # ce dictionnaire sert à afficher le bon QLabel à la sélection du
        # sous-menu (voir le QLabel associé à no_view_selected)
        sub_menu_to_french = {"expenses": "des dépenses",
                              "revenus": "des revenus",
                              "savings": "du patrimoine",
                              }

        # layout principal du widget courant
        expenses_layout = QVBoxLayout(self)
        expenses_layout.setSpacing(GV.horizontal_spacing)
        # widget affichant la vue sélectionnée (la vue d'un ou plusieurs mois)
        self.view_widget = QStackedWidget(self)

        """
        Widget permettant de sélectionner la vue souhaitée: soit la vue sur un
        mois, soit celle sur plusieurs mois
        """
        selection_widget = ViewSelectionWidget(self)
        expenses_layout.addWidget(selection_widget)

        """
        Widget affichant la vue sélectionnée (la vue d'un ou plusieurs mois)
        """
        # vue affichée lorsqu'aucune vue n'est sélectionnée
        no_view_selected = \
            QLabel(f"Bienvenue dans le menu {sub_menu_to_french[sub_menu]} !\n\
                   Sélectionner une vue en haut pour commencer !",
                   self.view_widget)
        no_view_selected.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # vue affichant à la sélection d'un mois
        one_month_view = OneMonthView(self.view_widget,
                                      transaction_type=sub_menu)
        # vue affichant à la sélection de plusieurs mois
        several_months_view = SeveralMonthsView(self.view_widget,
                                                transaction_type=sub_menu)

        self.view_widget.addWidget(no_view_selected)
        self.view_widget.addWidget(one_month_view)
        self.view_widget.addWidget(several_months_view)

        expenses_layout.addWidget(self.view_widget)
