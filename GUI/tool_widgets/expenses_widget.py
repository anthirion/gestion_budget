from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QStackedWidget
)
from GUI.tool_widgets.selection_widget import ViewSelectionWidget
from GUI.views.one_month_view import OneMonthView
from GUI.views.several_months_view import SeveralMonthsView

import global_variables as GV


class ExpensesWidget(QWidget):
    """
    Cette classe définit le widget affiché lorsque le sous-menu "Dépenses"
    est sélectionné.
    Il permet ensuite d'afficher une des 2 vues suivante:
        - une vue des dépenses sur un mois
        - une vue des dépenses sur plusieurs mois
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
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
        # vue affichant à la sélection d'un mois
        one_month_view = OneMonthView(self, transaction_type="expenses")
        several_months_view = SeveralMonthsView(self,
                                                transaction_type="expenses")
        self.view_widget.addWidget(one_month_view)
        self.view_widget.addWidget(several_months_view)

        expenses_layout.addWidget(self.view_widget)
