from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow
from OneMonthExpensesWidget import OneMonthExpensesWidget
from SeveralMonthsExpensesWidget import SeveralMonthsExpensesWidget


if __name__ == "__main__":
    clean_csv_filename = "/home/thiran/projets_persos/gestion_budget/csv_files/clean_csv_files/source_of_truth.csv"
    app = QApplication([])
    depenses_sur_un_mois = OneMonthExpensesWidget(clean_csv_filename)
    depenses_sur_plusieurs_mois = SeveralMonthsExpensesWidget(
        clean_csv_filename)
    window = MainWindow(depenses_sur_un_mois, depenses_sur_plusieurs_mois)
    window.show()
    app.exec()
