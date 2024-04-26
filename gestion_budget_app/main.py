from PySide6.QtWidgets import QApplication

from GUI.main_window import MainWindow


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
    return 0


if __name__ == "__main__":
    main()
