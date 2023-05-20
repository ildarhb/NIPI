from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from MainWindow import Ui_MainWindow
import sys


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.load_data()

    def load_data(self):
        self.ui.tableWidget.setRowCount(3)
        self.ui.tableWidget.setColumnCount(2)

        self.ui.tableWidget.setHorizontalHeaderLabels(('Liq', 'Oil'))

        self.ui.tableWidget.setItem(0, 0, QTableWidgetItem('Test value'))
        self.ui.tableWidget.setItem(0, 1, QTableWidgetItem('5000 tonn'))

    # def get_data(self):
    #     self.ui.tableWidget.

def create_app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # create_app()
    import initdata
    test = initdata.get_gis()
    print(test)
