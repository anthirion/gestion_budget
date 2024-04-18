from PySide6.QtWidgets import QApplication

from MainWindow import MainWindow
from OneMonthWidget import OneMonthWidget
from SeveralMonthsWidget import SeveralMonthsWidget


if __name__ == "__main__":
    clean_csv_filename = "/home/thiran/projets_persos/gestion_budget/csv_files/clean_csv_files/source_of_truth.csv"
    app = QApplication([])
    widget_un_mois = OneMonthWidget(clean_csv_filename)
    widget_plusieurs_mois = SeveralMonthsWidget(
        clean_csv_filename)
    window = MainWindow(widget_un_mois, widget_plusieurs_mois)
    window.show()
    app.exec()
