import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from config import APP_NAME, ICON_PATH
from PyQt6.QtGui import QIcon

def main():
    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setWindowIcon(QIcon(str(ICON_PATH)))

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()