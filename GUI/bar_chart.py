import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

from Backend.barplot_depenses import get_expenses_per_month


class BarChart(QtWidgets.QWidget):
    """
    Cette classe calcule puis affiche un diagramme en bâtons des dépenses 
    et des revenus mensuels
    """

    def __init__(self, parent_widget):
        super().__init__(parent=parent_widget)
        self.expenses = parent_widget.expenses
        self.revenus = parent_widget.revenus
        self.expenses = parent_widget.savings

        self.bar_canvas = QtWidgets.QWidget()

        """
        Extraction des mois et sommes pour afficher le diagramme
        """
        self.month_expenses = get_expenses_per_month(self.expenses)
        self.month_revenus = get_expenses_per_month(self.revenus)
        self.month_savings = get_expenses_per_month(self.expenses)

        categories = {
            "Dépenses": self.month_expenses,
            "Revenus": self.month_revenus,
            "Epargne": self.month_savings
        }

        # on fait en sorte que les dictionnaires aient la même longueur
        self.standardize_expenses()

        """
        Tracé du diagramme en bâtons
        """
        # ATTENTION lors du changement de la figsize
        # celle-ci semble ne pas introduire trop de bugs d'affichage
        # utiliser plutôt les barplots natifs de PySide 6 ???
        self.bar_canvas = FigureCanvas(Figure(figsize=(6, 8)))
        bar_ax = self.bar_canvas.figure.subplots()

        months = list(self.month_expenses.keys())
        step = np.arange(len(months))     # the label locations
        width = 0.25                      # the width of the bars
        multiplier = 0

        for category, transaction in categories.items():
            offset = width * multiplier
            rects = bar_ax.bar(step + offset, transaction.values(),
                               width, label=category)
            bar_ax.bar_label(rects, padding=3)
            multiplier += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        bar_ax.set_ylabel('Montant (en euros)')
        bar_ax.set_title(
            "Sommes des dépenses et revenus par mois et l'épargne sur la\
                période sélectionnée")
        bar_ax.set_xticks(step + width, months)
        bar_ax.legend(loc='upper left', ncols=3)

    def standardize_expenses(self):
        """
        Cette fonction sert à uniformiser les longueurs des dictionnaires des
        dépenses, revenus et épargne pour qu'ils aient la même longueur. Si
        pour un mois donné, un dictionnaire n'a pas de valeur, on donne par
        défaut la valeur 0
        """
        # la méthode est la suivante: on prend un dictionnaire sur les trois,
        # et on vérifie que chacune de ces clés (mois) est présente dans les
        # autres dictionnaires
        # sinon, on ajoute la clé avec la valeur 0
        # on répète l'opération pour les autres dictionnaires
        dictionnaries = [self.month_expenses,
                         self.month_revenus,
                         self.month_savings]

        for dictionnary in dictionnaries:
            left_dictionnaries = dictionnaries[:]
            left_dictionnaries.remove(dictionnary)
            for left_dictionnary in left_dictionnaries:
                for month in dictionnary.keys():
                    if month not in left_dictionnary:
                        # le mois est absent du dictionnaire
                        left_dictionnary[month] = 0.0
