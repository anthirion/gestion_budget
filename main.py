from PySide6.QtWidgets import QApplication

import MainWindow
from OneMonthWidget import OneMonthWidget
from SeveralMonthsWidget import SeveralMonthsWidget

import GlobalVariables

if __name__ == "__main__":
    app = QApplication([])
    widget_un_mois = OneMonthWidget()
    widget_plusieurs_mois = SeveralMonthsWidget()
    window = MainWindow.MainWindow(widget_un_mois, widget_plusieurs_mois)
    window.show()
    app.exec()
