from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QDialog
import initdata
from WindowData import WindowData
from CacheFile import CacheFile


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        # Инициализация
        super(Window, self).__init__()
        self.ui = uic.loadUi("UIWindow.ui", self)

        # Назначение переменных
        self.WindowData = WindowData()  # Класс со всеми входными данными
        self.tableWatering = self.ui.tableWatering  # Таблица с обводнениями
        self.cache_gelling = None  # гелеобразующие составы
        self.cachefile_gelling = CacheFile("Gelling")  # Файл с данными гелеобразующих составов
        self.combobox_gelling = self.ui.comboGelling  # Выпадающий список с гелеобразующими составами
        self.tableGelling = self.ui.tableWidgetGelling   # Таблица с гелеобразующими составами


        # Связывание кнопок с функциями
        self.ui.btnGetData.clicked.connect(self.btn_getdata_clicked)  # Получить данные
        self.ui.bntCalculate.clicked.connect(self.btn_calculate_clicked)  # Рассчитать
        self.ui.btnAddGelling.clicked.connect(self.btn_addgelling_clicked)  # Добавить гелеобразующий состав
        self.combobox_gelling.currentIndexChanged.connect(self.combobox_gelling_changed)  # Выбор гелеобразующего состава

        # инициализация моих функций
        self.update_gelling()

    def load_data(self):  # Загружает данные в таблицу из входного Excel

        try:
            file_data = initdata.get_gis("../doc/gis.xlsx")
        except BaseException:
            raise ImportError("Не удалось прочитать файл с данными")

        if len(file_data) == 0:  # если нет столбцов, то ничего не заполняем
            return

        self.tableWatering.setColumnCount(len(file_data))  # устанавливаем количество столбцов
        columns = file_data[0].__dict__  # получаем все переменные класса
        self.tableWatering.setRowCount(len(columns))  # устанавливаем количество строк
        self.tableWatering.setVerticalHeaderLabels(columns.keys())  # даем названия строкам

        # Заполняем данными таблицу
        for column_index, column in enumerate(file_data):
            for row_index, row in enumerate(columns):
                self.tableWatering.setItem(row_index, column_index, QTableWidgetItem(str(column.__getattribute__(row))))
        return file_data

    def fill_data(self):  # Заполнение класса WindowData
        self.WindowData.gis = self.load_data()

    def btn_getdata_clicked(self):  # Нажатие на кнопку "получить данные"
        self.tableWatering.clear()
        self.load_data()

    def btn_calculate_clicked(self):  # Нажатие на кнопку "рассчитать"
        print("Нажата кнопка Рассчитать")
        self.fill_data()
        # Фукнция ильдара

    def btn_addgelling_clicked(self):  # Нажатие на кнопку "Добавить гелеобразующий состав"
        dialog_gelling = DialogAddGelling(self.cachefile_gelling)
        dialog_gelling.add_data()
        self.update_gelling()

    def update_gelling(self):
        self.combobox_gelling.clear()

        self.cache_gelling = self.cachefile_gelling.read()
        if self.cache_gelling is not None:
            self.cache_gelling = self.cache_gelling.data
        else:
            return

        if len(self.cache_gelling) == 0:
            return
        for gelling in self.cache_gelling:
            self.combobox_gelling.addItem(gelling)

    def combobox_gelling_changed(self):
        gelling_key = self.combobox_gelling.currentText()
        if gelling_key == '':
            return
        gelling_data = self.cache_gelling[gelling_key]

        # Инициализация таблицы
        self.tableGelling.setRowCount(1)
        self.tableGelling.setColumnCount(len(gelling_data))
        self.tableGelling.setHorizontalHeaderLabels(gelling_data.keys())

        for index, value in enumerate(gelling_data.values()):  # Заполнение таблицы
            self.tableGelling.setItem(0, index, QTableWidgetItem(value))

        self.WindowData.gelling = gelling_data


class DialogAddGelling(QDialog):
    def __init__(self, cache_file):
        self.columns = {"Name": None,
                        "К, Па*с": None,
                        "n": None,
                        "Rост_в": None,
                        "Rост_г": None,
                        "Кр.гр.дав_в, атм/м": None,
                        "Кр.гр.дав_г, атм/м": None,
                        "Q, м3/сут": None,
                        "V, м3": None,
                        "Пл-ть, г/см3": None,
                        "Время геле-обр-я., мин": None}
        super(DialogAddGelling, self).__init__()
        self.ui = uic.loadUi("DialogAddGelling.ui", self)
        self.setWindowTitle("Добавление гелеобразующего состава")
        self.cache_file = cache_file
        self.fill_table()

    def fill_table(self):
        self.ui.tableWidgetGelling.setColumnCount(len(self))
        self.ui.tableWidgetGelling.setRowCount(1)
        self.ui.tableWidgetGelling.setHorizontalHeaderLabels(self.columns.keys())

    def __len__(self):
        return len(self.columns)

    def add_data(self):
        if self.exec() == 0:  # Если нажали "ок" в окне
            return

        gelling_container = self.cache_file.read()  # считываем данные с файла
        if gelling_container is None:
            gelling_container = GellingContainer()

        for index, key in enumerate(self.columns):
            value = self.ui.tableWidgetGelling.item(0, index)
            if value is None:
                self.columns[key] = ""
            else:
                self.columns[key] = value.text()

        gelling_container.add(self.columns)
        self.cache_file.write(gelling_container)


class GellingContainer:
    def __init__(self):
        self.data = dict()

    def add(self, columns):
        name = columns["Name"]
        columns.pop("Name")
        self.data[name] = columns

    def __len__(self):
        return len(self.data)

