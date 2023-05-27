from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from MainWindow import Ui_MainWindow
import sys
import initdata


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.load_data()
        self.ui.btnGetData.clicked.connect(self.btnGetDataClicked)

    def load_data(self):
        # Загружает данные в таблицу из входного Excel

        # self.ui.tableWidget.setItem(0, 0, QTableWidgetItem('Test value'))
        # self.ui.tableWidget.setItem(0, 1, QTableWidgetItem('5000 tonn'))
        try:
            file_data = initdata.get_gis("../doc/gis.xlsx")
        except:
            raise ImportError("Не удалось прочитать файл с данными")

        if len(file_data) == 0:  # если нет столбцов, то ничего не заполняем
            return

        self.ui.tableWidget.setColumnCount(len(file_data))  # устанавливаем количество столбцов
        columns = file_data[0].__dict__  # получаем все переменные класса
        self.ui.tableWidget.setRowCount(len(columns))  # устанавливаем количество строк
        self.ui.tableWidget.setVerticalHeaderLabels(columns.keys())  # даем названия строкам

        # Заполняем данными таблицу
        for column_index, column in enumerate(file_data):
            for row_index, row in enumerate(columns):
                self.ui.tableWidget.setItem(row_index, column_index, QTableWidgetItem(str(column.__getattribute__(row))))

    def btnGetDataClicked(self):
        self.ui.tableWidget.clear()
        self.load_data()


def create_app():
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    create_app()
    # data = initdata.get_gis("../doc/gis.xlsx")
