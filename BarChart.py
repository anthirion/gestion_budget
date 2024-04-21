import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

import barplot_depenses


class BarChart(QtWidgets.QWidget):
    """
    Cette classe calcule puis affiche un diagramme en bâtons des dépenses 
    et des revenus mensuels
    """

    def __init__(self, depenses, revenus, epargne):
        super().__init__()
        self.depenses = depenses
        self.revenus = revenus
        self.epargne = epargne

        self.bar_canvas = QtWidgets.QWidget()

        """
        Extraction des mois et sommes pour afficher le diagramme
        """
        self.depenses_mensuelles = barplot_depenses.get_expenses_per_month(
            self.depenses)
        self.revenus_mensuels = barplot_depenses.get_expenses_per_month(
            self.revenus)
        self.epargne_mensuelle = barplot_depenses.get_expenses_per_month(
            self.epargne)

        categories = {
            "Dépenses": self.depenses_mensuelles,
            "Revenus": self.revenus_mensuels,
            "Epargne": self.epargne_mensuelle
        }

        # on fait en sorte que les dictionnaires aient la même longueur
        self.standardize_expenses()

        """
        Tracé du diagramme en bâtons
        """
        self.bar_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        bar_ax = self.bar_canvas.figure.subplots()

        months = list(self.depenses_mensuelles.keys())
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
            "Sommes des dépenses et revenus par mois et l'épargne sur la période sélectionnée")
        bar_ax.set_xticks(step + width, months)
        bar_ax.legend(loc='upper left', ncols=3)

        # afficher la moyenne des dépenses sur le diagramme en batons
        depenses_mensuelles = self.depenses_mensuelles.values()
        expenses_mean_per_month = \
            sum(depenses_mensuelles for depenses_mensuelles in depenses_mensuelles) / \
            len(depenses_mensuelles)
        bar_ax.axhline(y=expenses_mean_per_month, color="red")
        # on ajoute un texte à la ligne pour indiquer le montant de la moyenne
        bar_ax.text(x=-1.2, y=expenses_mean_per_month,
                    s=f"Moyenne des dépenses mensuelles : \n {expenses_mean_per_month}€",
                    color="red")

    def standardize_expenses(self):
        """
        Cette fonction sert à uniformiser les longueurs des dictionnaires des dépenses,
        revenus et épargne pour qu'ils aient la même longueur. Si pour un mois donné,
        un dictionnaire n'a pas de valeur, on donne par défaut la valeur 0
        """
        # la méthode est la suivante: on prend un dictionnaire sur les trois, et on vérifie que
        # chacune de ces clés (mois) est présente dans les autres dictionnaires
        # sinon, on ajoute la clé avec la valeur 0
        # on répète l'opération pour les autres dictionnaires
        dictionnaries = [self.depenses_mensuelles,
                         self.revenus_mensuels,
                         self.epargne_mensuelle]

        for dictionnary in dictionnaries:
            left_dictionnaries = dictionnaries[:]
            left_dictionnaries.remove(dictionnary)
            for left_dictionnary in left_dictionnaries:
                for month in dictionnary.keys():
                    if month not in left_dictionnary:
                        # le mois est absent du dictionnaire
                        left_dictionnary[month] = 0.0
