from PySide6 import QtCharts

from Backend.pie_chart import split_transactions_by_categories


class ExpensesPieChart(QtCharts.QChart):
    """
    Cette classe calcule le camembert des dépenses passées en paramètre dans
    le constructeur
    """

    def __init__(self, transactions, condenser_value):
        """
        @parameter transactions: transactions à afficher
        @parameter condenser_value: indique s'il faut afficher la catégorie
            Autre ou non
        """
        super().__init__()
        self.transactions = transactions

        self.pie_chart = QtCharts.QChart()
        series = QtCharts.QPieSeries()

        expenses = split_transactions_by_categories(self.transactions,
                                                    condenser=condenser_value)

        # afficher les valeurs sur le camembert
        slices = []
        for categorie, amount in expenses.items():
            pie_slice = QtCharts.QPieSlice("", amount)
            label = f"<p align='center'> {categorie} <br> \
                {round(pie_slice.value(), 2)} €</p>"
            pie_slice.setLabel(label)
            slices.append(pie_slice)
            series.append(pie_slice)

        # modifier l'affichage des labels en fonction de leur pourcentage
        # for pie_slice in slices:
        #     if pie_slice.percentage() > global_variables.pourcentage_affichage_label_pie_chart:
        #         # si le montant est suffisamment grand pour être affiché correctement dans le camembert
        #         # on l'affiche à l'intérieur et en blanc pour être lisible
        #         pie_slice.setLabelPosition(
        #             QtCharts.QPieSlice.LabelInsideHorizontal)
        #         pie_slice.setLabelColor(QtGui.QColor("white"))
        #     else:
        #         # si le montant est trop petit pour être affiché
        #         # correctement dans le camembert
        #         # on préfère l'afficher à l'extérieur et en noir
        #         pie_slice.setLabelPosition(
        #             QtCharts.QPieSlice.LabelOutside)
        #         pie_slice.setLabelColor(QtGui.QColor("black"))

        # afficher les labels sur le camembert
        series.setLabelsVisible(True)

        # mettre à jour le graphe
        self.pie_chart.addSeries(series)
        # masquer la légende
        self.pie_chart.legend().hide()
