from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QFileDialog, QMessageBox, QMainWindow
from Calculation import initdata, calculation
from WindowData import WindowData
from CacheFile import CacheFile
from UpgradetWidgets import UpgradedTableWidget

debug = False


class Window(QMainWindow):
    def __init__(self):
        # Инициализация
        super(Window, self).__init__()
        self.ui = uic.loadUi("UIWindow.ui", self)

        # НАЗНАЧЕНИЕ ПЕРЕМЕННЫХ
        self.WindowData = WindowData()  # Класс со всеми входными данными
        self.cache_gelling = None  # гелеобразующие составы
        # файлы кэша
        self.cachefile_gelling = CacheFile("Gelling")
        self.cachefile_tableBeforeWatering = CacheFile("TableBeforeWatering")
        self.cachefile_tableAfterWatering = CacheFile("TableAfterWatering")
        # выпадающие списки
        self.combobox_gelling1 = self.ui.comboGelling1  # Выпадающий список с гелеобразующими составами
        self.combobox_gelling2 = self.ui.comboGelling2
        self.combobox_gelling3 = self.ui.comboGelling3
        # таблицы
        self.tableWatering = self.ui.tableWatering  # ГИС
        self.tableGelling = UpgradedTableWidget(self.ui.tableWidgetGelling)  # Гелеобразующие составы
        self.tableAfterWatering = UpgradedTableWidget(self.ui.tableAfterWatering)  # Данные после обводнения
        self.tableBeforeWatering = UpgradedTableWidget(self.ui.tableBeforeWatering)  # Данные до обводнения

        # Связывание кнопок (событий) с функциями (слотами)
        self.ui.btnGetData.clicked.connect(self.btn_getdata_clicked)  # Получить данные
        self.ui.bntCalculate.clicked.connect(self.btn_calculate_clicked)  # Рассчитать
        self.ui.btnAddGelling.clicked.connect(self.btn_addgelling_clicked)  # Добавить гелеобразующий состав
        self.combobox_gelling1.currentIndexChanged.connect(self.combobox_gelling_changed1)  # Выбор гелеобразующего состава
        self.combobox_gelling2.currentIndexChanged.connect(self.combobox_gelling_changed2)
        self.combobox_gelling3.currentIndexChanged.connect(self.combobox_gelling_changed3)

        # инициализация моих функций
        self.update_gelling()
        self.init_table_after_watering()
        self.init_table_before_watering()
        self.init_table_gelling()

    def closeEvent(self, *args, **kwargs):
        self.save_data()
        return super().closeEvent(*args, **kwargs)

    # ФУНКЦИИ ИНИЦИАЛИЗАЦИИ

    def init_table_after_watering(self):
        table = self.tableAfterWatering

        rows = ('Пласт',
                   'Pпл, атм',
                   'Pзаб, атм',
                   'Qж, м3/сут',
                   'Qг, тыс. м3/сут',
                   'ВГФ, м3/тыс. м3',
                   'Dэ/к, мм',
                   'Dнкт, мм',
                   'Rс, м',
                   'Hвд, м',
                   'Удл, м',
                   'D скв. дол., мм',
                   'Н перф, м',
                   'Толщина стенок НКТ, мм',
                   'Толщина стенок Э/К, мм',
                   'Давл. опрессовки, атм',
                   'Закачка с пакером',
                   'Вяз-ть пл.воды, сПз',
                   'Вяз-ть газа, сПз',
                   'Плотность газа,  г/см3',
                   'Пл-ть пл.воды, г/см3',
                   'К-т сверхсжимаемости газа',
                   'ΔT м/у устьем и забоем, ℃',
                   'Pбуф, атм',
                   'P конечное на устье, атм;',
                   'Расход жидкости, м3/сут',
                   'Pзаб план-е после РИР, атм')

        table.fill_labels(rows, ('Данные',))

        cache = self.cachefile_tableAfterWatering.read()
        if cache is not None:
            table.fill_data(self.cachefile_tableAfterWatering.read())

    def init_table_before_watering(self):
        table = self.tableBeforeWatering

        rows = ('Пласт',
                'Pпл, атм',
                'Pзаб, атм',
                'Qж, м3/сут',
                'Qг, тыс. м3/сут',
                'ВГФ, м3/тыс. м3')

        table.fill_labels(rows, ('Данные',))

        cache = self.cachefile_tableBeforeWatering.read()
        if cache is not None:
            table.fill_data(cache)

    def init_table_gelling(self):
        table = self.tableGelling

        columns = DialogAddGelling(self.cache_gelling).columns
        table.fill_labels(('1', '2', '3'), columns)

    # ОБРАБОТЧИКИ СОБЫТИЙ

    def btn_getdata_clicked(self):  # Нажатие на кнопку "получить данные"
        self.tableWatering.clear()
        self.load_data()

    def btn_calculate_clicked(self):  # Нажатие на кнопку "рассчитать"
        self.fill_data()
        res_list = calculation.calculation_click(self.WindowData)
        radius, stability, _, _ = tuple(res_list)
        result_window = DialogResult(radius, stability, self.WindowData)
        result_window.show()

    def btn_addgelling_clicked(self):  # Нажатие на кнопку "Добавить гелеобразующий состав"
        dialog_gelling = DialogAddGelling(self.cachefile_gelling)
        dialog_gelling.add_data()
        self.update_gelling()

    def combobox_gelling_changed1(self):
        gelling_key = self.combobox_gelling1.currentText()

        self.fill_table_gelling(1, gelling_key)

    def combobox_gelling_changed2(self):
        gelling_key = self.combobox_gelling2.currentText()

        self.fill_table_gelling(2, gelling_key)

    def combobox_gelling_changed3(self):
        gelling_key = self.combobox_gelling3.currentText()

        self.fill_table_gelling(3, gelling_key)

    # ПРОЧИЕ ФУНКЦИИ

    def load_data(self): # Загружает данные в таблицу из входного Excel

        if not debug:
            file_name = QFileDialog.getOpenFileName(self, 'Открыть файл')

        try:
            if debug:
                file_data = initdata.get_gis("../doc/origin_gis.xlsx")
            else:
                file_data = initdata.get_gis(file_name[0])
        except BaseException:
            Window.show_error(informative_text='Не удалось прочитать файл с данными')
            return
            # raise ImportError("Не удалось прочитать файл с данными")

        if len(file_data) == 0:  # если нет столбцов, то ничего не заполняем
            return

        self.tableWatering.setColumnCount(len(file_data))  # устанавливаем количество столбцов
        columns = file_data[0].__dict__  # получаем все переменные класса
        self.tableWatering.setRowCount(len(columns))  # устанавливаем количество строк
        self.tableWatering.setVerticalHeaderLabels(columns.values())  # даем названия строкам

        file_data.pop(0)  # удаляем первый столбец с именами

        # Заполняем данными таблицу
        for column_index, column in enumerate(file_data):
            for row_index, row in enumerate(columns):
                self.tableWatering.setItem(row_index, column_index, QTableWidgetItem(str(column.__getattribute__(row))))
        return file_data

    def fill_data(self):  # Заполнение класса WindowData
        self.WindowData.gis.clear()

        table = self.tableWatering
        row_count = table.rowCount()
        column_count = table.columnCount()

        # Заполняем обводнение
        for column_index in range(0, column_count):
            current_row = (table.item(row_index, column_index) for row_index in range(row_count))  # столбец таблицы
            current_row_text = (item.text() if item is not None else "" for item in current_row)  # текстовый столбец
            init_gis_row = initdata.InitGis(*tuple(current_row_text))  # делаем из текста класс InitGis
            self.WindowData.gis.append(init_gis_row)  # добавляем класс в список

        self.WindowData.gis_after_watering = self.tableAfterWatering.get_dict_column()
        self.WindowData.gis_before_watering = self.tableBeforeWatering.get_dict_column()

    def update_gelling(self):
        self.combobox_gelling1.clear()
        self.combobox_gelling2.clear()
        self.combobox_gelling3.clear()

        self.cache_gelling = self.cachefile_gelling.read()
        if self.cache_gelling is not None:
            self.cache_gelling = self.cache_gelling.data
        else:
            return

        if len(self.cache_gelling) == 0:
            return
        for gelling in self.cache_gelling:
            self.combobox_gelling1.addItem(gelling)
            self.combobox_gelling2.addItem(gelling)
            self.combobox_gelling3.addItem(gelling)

    def fill_table_gelling(self, num: int, key: str):
        if key == '':
            return

        num -= 1  # индекс стоки на 1 меньше номера колонки

        gelling_data = self.cache_gelling[key]

        for index, value in enumerate(gelling_data.values()):  # Заполнение таблицы
            self.tableGelling.table.setItem(num, index, QTableWidgetItem(value))

        self.WindowData.gelling[num] = gelling_data  # Заполняем выходной класс

    def save_data(self):  # сохраняем данные при закрытии проги
        self.cachefile_tableBeforeWatering.write(self.tableBeforeWatering.table_items())
        self.cachefile_tableAfterWatering.write(self.tableAfterWatering.table_items())

    @staticmethod
    def show_error(text='Error', informative_text='More information', title='Error'):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setInformativeText(informative_text)
        msg.setWindowTitle(title)
        msg.exec_()


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


class DialogResult(QMainWindow):
    def __init__(self, radius, stability, window_data: WindowData):
        super(DialogResult, self).__init__()
        self.ui = uic.loadUi('ResultWindow.ui', self)
        self.setWindowTitle("Вывод результатов вычислений")

        self.radius = radius
        self.stability = stability
        # self.radius_plot = radius_plot
        # self.injection_plot = injection_plot
        self.window_data = window_data

        self.table_radius = UpgradedTableWidget(self.ui.table_radius)
        self.table_stability = UpgradedTableWidget(self.ui.table_stability)

        self.ui.btn_show_radius.clicked.connect(self.show_radius)
        self.ui.btn_show_injection.clicked.connect(self.show_injection)

        self.fill_radius_table()
        self.fill_stability_table()

    def show_radius(self):
        calculation.get_radius_image(self.window_data)
        # self.radius_plot.show()

    def show_injection(self):
        calculation.get_injection_image(self.window_data)
        calculation.get_radius_graph(self.window_data)
        # self.injection_plot.show()

    def fill_radius_table(self):
        table = self.table_radius

        if len(self.radius) == 0:
            return

        column_names = self.radius[0]
        column_names.pop(0)
        row_names = list(map(lambda x: x[0], self.radius))
        row_names.pop(0)

        self.radius.pop(0)
        for row in self.radius:
            row.pop(0)

        table.fill_labels(row_names, column_names)
        table.fill_data(self.radius)

    def fill_stability_table(self):
        table = self.table_stability

        if len(self.stability) == 0:
            return

        # row_names = list(map(str, range(len(self.stability))))
        # column_names = list(map(str, range(len(self.stability[1]))))
        column_names = self.stability[0]
        column_names.pop(0)
        row_names = list(map(lambda x: x[0], self.stability))
        row_names.pop(0)

        self.stability.pop(0)
        for row in self.stability:
            row.pop(0)

        table.fill_labels(row_names, column_names)
        table.fill_data(self.stability)
