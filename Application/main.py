from PyQt5 import QtWidgets
import sys
from MainWindow import Window


def create_app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    create_app()

