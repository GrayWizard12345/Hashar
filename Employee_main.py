import sys

from PyQt6 import QtWidgets
from PyQt6.QtGui import QFont

from src import AuthEmployee
from utils.dev import setup_logging
from utils.pathfinder import UI_LOG_FILE

if __name__ == '__main__':
    setup_logging(UI_LOG_FILE)
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(QFont("Gilroy", 12))

    auth = QtWidgets.QWidget()

    window = AuthEmployee()
    window.setupUi(auth)
    auth.show()

    sys.exit(app.exec())
