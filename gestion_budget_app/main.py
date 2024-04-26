from PySide6.QtWidgets import QApplication

from GUI.main_window import MainWindow
from GUI.one_month_widget import OneMonthWidget
from GUI.several_months_widget import SeveralMonthsWidget


def main():
    app = QApplication([])
    widget_un_mois = OneMonthWidget()
    widget_plusieurs_mois = SeveralMonthsWidget()
    window = MainWindow(widget_un_mois, widget_plusieurs_mois)
    window.show()
    app.exec()
    return 0


if __name__ == "__main__":
    main()
